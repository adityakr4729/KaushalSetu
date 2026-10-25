import re
import secrets
from functools import wraps
from flask import session, redirect, url_for, flash, request, g, abort
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

def validate_registration_input(full_name, email, password, confirm_password, education_level):
    """Validate user registration inputs."""
    errors = []
    
    if not full_name or len(full_name.strip()) < 2:
        errors.append("Full Name must be at least 2 characters long.")
        
    if not email or not EMAIL_REGEX.match(email.strip()):
        errors.append("Please provide a valid email address.")
        
    if not password or len(password) < 6:
        errors.append("Password must be at least 6 characters long.")
        
    if password != confirm_password:
        errors.append("Passwords do not match.")
        
    if not education_level or not education_level.strip():
        errors.append("Please select your current education level.")
        
    return errors

def register_user(full_name, email, password, confirm_password, education_level, college_name=None):
    """Register a new student user and create their initial profile."""
    errors = validate_registration_input(full_name, email, password, confirm_password, education_level)
    if errors:
        return None, errors
        
    email_clean = email.strip().lower()
    full_name_clean = full_name.strip()
    college = (college_name or "").strip()
    
    db = get_db()
    
    # Check for existing user
    existing = db.execute("SELECT id FROM users WHERE email = ?", (email_clean,)).fetchone()
    if existing:
        return None, ["An account with this email address already exists. Please login instead."]
        
    password_hash = generate_password_hash(password)
    
    try:
        cursor = db.execute("""
            INSERT INTO users (full_name, email, password_hash, education_level, college_name)
            VALUES (?, ?, ?, ?, ?)
        """, (full_name_clean, email_clean, password_hash, education_level.strip(), college))
        user_id = cursor.lastrowid
        
        # Initialize student profile record
        db.execute("""
            INSERT INTO student_profiles (user_id, target_career, degree_course, academic_year)
            VALUES (?, 'Python Developer', ?, '3rd Year')
        """, (user_id, education_level.strip()))
        
        db.commit()
        return user_id, []
    except Exception as e:
        db.rollback()
        return None, [f"Registration error: {str(e)}"]

def authenticate_user(email, password):
    """Authenticate user with email and password."""
    if not email or not password:
        return None, "Please enter both email and password."
        
    email_clean = email.strip().lower()
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE email = ?", (email_clean,)).fetchone()
    
    if not user:
        return None, "No account found with this email. Please check your email or register."
        
    if not check_password_hash(user['password_hash'], password):
        return None, "Incorrect password. Please try again."
        
    return dict(user), None

def login_user(user, remember=False):
    """Set session state for authenticated user."""
    session.clear()
    session['user_id'] = user['id']
    session['user_name'] = user['full_name']
    session['user_email'] = user['email']
    if remember:
        session.permanent = True
    else:
        session.permanent = False

def logout_user():
    """Clear user session."""
    session.clear()

def get_current_user():
    """Fetch current user record from database based on session."""
    user_id = session.get('user_id')
    if not user_id:
        return None
    db = get_db()
    user = db.execute("SELECT id, full_name, email, education_level, college_name, created_at FROM users WHERE id = ?", (user_id,)).fetchone()
    return dict(user) if user else None

def login_required(view):
    """Decorator to protect routes requiring authentication."""
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login', next=request.path))
        return view(**kwargs)
    return wrapped_view

# CSRF Protection Helpers
def generate_csrf_token():
    """Generate or retrieve a session CSRF token."""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(24)
    return session['csrf_token']

def validate_csrf():
    """Validate submitted CSRF token for state-changing requests."""
    token = request.form.get('csrf_token') or request.headers.get('X-CSRFToken')
    expected = session.get('csrf_token')
    if not expected or not token or not secrets.compare_digest(expected, token):
        abort(400, description="Invalid or missing CSRF security token. Please refresh and try again.")

def update_user_password(user_id, current_password, new_password, confirm_new_password):
    """Update user password securely."""
    if not new_password or len(new_password) < 6:
        return False, "New password must be at least 6 characters long."
    if new_password != confirm_new_password:
        return False, "New passwords do not match."
        
    db = get_db()
    user = db.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user or not check_password_hash(user['password_hash'], current_password):
        return False, "Current password is incorrect."
        
    new_hash = generate_password_hash(new_password)
    db.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
    db.commit()
    return True, "Password updated successfully!"

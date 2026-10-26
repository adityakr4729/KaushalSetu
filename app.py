import os
from flask import (
    Flask, render_template, request, redirect, url_for, flash,
    session, jsonify, g, abort
)
from config import Config, DevelopmentConfig, ProductionConfig
from database import get_db, init_db, init_app
from services import (
    register_user, authenticate_user, login_user, logout_user,
    get_current_user, login_required, generate_csrf_token, validate_csrf,
    update_user_password, get_questions_for_career, evaluate_assessment,
    save_assessment_record, get_latest_assessment, get_assessment_history,
    calculate_skill_gaps, save_skill_results, get_latest_skill_results,
    get_student_roadmap, toggle_task_completion, get_matched_opportunities
)

def create_app(config_class=None):
    """Application factory for Kaushal Setu."""
    if config_class is None:
        if os.environ.get('FLASK_ENV') == 'production' or os.environ.get('RENDER'):
            config_class = ProductionConfig
        else:
            config_class = DevelopmentConfig

    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database
    init_app(app)
    
    with app.app_context():
        # Ensure database tables exist automatically on startup
        init_db()

    # Context processors to supply global utilities in templates
    @app.context_processor
    def inject_global_data():
        return {
            'current_user': get_current_user(),
            'csrf_token': generate_csrf_token()
        }

    @app.template_filter('date_only')
    def date_only_filter(val):
        if not val:
            return ''
        s = str(val)
        return s[:10]

    # =========================================================================
    # AUTHENTICATION & ENTRY POINT ROUTES
    # =========================================================================

    @app.route('/')
    def index():
        """
        Entry point:
        If authenticated -> redirect to Dashboard.
        If unauthenticated -> redirect to Login window (requirement: first page is login).
        """
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Split-screen Login and Registration page."""
        if 'user_id' in session:
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            validate_csrf()
            action = request.form.get('action', 'login')

            if action == 'login':
                email = request.form.get('email', '').strip()
                password = request.form.get('password', '')
                remember = bool(request.form.get('remember'))

                user, error = authenticate_user(email, password)
                if error:
                    flash(error, 'danger')
                    return render_template('login.html', active_tab='login', email=email)

                login_user(user, remember=remember)
                flash(f"Welcome back, {user['full_name']}!", 'success')
                
                next_url = request.args.get('next')
                if next_url and next_url.startswith('/'):
                    return redirect(next_url)
                return redirect(url_for('dashboard'))

            elif action == 'register':
                full_name = request.form.get('full_name', '').strip()
                email = request.form.get('email', '').strip()
                password = request.form.get('password', '')
                confirm_password = request.form.get('confirm_password', '')
                education_level = request.form.get('education_level', '').strip()
                college_name = request.form.get('college_name', '').strip()

                user_id, errors = register_user(
                    full_name, email, password, confirm_password, education_level, college_name
                )

                if errors:
                    for err in errors:
                        flash(err, 'danger')
                    return render_template(
                        'login.html',
                        active_tab='register',
                        reg_name=full_name,
                        reg_email=email,
                        reg_edu=education_level,
                        reg_college=college_name
                    )

                # Auto login upon successful registration
                user, _ = authenticate_user(email, password)
                login_user(user)
                flash("Account created successfully! Welcome to Kaushal Setu. Let's configure your career target.", 'success')
                return redirect(url_for('profile_setup'))

        active_tab = request.args.get('tab', 'login')
        return render_template('login.html', active_tab=active_tab)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Explicit route pointing to registration tab on login screen."""
        if request.method == 'GET':
            return redirect(url_for('login', tab='register'))
        # If POST submitted to /register, route to login handler
        return login()

    @app.route('/logout')
    def logout():
        """Log out the student and clear session state."""
        logout_user()
        flash("You have been successfully logged out.", "info")
        return redirect(url_for('login'))

    @app.route('/forgot-password', methods=['GET', 'POST'])
    def forgot_password():
        """
        Honest password recovery handler.
        Explains clearly that external SMTP email dispatch is not configured in local demo mode,
        and provides direct local reset instructions.
        """
        if request.method == 'POST':
            validate_csrf()
            email = request.form.get('email', '').strip()
            flash(
                "NOTE (Local Demo Mode): External email delivery is not configured. "
                "For local testing, you can update your password directly from the Settings page once logged in, "
                "or register a new student testing account.",
                "info"
            )
            return redirect(url_for('login'))
        return redirect(url_for('login'))

    # =========================================================================
    # STUDENT PROFILE ROUTES
    # =========================================================================

    @app.route('/profile-setup', methods=['GET', 'POST'])
    @login_required
    def profile_setup():
        """First-time onboarding to configure student career goals."""
        user_id = session['user_id']
        db = get_db()
        
        if request.method == 'POST':
            validate_csrf()
            target_career = request.form.get('target_career', 'Python Developer').strip()
            degree_course = request.form.get('degree_course', '').strip()
            academic_year = request.form.get('academic_year', '3rd Year').strip()
            preferred_location = request.form.get('preferred_location', 'Lucknow / Remote').strip()
            technical_skills = request.form.get('technical_skills', '').strip()
            interests = request.form.get('interests', '').strip()

            db.execute("""
                UPDATE student_profiles
                SET target_career = ?, degree_course = ?, academic_year = ?,
                    preferred_location = ?, technical_skills = ?, interests = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (target_career, degree_course, academic_year, preferred_location, technical_skills, interests, user_id))
            db.commit()

            flash("Profile initialized successfully! Next, take your first diagnostic skill assessment.", "success")
            return redirect(url_for('assessment'))

        profile = db.execute("SELECT * FROM student_profiles WHERE user_id = ?", (user_id,)).fetchone()
        user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return render_template('profile_setup.html', profile=profile, user=user)

    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        """View and edit comprehensive student profile."""
        user_id = session['user_id']
        db = get_db()

        if request.method == 'POST':
            validate_csrf()
            full_name = request.form.get('full_name', '').strip()
            college_name = request.form.get('college_name', '').strip()
            education_level = request.form.get('education_level', '').strip()
            target_career = request.form.get('target_career', 'Python Developer').strip()
            degree_course = request.form.get('degree_course', '').strip()
            academic_year = request.form.get('academic_year', '3rd Year').strip()
            preferred_location = request.form.get('preferred_location', 'Lucknow / Remote').strip()
            technical_skills = request.form.get('technical_skills', '').strip()
            interests = request.form.get('interests', '').strip()
            bio = request.form.get('bio', '').strip()

            if not full_name:
                flash("Full name cannot be empty.", "danger")
            else:
                db.execute("""
                    UPDATE users
                    SET full_name = ?, college_name = ?, education_level = ?
                    WHERE id = ?
                """, (full_name, college_name, education_level, user_id))

                db.execute("""
                    UPDATE student_profiles
                    SET target_career = ?, degree_course = ?, academic_year = ?,
                        preferred_location = ?, technical_skills = ?, interests = ?,
                        bio = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                """, (target_career, degree_course, academic_year, preferred_location, technical_skills, interests, bio, user_id))
                db.commit()

                session['user_name'] = full_name
                flash("Your profile has been updated successfully!", "success")
                return redirect(url_for('profile'))

        user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        profile_row = db.execute("SELECT * FROM student_profiles WHERE user_id = ?", (user_id,)).fetchone()
        return render_template('profile.html', user=user, profile=profile_row)

    # =========================================================================
    # DASHBOARD
    # =========================================================================

    @app.route('/dashboard')
    @login_required
    def dashboard():
        """Student central command center with actionable metrics and real data."""
        user_id = session['user_id']
        db = get_db()

        user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        profile_row = db.execute("SELECT * FROM student_profiles WHERE user_id = ?", (user_id,)).fetchone()
        target_career = profile_row["target_career"] if profile_row and profile_row["target_career"] else "Python Developer"

        # Latest assessment & skill gap breakdown
        latest_assessment = get_latest_assessment(user_id)
        skill_gap_summary = get_latest_skill_results(user_id)
        
        # Roadmap progress
        roadmap_data = get_student_roadmap(user_id, target_career)
        
        # Top 3 matched opportunities
        opportunities = get_matched_opportunities(user_id, career_filter=target_career)[:3]
        
        # Assessment history
        history = get_assessment_history(user_id)

        # Count identified gaps
        high_gaps_count = 0
        if skill_gap_summary:
            high_gaps_count = sum(1 for s in skill_gap_summary["breakdown"] if s["priority"] in ('High', 'Medium'))

        return render_template(
            'dashboard.html',
            user=user,
            profile=profile_row,
            target_career=target_career,
            latest_assessment=latest_assessment,
            skill_gap_summary=skill_gap_summary,
            high_gaps_count=high_gaps_count,
            roadmap_data=roadmap_data,
            top_opportunities=opportunities,
            assessment_history=history
        )

    # =========================================================================
    # SKILL ASSESSMENT MODULE
    # =========================================================================

    @app.route('/assessment', methods=['GET'])
    @login_required
    def assessment():
        """Diagnostic skill assessment screen."""
        user_id = session['user_id']
        db = get_db()
        profile_row = db.execute("SELECT target_career FROM student_profiles WHERE user_id = ?", (user_id,)).fetchone()
        
        # Student can choose or switch career
        career_path = request.args.get('career') or (profile_row["target_career"] if profile_row else "Python Developer")
        questions = get_questions_for_career(career_path)
        
        return render_template(
            'assessment.html',
            career_path=career_path,
            questions=questions,
            total_questions=len(questions)
        )

    @app.route('/assessment/submit', methods=['POST'])
    @login_required
    def submit_assessment():
        """Evaluate submitted diagnostic quiz, store scores, and compute skill gap."""
        validate_csrf()
        user_id = session['user_id']
        career_path = request.form.get('career_path', 'Python Developer')
        questions = get_questions_for_career(career_path)
        
        # Extract answers
        submitted_answers = {}
        for q in questions:
            qid = q["id"]
            if qid in request.form:
                submitted_answers[qid] = int(request.form.get(qid))
                
        # Validate that all questions were answered
        if len(submitted_answers) < len(questions):
            flash(f"Please answer all {len(questions)} questions before submitting.", "warning")
            return redirect(url_for('assessment', career=career_path))
            
        evaluation = evaluate_assessment(career_path, submitted_answers)
        
        # 1. Save assessment header
        assessment_id = save_assessment_record(user_id, career_path, evaluation)
        
        # 2. Extract current skill scores (scaled 0-100)
        current_skill_scores = {k: v["current_score"] for k, v in evaluation["normalized_skills"].items()}
        
        # 3. Compute skill gaps and store
        gap_analysis = calculate_skill_gaps(career_path, current_skill_scores)
        save_skill_results(assessment_id, user_id, gap_analysis)
        
        # 4. Update profile career target if different
        db = get_db()
        db.execute("""
            UPDATE student_profiles 
            SET target_career = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """, (career_path, user_id))
        db.commit()

        flash("Assessment evaluated successfully! Here is your Skill Gap Analysis.", "success")
        return redirect(url_for('skill_gap'))

    # =========================================================================
    # SKILL GAP ANALYSIS
    # =========================================================================

    @app.route('/skill-gap')
    @login_required
    def skill_gap():
        """Rule-based Skill Gap Analysis report with Chart.js visualization."""
        user_id = session['user_id']
        data = get_latest_skill_results(user_id)
        
        if not data:
            flash("You haven't completed an assessment yet. Please take the diagnostic assessment first.", "info")
            return redirect(url_for('assessment'))
            
        return render_template('skill_gap.html', data=data)

    # =========================================================================
    # PERSONALIZED LEARNING ROADMAP
    # =========================================================================

    @app.route('/roadmap')
    @login_required
    def roadmap():
        """30-day structured personalized learning roadmap."""
        user_id = session['user_id']
        roadmap_data = get_student_roadmap(user_id)
        return render_template('roadmap.html', roadmap=roadmap_data)

    @app.route('/roadmap/toggle/<int:task_id>', methods=['POST'])
    @login_required
    def toggle_task(task_id):
        """Toggle completion status of a roadmap task."""
        validate_csrf()
        user_id = session['user_id']
        new_status = toggle_task_completion(user_id, task_id)
        
        # Return JSON if requested via AJAX or redirect back
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
            roadmap_data = get_student_roadmap(user_id)
            return jsonify({
                'success': True,
                'task_id': task_id,
                'is_completed': new_status,
                'completion_percentage': roadmap_data['completion_percentage'],
                'completed_count': roadmap_data['completed_count']
            })
            
        flash("Task progress updated!", "success")
        return redirect(request.referrer or url_for('roadmap'))

    # =========================================================================
    # JOB & INTERNSHIP MATCHING
    # =========================================================================

    @app.route('/opportunities')
    @login_required
    def opportunities():
        """Match student skills with entry-level job and internship opportunities."""
        user_id = session['user_id']
        career_filter = request.args.get('career', 'All')
        type_filter = request.args.get('type', 'All')
        location_filter = request.args.get('location', 'All')
        skill_filter = request.args.get('skill', '')

        listings = get_matched_opportunities(
            user_id,
            career_filter=career_filter,
            type_filter=type_filter,
            location_filter=location_filter,
            skill_filter=skill_filter
        )

        return render_template(
            'opportunities.html',
            opportunities=listings,
            current_career=career_filter,
            current_type=type_filter,
            current_location=location_filter,
            current_skill=skill_filter
        )

    # =========================================================================
    # PROGRESS TRACKER
    # =========================================================================

    @app.route('/progress')
    @login_required
    def progress():
        """Comprehensive learning progress dashboard."""
        user_id = session['user_id']
        roadmap_data = get_student_roadmap(user_id)
        history = get_assessment_history(user_id)
        latest_skill_results = get_latest_skill_results(user_id)
        
        return render_template(
            'progress.html',
            roadmap=roadmap_data,
            history=history,
            latest_skill_results=latest_skill_results
        )

    # =========================================================================
    # SKILL REPORT (PRINTABLE TO PDF)
    # =========================================================================

    @app.route('/report')
    @login_required
    def report():
        """Official formal skill gap and employability report with print-to-PDF formatting."""
        user_id = session['user_id']
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        profile_row = db.execute("SELECT * FROM student_profiles WHERE user_id = ?", (user_id,)).fetchone()
        latest_assessment = get_latest_assessment(user_id)
        skill_data = get_latest_skill_results(user_id)
        roadmap_data = get_student_roadmap(user_id)

        if not latest_assessment or not skill_data:
            flash("Please complete a skill assessment to generate your formal diagnostic report.", "info")
            return redirect(url_for('assessment'))

        return render_template(
            'report.html',
            user=user,
            profile=profile_row,
            assessment=latest_assessment,
            skill_data=skill_data,
            roadmap=roadmap_data
        )

    # =========================================================================
    # SETTINGS
    # =========================================================================

    @app.route('/settings', methods=['GET', 'POST'])
    @login_required
    def settings():
        """Account settings, password updates, and data management."""
        user_id = session['user_id']
        db = get_db()

        if request.method == 'POST':
            validate_csrf()
            action = request.form.get('action')

            if action == 'update_password':
                curr_pwd = request.form.get('current_password', '')
                new_pwd = request.form.get('new_password', '')
                conf_pwd = request.form.get('confirm_new_password', '')

                success, msg = update_user_password(user_id, curr_pwd, new_pwd, conf_pwd)
                flash(msg, 'success' if success else 'danger')
                return redirect(url_for('settings'))

            elif action == 'reset_progress':
                # Reset only roadmap progress for learner restart
                db.execute("DELETE FROM user_task_progress WHERE user_id = ?", (user_id,))
                db.commit()
                flash("Your roadmap learning progress has been reset.", "info")
                return redirect(url_for('settings'))

            elif action == 'reset_assessments':
                # Reset assessment history
                db.execute("DELETE FROM assessments WHERE user_id = ?", (user_id,))
                db.execute("DELETE FROM skill_results WHERE user_id = ?", (user_id,))
                db.commit()
                flash("Your assessment history has been cleared. You can now retake a diagnostic test.", "info")
                return redirect(url_for('settings'))

        user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        profile_row = db.execute("SELECT * FROM student_profiles WHERE user_id = ?", (user_id,)).fetchone()
        return render_template('settings.html', user=user, profile=profile_row)

    # =========================================================================
    # ERROR HANDLERS
    # =========================================================================

    @app.errorhandler(400)
    def bad_request(e):
        return render_template('base.html', error_code=400, error_message=str(e.description or "Bad Request")), 400

    @app.errorhandler(404)
    def not_found(e):
        return render_template('base.html', error_code=404, error_message="Page Not Found"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('base.html', error_code=500, error_message="Internal Server Error"), 500

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config.get('DEBUG', False))

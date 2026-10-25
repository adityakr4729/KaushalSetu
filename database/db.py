import sqlite3
import os
from flask import g, current_app
from pathlib import Path
from database.seed_data import ROADMAP_TASKS, DEMO_OPPORTUNITIES

BASE_DIR = Path(__file__).resolve().parent.parent

def get_db_path():
    """Return database path based on Flask current_app or environment."""
    if current_app:
        return current_app.config.get('DATABASE_PATH')
    return os.environ.get('DATABASE_PATH', str(BASE_DIR / 'kaushal_setu.db'))

def get_db(custom_path=None):
    """Obtain a database connection with sqlite3.Row factory and FKs enabled."""
    db_path = custom_path or get_db_path()
    
    if current_app and not custom_path:
        if 'db' not in g:
            g.db = sqlite3.connect(db_path)
            g.db.row_factory = sqlite3.Row
            g.db.execute("PRAGMA foreign_keys = ON;")
        return g.db
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def close_db(e=None):
    """Flask teardown function to close database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(custom_path=None):
    """Initialize database tables and seed baseline data."""
    conn = get_db(custom_path)
    schema_path = BASE_DIR / 'database' / 'schema.sql'
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    
    # Seed roadmap tasks if empty
    task_count = conn.execute("SELECT COUNT(*) FROM roadmap_tasks").fetchone()[0]
    if task_count == 0:
        for task in ROADMAP_TASKS:
            conn.execute("""
                INSERT INTO roadmap_tasks (
                    career_path, week_number, day_number, title, skill_name,
                    description, estimated_hours, resource_title, resource_url, mini_project
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task["career_path"], task["week_number"], task["day_number"], task["title"],
                task["skill_name"], task["description"], task["estimated_hours"],
                task["resource_title"], task["resource_url"], task["mini_project"]
            ))
            
    # Seed opportunities if empty
    opp_count = conn.execute("SELECT COUNT(*) FROM opportunities").fetchone()[0]
    if opp_count == 0:
        for opp in DEMO_OPPORTUNITIES:
            conn.execute("""
                INSERT INTO opportunities (
                    title, company, opportunity_type, career_path, location,
                    is_remote, required_skills, eligibility, application_url,
                    deadline, source, status, description
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                opp["title"], opp["company"], opp["opportunity_type"], opp["career_path"],
                opp["location"], opp["is_remote"], opp["required_skills"], opp["eligibility"],
                opp["application_url"], opp["deadline"], opp["source"], opp["status"],
                opp["description"]
            ))

    # Seed initial demo student if empty for instant platform demonstration
    user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if user_count == 0:
        from werkzeug.security import generate_password_hash
        pwd_hash = generate_password_hash("Password123")
        cursor = conn.execute("""
            INSERT INTO users (full_name, email, password_hash, education_level, college_name)
            VALUES ('Aditya Sharma', 'student@example.com', ?, 'BCA', 'Institute of Technology')
        """, (pwd_hash,))
        demo_user_id = cursor.lastrowid

        conn.execute("""
            INSERT INTO student_profiles (
                user_id, target_career, degree_course, academic_year, preferred_location,
                technical_skills, interests, bio
            ) VALUES (
                ?, 'Python Developer', 'BCA 5th Semester', '3rd Year', 'Remote / Hybrid',
                'Python, Git, HTML, Basic SQL', 'Backend Development, Automation, API Development',
                'Aspiring software developer preparing for engineering and development roles.'
            )
        """, (demo_user_id,))

        # Seed initial assessment & skill results
        ass_cursor = conn.execute("""
            INSERT INTO assessments (user_id, career_path, total_score, max_possible, readiness_percentage)
            VALUES (?, 'Python Developer', 80.0, 120.0, 68.2)
        """, (demo_user_id,))
        demo_ass_id = ass_cursor.lastrowid

        demo_skills = [
            ("Python Fundamentals", 70.0, 85.0, 15.0, "Medium"),
            ("Data Structures", 50.0, 80.0, 30.0, "High"),
            ("SQL & Databases", 65.0, 75.0, 10.0, "Low"),
            ("Git & GitHub", 70.0, 70.0, 0.0, "Mastered"),
            ("Problem Solving", 60.0, 80.0, 20.0, "Medium"),
            ("Project Experience", 75.0, 75.0, 0.0, "Mastered")
        ]
        for s_name, curr, targ, gap, prio in demo_skills:
            conn.execute("""
                INSERT INTO skill_results (
                    assessment_id, user_id, skill_name, current_score, target_score, gap, priority
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (demo_ass_id, demo_user_id, s_name, curr, targ, gap, prio))

        # Complete first 2 roadmap tasks
        task_rows = conn.execute("""
            SELECT id FROM roadmap_tasks WHERE career_path = 'Python Developer' ORDER BY week_number ASC, day_number ASC LIMIT 2
        """).fetchall()
        for tr in task_rows:
            conn.execute("""
                INSERT INTO user_task_progress (user_id, task_id, is_completed, completed_at)
                VALUES (?, ?, 1, CURRENT_TIMESTAMP)
            """, (demo_user_id, tr["id"]))
            
    conn.commit()
    if not current_app or custom_path:
        conn.close()

def init_app(app):
    """Register database teardown and CLI command with Flask app."""
    app.teardown_appcontext(close_db)
    
    @app.cli.command('init-db')
    def init_db_command():
        """Initialize and seed the database."""
        init_db()
        print("Initialized and seeded the Kaushal Setu database successfully.")

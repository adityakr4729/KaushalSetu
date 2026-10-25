import os
import tempfile
import pytest
from werkzeug.security import check_password_hash
from app import create_app
from config import TestingConfig
from database import init_db, get_db
from services import (
    register_user, authenticate_user, evaluate_assessment,
    calculate_skill_gaps, get_questions_for_career,
    get_student_roadmap, toggle_task_completion,
    get_matched_opportunities
)

@pytest.fixture
def test_app():
    """Create and configure a clean testing app instance with a temporary database."""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)
    
    class LocalTestingConfig(TestingConfig):
        DATABASE_PATH = db_path
        TESTING = True
        SECRET_KEY = 'test-secret-key-kaushal-setu'

    app = create_app(LocalTestingConfig)
    
    with app.app_context():
        init_db(db_path)
        yield app

    # Cleanup temporary test database file
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
    except Exception:
        pass

@pytest.fixture
def client(test_app):
    """A test client for the app."""
    return test_app.test_client()

# =============================================================================
# 1. First Page Must Be Login Window & Route Protection
# =============================================================================

def test_1_root_redirects_to_login(client):
    """Requirement 1: When a visitor opens the website '/', first page must be login."""
    response = client.get('/', follow_redirects=False)
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_8_unauthenticated_protected_routes_redirect(client):
    """Requirement 8: Unauthenticated visitors cannot access private pages."""
    protected_urls = [
        '/dashboard',
        '/profile',
        '/profile-setup',
        '/assessment',
        '/skill-gap',
        '/roadmap',
        '/opportunities',
        '/progress',
        '/report',
        '/settings'
    ]
    for url in protected_urls:
        res = client.get(url, follow_redirects=False)
        assert res.status_code == 302, f"Route {url} did not redirect"
        assert '/login' in res.headers['Location'], f"Route {url} did not redirect to /login"

# =============================================================================
# 2, 3, 4, 5, 6, 7: Authentication & Registration Security
# =============================================================================

def test_2_and_4_register_success_and_password_hashed(test_app):
    """Requirements 2 & 4: User registers successfully and passwords are stored as hashes."""
    with test_app.app_context():
        user_id, errors = register_user(
            full_name="Aditya Sharma",
            email="aditya@example.com",
            password="StrongPassword123",
            confirm_password="StrongPassword123",
            education_level="BCA",
            college_name="Institute of Technology"
        )
        assert errors == []
        assert user_id is not None

        db = get_db()
        row = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        assert row is not None
        assert row['email'] == "aditya@example.com"
        # Never plaintext
        assert row['password_hash'] != "StrongPassword123"
        # Verified hash
        assert check_password_hash(row['password_hash'], "StrongPassword123")

def test_3_duplicate_email_rejected(test_app):
    """Requirement 3: Duplicate email registration is rejected."""
    with test_app.app_context():
        # First registration
        register_user("User One", "dup@test.com", "pass123", "pass123", "BCA")
        # Second registration with identical email
        user_id, errors = register_user("User Two", "dup@test.com", "pass123", "pass123", "BCA")
        assert user_id is None
        assert any("already exists" in err.lower() for err in errors)

def test_5_and_6_login_validation(test_app):
    """Requirements 5 & 6: Correct credentials work, incorrect are rejected."""
    with test_app.app_context():
        register_user("Login Tester", "login@example.com", "secret456", "secret456", "B.Tech")

        # Correct credentials
        user, err = authenticate_user("login@example.com", "secret456")
        assert err is None
        assert user is not None
        assert user['email'] == "login@example.com"

        # Incorrect password
        bad_user, bad_err = authenticate_user("login@example.com", "wrongpass")
        assert bad_user is None
        assert "incorrect password" in bad_err.lower()

        # Non-existent user
        no_user, no_err = authenticate_user("unknown@example.com", "secret456")
        assert no_user is None
        assert "no account found" in no_err.lower()

def test_7_logout_ends_session(client, test_app):
    """Requirement 7: Logout ends the session."""
    with test_app.app_context():
        register_user("Session User", "sess@example.com", "mypass123", "mypass123", "BCA")

    # Login via client session
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['user_name'] = "Session User"

    # Confirm access
    dash_res = client.get('/dashboard')
    assert dash_res.status_code == 200

    # Logout
    logout_res = client.get('/logout', follow_redirects=False)
    assert logout_res.status_code == 302
    assert '/login' in logout_res.headers['Location']

    # Confirm session cleared
    with client.session_transaction() as sess:
        assert 'user_id' not in sess

# =============================================================================
# 9. Student Profile Create & Update
# =============================================================================

def test_9_profile_create_and_update(test_app):
    """Requirement 9: A student can create and update a profile."""
    with test_app.app_context():
        user_id, _ = register_user("Profile Test", "prof@example.com", "pass123", "pass123", "BCA")
        db = get_db()

        # Check default profile auto-created
        profile = db.execute("SELECT * FROM student_profiles WHERE user_id = ?", (user_id,)).fetchone()
        assert profile is not None
        assert profile['target_career'] == 'Python Developer'

        # Update profile
        db.execute("""
            UPDATE student_profiles
            SET target_career = 'Data Analyst', technical_skills = 'Python, SQL, Excel',
                preferred_location = 'Lucknow'
            WHERE user_id = ?
        """, (user_id,))
        db.commit()

        updated = db.execute("SELECT * FROM student_profiles WHERE user_id = ?", (user_id,)).fetchone()
        assert updated['target_career'] == 'Data Analyst'
        assert 'SQL' in updated['technical_skills']
        assert updated['preferred_location'] == 'Lucknow'

# =============================================================================
# 10 & 11: Different Assessment Answers & Skill Gap Math
# =============================================================================

def test_10_different_answers_produce_different_results():
    """Requirement 10: Different assessment answers produce appropriate different results."""
    career = "Python Developer"
    questions = get_questions_for_career(career)
    assert len(questions) >= 10

    # 1. Perfect score answers
    perfect_answers = {}
    for q in questions:
        if q.get("is_experience_scale"):
            perfect_answers[q["id"]] = 3  # Highest experience
        else:
            perfect_answers[q["id"]] = q["correct_index"]

    result_high = evaluate_assessment(career, perfect_answers)

    # 2. Low score answers (all wrong)
    low_answers = {}
    for q in questions:
        if q.get("is_experience_scale"):
            low_answers[q["id"]] = 0  # Lowest
        else:
            wrong_index = (q["correct_index"] + 1) % len(q["options"])
            low_answers[q["id"]] = wrong_index

    result_low = evaluate_assessment(career, low_answers)

    assert result_high["overall_percentage"] > result_low["overall_percentage"]
    assert result_high["overall_percentage"] >= 95.0
    assert result_low["overall_percentage"] <= 25.0

def test_11_skill_gap_calculations_correct():
    """Requirement 11: Skill-gap calculations and readiness formula are strictly correct."""
    career = "Python Developer"
    # Target benchmark for Python Developer:
    # Python Fundamentals: 85.0
    # SQL & Databases: 75.0
    current_scores = {
        "Python Fundamentals": 60.0,
        "SQL & Databases": 80.0,
        "Git & GitHub": 70.0,
        "Data Structures": 40.0,
        "Problem Solving": 80.0,
        "Project Experience": 50.0
    }

    analysis = calculate_skill_gaps(career, current_scores)

    # Find Python Fundamentals gap: Target 85 - Current 60 = 25 (Medium Priority)
    py_breakdown = next(b for b in analysis["breakdown"] if b["skill_name"] == "Python Fundamentals")
    assert py_breakdown["gap"] == 25.0
    assert py_breakdown["priority"] == "Medium"

    # Find SQL gap: Target 75 - Current 80 -> gap = max(0, 75 - 80) = 0 (Mastered)
    sql_breakdown = next(b for b in analysis["breakdown"] if b["skill_name"] == "SQL & Databases")
    assert sql_breakdown["gap"] == 0.0
    assert sql_breakdown["priority"] == "Mastered"

    # Check overall readiness bounds
    assert 0.0 <= analysis["readiness_percentage"] <= 100.0

# =============================================================================
# 12 & 13: Roadmap & Task Completion in Database
# =============================================================================

def test_12_learning_roadmap_matches_career(test_app):
    """Requirement 12: Learning roadmaps match student's career."""
    with test_app.app_context():
        user_id, _ = register_user("Roadmap User", "rd@example.com", "pass123", "pass123", "BCA")

        # Test Python Developer roadmap
        py_roadmap = get_student_roadmap(user_id, "Python Developer")
        assert py_roadmap["career_path"] == "Python Developer"
        assert len(py_roadmap["all_tasks"]) > 0
        assert any("Python" in t["title"] for t in py_roadmap["all_tasks"])

        # Test Data Analyst roadmap
        da_roadmap = get_student_roadmap(user_id, "Data Analyst")
        assert da_roadmap["career_path"] == "Data Analyst"
        assert any("Pandas" in t["title"] or "Data" in t["title"] for t in da_roadmap["all_tasks"])

def test_13_task_completion_saved_in_database(test_app):
    """Requirement 13: Task completion is saved in SQLite and dynamically computed."""
    with test_app.app_context():
        user_id, _ = register_user("Progress Tester", "prog@example.com", "pass123", "pass123", "BCA")
        roadmap = get_student_roadmap(user_id, "Python Developer")
        first_task = roadmap["all_tasks"][0]

        # Initial completion is 0%
        assert roadmap["completion_percentage"] == 0.0

        # Toggle first task
        status = toggle_task_completion(user_id, first_task["id"])
        assert status is True

        # Check refreshed roadmap
        updated_roadmap = get_student_roadmap(user_id, "Python Developer")
        assert updated_roadmap["completed_count"] == 1
        assert updated_roadmap["completion_percentage"] > 0.0
        assert updated_roadmap["all_tasks"][0]["is_completed"] is True

# =============================================================================
# 14: Job Matching & Filters
# =============================================================================

def test_14_job_matching_and_filters(test_app):
    """Requirement 14: Job matching and filters work."""
    with test_app.app_context():
        user_id, _ = register_user("Job Matcher", "job@example.com", "pass123", "pass123", "BCA")
        
        # Test unfiltered opportunities
        all_opps = get_matched_opportunities(user_id)
        assert len(all_opps) > 0
        assert all_opps[0]["match_percentage"] >= 0

        # Test career filter
        py_opps = get_matched_opportunities(user_id, career_filter="Python Developer")
        for o in py_opps:
            assert o["career_path"] == "Python Developer"

        # Test type filter
        internships = get_matched_opportunities(user_id, type_filter="Internship")
        for o in internships:
            assert o["opportunity_type"] == "Internship"

# =============================================================================
# 15 & 16: Reports & User Data Isolation
# =============================================================================

def test_15_and_16_user_data_isolation(test_app):
    """Requirements 15 & 16: A user cannot access or modify another user's records."""
    with test_app.app_context():
        user_a, _ = register_user("Student A", "a@example.com", "pass123", "pass123", "BCA")
        user_b, _ = register_user("Student B", "b@example.com", "pass123", "pass123", "BCA")

        roadmap_a = get_student_roadmap(user_a, "Python Developer")
        task_id = roadmap_a["all_tasks"][0]["id"]

        # Student A marks task as complete
        toggle_task_completion(user_a, task_id, is_completed=True)

        # Student A's progress should be 1
        roadmap_a_new = get_student_roadmap(user_a, "Python Developer")
        assert roadmap_a_new["completed_count"] == 1

        # Student B's progress must strictly remain 0 (Isolation)
        roadmap_b = get_student_roadmap(user_b, "Python Developer")
        assert roadmap_b["completed_count"] == 0

# =============================================================================
# 17 & 18: Full Workflow Navigation & Error Handling
# =============================================================================

def test_17_and_18_full_application_navigation_flow(client, test_app):
    """Requirements 17 & 18: All important buttons, links, and pages load without error."""
    with test_app.app_context():
        user_id, _ = register_user("Full Flow", "flow@example.com", "pass123", "pass123", "BCA")

    # Simulate authenticated session
    with client.session_transaction() as sess:
        sess['user_id'] = user_id
        sess['user_name'] = "Full Flow"

    endpoints = [
        '/dashboard',
        '/profile',
        '/profile-setup',
        '/assessment',
        '/roadmap',
        '/opportunities',
        '/progress',
        '/settings'
    ]

    for ep in endpoints:
        res = client.get(ep)
        assert res.status_code == 200, f"Endpoint {ep} failed with status {res.status_code}"
        assert b"Kaushal Setu" in res.data

def test_19_assessment_submission_and_report_generation(client, test_app):
    """Test full assessment submission flow, gap generation, and printable report viewing."""
    with test_app.app_context():
        user_id, _ = register_user("Assessment Tester", "eval@example.com", "pass123", "pass123", "BCA")

    with client.session_transaction() as sess:
        sess['user_id'] = user_id
        sess['user_name'] = "Assessment Tester"
        sess['csrf_token'] = "test-csrf-token"

    # Fetch assessment page questions
    career = "Python Developer"
    questions = get_questions_for_career(career)
    
    post_data = {
        'csrf_token': 'test-csrf-token',
        'career_path': career
    }
    for q in questions:
        post_data[q['id']] = 2  # choose option index 2

    # Submit assessment
    submit_res = client.post('/assessment/submit', data=post_data, follow_redirects=True)
    assert submit_res.status_code == 200
    assert b"Skill Gap Analysis" in submit_res.data
    assert b"Overall Readiness" in submit_res.data

    # Check report page now loads cleanly with student data
    report_res = client.get('/report')
    assert report_res.status_code == 200
    assert b"Assessment Tester" in report_res.data
    assert b"KAUSHAL SETU" in report_res.data
    assert b"Print / Save as PDF" in report_res.data

def test_20_roadmap_ajax_toggle_and_settings_reset(client, test_app):
    """Test AJAX toggle of task progress and test resets in Settings."""
    with test_app.app_context():
        user_id, _ = register_user("Reset User", "reset@example.com", "pass123", "pass123", "BCA")

    with client.session_transaction() as sess:
        sess['user_id'] = user_id
        sess['user_name'] = "Reset User"
        sess['csrf_token'] = 'test-token'

    # Toggle task via AJAX
    roadmap = get_student_roadmap(user_id, "Python Developer")
    task_id = roadmap['all_tasks'][0]['id']

    ajax_res = client.post(
        f'/roadmap/toggle/{task_id}',
        headers={'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': 'test-token'},
        json={'is_completed': True}
    )
    assert ajax_res.status_code == 200
    data = ajax_res.get_json()
    assert data['success'] is True
    assert data['is_completed'] is True
    assert data['completed_count'] == 1

    # Reset progress in settings
    reset_res = client.post(
        '/settings',
        data={'action': 'reset_progress', 'csrf_token': 'test-token'},
        follow_redirects=True
    )
    assert reset_res.status_code == 200
    assert b"roadmap learning progress has been reset" in reset_res.data

    # Confirm progress reset to 0
    updated_roadmap = get_student_roadmap(user_id, "Python Developer")
    assert updated_roadmap['completed_count'] == 0


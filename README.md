# Kaushal Setu — Bridging the Skills-to-Employment Gap

> **Career Development & Employability Platform**  
> **Tagline:** Assess. Learn. Apply. | *"Your Skills. Your Future."*

---

## 📖 Project Overview

**Kaushal Setu** is an independent full-stack web application developed for college students and graduates to bridge the critical skills-to-employment disconnect. Many students struggle to identify what specific industry competencies they lack for entry-level technology jobs. 

Kaushal Setu solves this with an end-to-end, beginner-friendly pipeline:
1. **Entry Point Authentication**: Professional split-screen login/signup screen with cryptographic password security and complete route protection.
2. **Diagnostic Skill Assessment**: Role-specific multi-domain technical diagnostic assessments for:
   - **Python Developer**
   - **Web Developer**
   - **Data Analyst**
3. **Rule-Based Skill Gap Engine**: Benchmarks the student's assessed proficiency against industry target standards (0–100 scale), calculating exact non-negative deficits:
   $$\text{Gap} = \max(0, \text{Target Score} - \text{Current Score})$$
   $$\text{Readiness Percentage} = \min\left(100, \left(\frac{\sum \text{Current Scores}}{\sum \text{Target Scores}}\right) \times 100\right)$$
4. **Personalized 30-Day Learning Roadmap**: 4 structured weekly milestones tailored to the student's career path and missing skills, with legitimate free resources and hands-on mini-projects.
5. **Skill-Matched Opportunities**: Matches student competencies with curated entry-level jobs, internships, and apprenticeships, highlighting matched skills in green and missing skills in amber.
6. **Student Progress Tracker & Command Dashboard**: Dynamic progress tracking saved in SQLite.
7. **Printable Skill Report**: Formal diagnostic employability report formatted for high-quality browser print-to-PDF.

---

## 💻 Technology Stack

- **Backend**: Python 3.10+ / Python 3.14 with Flask 3.1
- **Database**: SQLite with foreign key enforcement and automated seeding
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6+)
- **UI Framework**: Bootstrap 5.3 + Bootstrap Icons
- **Data Visualizations**: Chart.js 4.4 (Interactive Radar and Bar charts)
- **Security**: Werkzeug PBKDF2 password hashing, session cookies, and CSRF protection
- **Testing**: Pytest automated test suite (16 comprehensive tests)

---

## 📁 Project Folder Structure

```text
Kaushal setu/
│
├── app.py                      # Flask application factory, routes & error handlers
├── config.py                   # Configuration classes (Development, Testing)
├── requirements.txt            # Python dependencies (Flask, Werkzeug, python-dotenv, gunicorn, pytest)
├── Procfile                    # Web service process configuration for cloud deployment (Render)
├── README.md                   # Complete documentation & project guide
├── .env.example                # Sample environment file template
├── .gitignore                  # Git exclusions for venv, SQLite, and caches
├── kaushal_setu.db             # Auto-generated SQLite database
│
├── database/                   # Database layer
│   ├── __init__.py             # Database exports
│   ├── schema.sql              # Relational schema (users, profiles, assessments, roadmaps, etc.)
│   ├── db.py                   # Connection management & auto-seed runner
│   └── seed_data.py            # 24 structured roadmap milestones & 8 demo vacancies
│
├── services/                   # Business logic and algorithms
│   ├── __init__.py             # Service layer exports
│   ├── auth_service.py         # Werkzeug hashing, validation, session & CSRF logic
│   ├── assessment_service.py   # Diagnostic questions & scoring engine
│   ├── skill_gap_service.py    # Rule-based gap & readiness calculation engine
│   ├── roadmap_service.py      # 30-day curriculum & user progress tracking
│   └── job_match_service.py    # Opportunity matching & skill overlap engine
│
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css           # Custom dark navy & teal styling, print stylesheet
│   └── js/
│       ├── main.js             # Password toggle, form validation, AJAX roadmap toggle
│       └── charts.js           # Chart.js radar & bar chart rendering
│
├── templates/                  # Jinja2 HTML5 templates
│   ├── base.html               # Base layout, responsive sidebar & top navbar
│   ├── login.html              # Split-screen login & registration window (entry screen)
│   ├── profile_setup.html      # First-time onboarding career wizard
│   ├── dashboard.html          # Student command center with metrics & radar snapshot
│   ├── profile.html            # Profile view & editing form
│   ├── assessment.html         # Interactive 12-question diagnostic test
│   ├── skill_gap.html          # Comprehensive gap report with dual charts
│   ├── roadmap.html            # 30-day 4-week structured roadmap with checkboxes
│   ├── opportunities.html      # Opportunity matching with skill pills & filters
│   ├── progress.html           # Progress metrics & full curriculum inventory
│   ├── report.html             # Formal printable report (Save as PDF)
│   └── settings.html           # Password updates & account details
│
└── tests/                      # Automated test suite
    ├── __init__.py
    └── test_app.py             # 16 unit & integration tests covering all requirements
```

---

## 🚀 Windows Setup and Running Instructions

The application runs locally on Windows without requiring any external paid APIs or complex cloud tools.

### Step 1: Open the Project in VS Code or Terminal
Open **Command Prompt (`cmd.exe`)** or **PowerShell**, then navigate to the project directory:
```powershell
cd "c:\Users\adity\OneDrive\Desktop\Kaushal setu"
```

### Step 2: Create and Activate Virtual Environment (Optional but Recommended)

**Using Windows PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If PowerShell displays a script execution policy error, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and then run the activation command again).*

**Using Windows Command Prompt (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### Step 3: Install Required Packages
```powershell
python -m pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy `.env.example` to `.env` (a safe default is already included in `config.py`):
```powershell
copy .env.example .env
```

### Step 5: Start the Flask Development Server
```powershell
python app.py
```

You will see output similar to:
```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Step 6: Open the Website in Your Browser
Visit:
```text
http://127.0.0.1:5000
```
When you open this URL, **the first page that appears is the professional split-screen login/signup screen**.

---

## 🌐 Cloud Deployment (Render)

Kaushal Setu is configured for 1-click deployment on [Render](https://render.com) as a Python Web Service:

- **Repository:** Connect your GitHub repository (`https://github.com/adityakr4729/KaushalSetu`)
- **Environment:** `Python 3`
- **Region:** Any (e.g., Singapore or Oregon)
- **Branch:** `main`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

*(The included `Procfile` and `requirements.txt` pre-configure the Gunicorn WSGI production server, automatic SQLite database initialization, and dynamic `$PORT` binding).*


---

## 🔑 Demo Login Credentials

You can test the platform using the pre-seeded student account:
- **Email:** `student@example.com`
- **Password:** `Password123`
*(Or click the **"Fill Demo Student Account"** button on the login screen for instant 1-click credentials).*

Alternatively, click **"Create Account"** to register a brand-new student account and experience the full onboarding and assessment wizard from scratch.

---

## 🧪 Running Automated Tests

To execute the automated test suite verifying all requirements:
```powershell
python -m pytest -v
```

All 16 tests will execute and pass:
```text
tests/test_app.py::test_1_root_redirects_to_login PASSED
tests/test_app.py::test_8_unauthenticated_protected_routes_redirect PASSED
tests/test_app.py::test_2_and_4_register_success_and_password_hashed PASSED
tests/test_app.py::test_3_duplicate_email_rejected PASSED
tests/test_app.py::test_5_and_6_login_validation PASSED
tests/test_app.py::test_7_logout_ends_session PASSED
tests/test_app.py::test_9_profile_create_and_update PASSED
tests/test_app.py::test_10_different_answers_produce_different_results PASSED
tests/test_app.py::test_11_skill_gap_calculations_correct PASSED
tests/test_app.py::test_12_learning_roadmap_matches_career PASSED
tests/test_app.py::test_13_task_completion_saved_in_database PASSED
tests/test_app.py::test_14_job_matching_and_filters PASSED
tests/test_app.py::test_15_and_16_user_data_isolation PASSED
tests/test_app.py::test_17_and_18_full_application_navigation_flow PASSED
tests/test_app.py::test_19_assessment_submission_and_report_generation PASSED
tests/test_app.py::test_20_roadmap_ajax_toggle_and_settings_reset PASSED

============================= 16 passed =============================
```

---

## 🔒 Security & Safe Coding Features

- **Password Hashing**: Uses Werkzeug's PBKDF2 implementation with SHA-256 salt. Plaintext passwords are never saved.
- **Route Authorization**: All private pages are protected by a `@login_required` decorator. Unauthenticated access attempts redirect to `/login`.
- **SQL Injection Prevention**: All SQLite queries use parameterized placeholders (`?`).
- **CSRF Defense**: Session-backed cryptographic tokens validate all state-changing POST requests.
- **Data Isolation**: Database updates and queries strictly filter by authenticated `session['user_id']`. Student A cannot view or modify Student B's progress.
- **Local Environment Notice**: Designed for local development. For live production deployment, configure HTTPS (`SESSION_COOKIE_SECURE=True`) and load secret keys from an external vault.

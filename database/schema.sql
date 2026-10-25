-- Kaushal Setu Database Schema
-- Career Development & Employability Platform

PRAGMA foreign_keys = ON;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    education_level TEXT NOT NULL,
    college_name TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Student Profiles Table
CREATE TABLE IF NOT EXISTS student_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    target_career TEXT DEFAULT 'Python Developer',
    preferred_location TEXT DEFAULT 'Lucknow / Remote',
    degree_course TEXT DEFAULT 'BCA / B.Tech',
    academic_year TEXT DEFAULT '3rd Year',
    technical_skills TEXT DEFAULT '',
    interests TEXT DEFAULT '',
    bio TEXT DEFAULT '',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Assessments History Table
CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    career_path TEXT NOT NULL,
    total_score REAL NOT NULL,
    max_possible REAL NOT NULL,
    readiness_percentage REAL NOT NULL,
    taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Skill Breakdown Results per Assessment
CREATE TABLE IF NOT EXISTS skill_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    skill_name TEXT NOT NULL,
    current_score REAL NOT NULL,
    target_score REAL NOT NULL,
    gap REAL NOT NULL,
    priority TEXT NOT NULL, -- 'High', 'Medium', 'Low', 'Mastered'
    FOREIGN KEY (assessment_id) REFERENCES assessments (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Master Roadmap Tasks
CREATE TABLE IF NOT EXISTS roadmap_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    career_path TEXT NOT NULL,
    week_number INTEGER NOT NULL,
    day_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    skill_name TEXT NOT NULL,
    description TEXT NOT NULL,
    estimated_hours REAL NOT NULL,
    resource_title TEXT NOT NULL,
    resource_url TEXT NOT NULL,
    mini_project TEXT NOT NULL
);

-- Student Roadmap Task Progress
CREATE TABLE IF NOT EXISTS user_task_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL,
    is_completed INTEGER DEFAULT 0, -- 0 = false, 1 = true
    completed_at TIMESTAMP,
    UNIQUE(user_id, task_id),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES roadmap_tasks (id) ON DELETE CASCADE
);

-- Job & Internship Opportunities (Curated Sample Dataset)
CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    opportunity_type TEXT NOT NULL, -- 'Full-time Job', 'Internship', 'Apprenticeship'
    career_path TEXT NOT NULL,      -- 'Python Developer', 'Web Developer', 'Data Analyst'
    location TEXT NOT NULL,
    is_remote INTEGER DEFAULT 0,
    required_skills TEXT NOT NULL,  -- Comma-separated
    eligibility TEXT NOT NULL,
    application_url TEXT NOT NULL,
    deadline TEXT NOT NULL,
    source TEXT NOT NULL,           -- e.g., 'National Career Service (NCS) Mock Index'
    status TEXT DEFAULT 'DEMO DATA — NOT A VERIFIED LIVE VACANCY',
    description TEXT NOT NULL
);

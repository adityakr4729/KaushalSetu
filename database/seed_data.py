"""
Seed data for Kaushal Setu.
Provides:
1. 30-day structured roadmap tasks across 4 weekly stages for:
   - Python Developer
   - Web Developer
   - Data Analyst
2. Curated demo opportunities marked as 'DEMO DATA — NOT A VERIFIED LIVE VACANCY'
"""

ROADMAP_TASKS = [
    # ==========================================
    # Python Developer Roadmap (Weeks 1 to 4)
    # ==========================================
    {
        "career_path": "Python Developer",
        "week_number": 1,
        "day_number": 1,
        "title": "Python Syntax, Variables & Control Flow",
        "skill_name": "Python Fundamentals",
        "description": "Master data types, conditional branching (if/elif/else), loops (for, while), and input handling.",
        "estimated_hours": 3.0,
        "resource_title": "Python.org Official Tutorial: Informal Introduction",
        "resource_url": "https://docs.python.org/3/tutorial/introduction.html",
        "mini_project": "Build an interactive CLI Grade & CGPA Calculator."
    },
    {
        "career_path": "Python Developer",
        "week_number": 1,
        "day_number": 2,
        "title": "Data Structures: Lists, Dictionaries, Tuples & Sets",
        "skill_name": "Data Structures",
        "description": "Understand indexing, slicing, dictionary key-value lookups, list comprehensions, and set operations.",
        "estimated_hours": 3.5,
        "resource_title": "Python.org: Data Structures Deep Dive",
        "resource_url": "https://docs.python.org/3/tutorial/datastructures.html",
        "mini_project": "Develop a Contact Book CLI storing data with nested dictionaries."
    },
    {
        "career_path": "Python Developer",
        "week_number": 1,
        "day_number": 3,
        "title": "Functions, Scope, Modules & Error Handling",
        "skill_name": "Python Fundamentals",
        "description": "Learn parameter passing (*args, **kwargs), return values, try-except-finally blocks, and custom exceptions.",
        "estimated_hours": 3.0,
        "resource_title": "W3Schools: Python Functions & Try-Except",
        "resource_url": "https://www.w3schools.com/python/python_functions.asp",
        "mini_project": "Build a robust Bank Account Simulator with custom overdraft exceptions."
    },
    {
        "career_path": "Python Developer",
        "week_number": 2,
        "day_number": 1,
        "title": "Object-Oriented Programming (OOP) in Python",
        "skill_name": "Object-Oriented Programming",
        "description": "Define classes, objects, constructors (__init__), inheritance, encapsulation, and method overriding.",
        "estimated_hours": 4.0,
        "resource_title": "Real Python: OOP in Python",
        "resource_url": "https://realpython.com/python3-object-oriented-programming/",
        "mini_project": "Design a Digital Campus Library Management System using OOP classes."
    },
    {
        "career_path": "Python Developer",
        "week_number": 2,
        "day_number": 2,
        "title": "Relational Databases & SQL with SQLite3",
        "skill_name": "SQL & Databases",
        "description": "Write SQL queries: SELECT, INSERT, UPDATE, DELETE, JOINs, aggregations, and connect via Python sqlite3.",
        "estimated_hours": 4.0,
        "resource_title": "W3Schools: SQL Tutorial & Joins",
        "resource_url": "https://www.w3schools.com/sql/",
        "mini_project": "Write a Python script managing a Student Database with parameterized SQL."
    },
    {
        "career_path": "Python Developer",
        "week_number": 3,
        "day_number": 1,
        "title": "Git Version Control & GitHub Essentials",
        "skill_name": "Git & GitHub",
        "description": "Master git init, commit, branching, merging, remote repositories, push/pull, and resolving merge conflicts.",
        "estimated_hours": 3.0,
        "resource_title": "Git-SCM Official Documentation Book",
        "resource_url": "https://git-scm.com/doc",
        "mini_project": "Publish a repository on GitHub with clean commit history, branches, and README."
    },
    {
        "career_path": "Python Developer",
        "week_number": 3,
        "day_number": 2,
        "title": "Backend Web Basics with Flask",
        "skill_name": "Flask & Web APIs",
        "description": "Create routes, render dynamic Jinja templates, process POST requests, and handle sessions.",
        "estimated_hours": 4.5,
        "resource_title": "Flask Official Documentation: Quickstart",
        "resource_url": "https://flask.palletsprojects.com/en/latest/quickstart/",
        "mini_project": "Build a Todo Web Application with SQLite backend."
    },
    {
        "career_path": "Python Developer",
        "week_number": 4,
        "day_number": 1,
        "title": "Capstone: Full-Stack Python Application",
        "skill_name": "Full Project Development",
        "description": "Integrate SQLite, Flask, Jinja templates, authentication, and form validation into a showcase project.",
        "estimated_hours": 6.0,
        "resource_title": "Flask Mega-Tutorial by Miguel Grinberg",
        "resource_url": "https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world",
        "mini_project": "Develop a Student Project Portal with search and role management."
    },

    # ==========================================
    # Web Developer Roadmap (Weeks 1 to 4)
    # ==========================================
    {
        "career_path": "Web Developer",
        "week_number": 1,
        "day_number": 1,
        "title": "Semantic HTML5 & Accessible Web Forms",
        "skill_name": "HTML5",
        "description": "Learn semantic elements (header, nav, main, section, footer), form inputs, labels, and accessibility basics.",
        "estimated_hours": 3.0,
        "resource_title": "MDN Web Docs: HTML Semantics",
        "resource_url": "https://developer.mozilla.org/en-US/docs/Learn/HTML",
        "mini_project": "Code a semantic multi-field job registration form with native validation."
    },
    {
        "career_path": "Web Developer",
        "week_number": 1,
        "day_number": 2,
        "title": "Modern CSS3: Flexbox, Grid & Media Queries",
        "skill_name": "CSS3 & Responsive Design",
        "description": "Master CSS Box Model, Flexbox alignment, CSS Grid layouts, and responsive breakpoints for mobile/desktop.",
        "estimated_hours": 4.0,
        "resource_title": "MDN Web Docs: CSS Layout",
        "resource_url": "https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout",
        "mini_project": "Build a responsive college event showcase landing page."
    },
    {
        "career_path": "Web Developer",
        "week_number": 2,
        "day_number": 1,
        "title": "JavaScript Fundamentals & DOM Manipulation",
        "skill_name": "JavaScript",
        "description": "Variables (let/const), arrow functions, array methods (map, filter), document.querySelector, and event listeners.",
        "estimated_hours": 4.0,
        "resource_title": "javascript.info: The Modern JavaScript Tutorial",
        "resource_url": "https://javascript.info/",
        "mini_project": "Create an interactive Dynamic Quiz Card UI with real-time score counter."
    },
    {
        "career_path": "Web Developer",
        "week_number": 2,
        "day_number": 2,
        "title": "Asynchronous JS, Fetch API & JSON Handling",
        "skill_name": "JavaScript",
        "description": "Learn Promises, async/await syntax, fetching remote JSON APIs, and handling loading/error states.",
        "estimated_hours": 3.5,
        "resource_title": "MDN Web Docs: Working with JSON & Fetch",
        "resource_url": "https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON",
        "mini_project": "Build a live Weather or GitHub User Profile Search widget."
    },
    {
        "career_path": "Web Developer",
        "week_number": 3,
        "day_number": 1,
        "title": "Bootstrap 5 Components & Clean UI Design",
        "skill_name": "UI Frameworks",
        "description": "Use Bootstrap container, grid columns, cards, modal dialogs, navbars, and badge components.",
        "estimated_hours": 3.0,
        "resource_title": "Bootstrap 5 Official Documentation",
        "resource_url": "https://getbootstrap.com/docs/5.3/getting-started/introduction/",
        "mini_project": "Redesign a student dashboard with dark navy/teal color theme."
    },
    {
        "career_path": "Web Developer",
        "week_number": 3,
        "day_number": 2,
        "title": "Backend Integration with Python Flask",
        "skill_name": "Python/Flask Backend",
        "description": "Connect frontend HTML templates to Flask routes, handle form submission POST requests, and render dynamic data.",
        "estimated_hours": 4.0,
        "resource_title": "Flask Quickstart & Jinja Templating",
        "resource_url": "https://flask.palletsprojects.com/en/latest/tutorial/",
        "mini_project": "Develop a feedback collection web app storing entries in SQLite."
    },
    {
        "career_path": "Web Developer",
        "week_number": 4,
        "day_number": 1,
        "title": "Git, GitHub & Web Deployment Best Practices",
        "skill_name": "Git & Deployment",
        "description": "Practice git workflow, creating feature branches, pull requests, and preparing production-ready static assets.",
        "estimated_hours": 3.5,
        "resource_title": "GitHub Skills: Introduction to GitHub",
        "resource_url": "https://skills.github.com/",
        "mini_project": "Publish your portfolio repository with GitHub Pages / local deployment instructions."
    },
    {
        "career_path": "Web Developer",
        "week_number": 4,
        "day_number": 2,
        "title": "Capstone: Complete Responsive Web Portal",
        "skill_name": "Full Project Development",
        "description": "Build an end-to-end responsive portal featuring authentication, dashboard metrics, and interactive charts.",
        "estimated_hours": 6.0,
        "resource_title": "MDN Web Docs: Complete Web Development Path",
        "resource_url": "https://developer.mozilla.org/en-US/docs/Learn",
        "mini_project": "Build and document a Campus Placement & Skill Tracking Portal."
    },

    # ==========================================
    # Data Analyst Roadmap (Weeks 1 to 4)
    # ==========================================
    {
        "career_path": "Data Analyst",
        "week_number": 1,
        "day_number": 1,
        "title": "Python for Data Analysis: Pandas & NumPy Basics",
        "skill_name": "Python for Data",
        "description": "Learn NumPy arrays, Pandas DataFrames, Series, reading CSV/Excel files, and handling missing data (NaN).",
        "estimated_hours": 4.0,
        "resource_title": "Kaggle Learn: Pandas Micro-Course",
        "resource_url": "https://www.kaggle.com/learn/pandas",
        "mini_project": "Clean and inspect a 500-row student grades dataset using Pandas."
    },
    {
        "career_path": "Data Analyst",
        "week_number": 1,
        "day_number": 2,
        "title": "Data Manipulation, Grouping & Filtering",
        "skill_name": "Python for Data",
        "description": "Master df.groupby(), agg(), pivot tables, boolean indexing, and string operations in Pandas.",
        "estimated_hours": 3.5,
        "resource_title": "Pandas Official Documentation: User Guide",
        "resource_url": "https://pandas.pydata.org/docs/user_guide/index.html",
        "mini_project": "Generate an automated summary report of sales per region and product."
    },
    {
        "career_path": "Data Analyst",
        "week_number": 2,
        "day_number": 1,
        "title": "SQL Queries, Aggregations & Multi-Table Joins",
        "skill_name": "SQL & Databases",
        "description": "Write advanced SQL: GROUP BY, HAVING, INNER/LEFT JOIN, subqueries, and window function concepts.",
        "estimated_hours": 4.5,
        "resource_title": "W3Schools SQL Tutorial & Mode Analytics SQL Guide",
        "resource_url": "https://www.w3schools.com/sql/",
        "mini_project": "Query an eCommerce database to find top 5 customer cohorts and churn rates."
    },
    {
        "career_path": "Data Analyst",
        "week_number": 2,
        "day_number": 2,
        "title": "Advanced Spreadsheets: Pivot Tables & Lookup Formulas",
        "skill_name": "Excel / Spreadsheets",
        "description": "Formulas: XLOOKUP, INDEX/MATCH, SUMIFS, COUNTIFS, conditional formatting, and interactive Pivot Charts.",
        "estimated_hours": 3.5,
        "resource_title": "Microsoft Support: Excel Formulas & Functions Guide",
        "resource_url": "https://support.microsoft.com/en-us/excel",
        "mini_project": "Build an Executive Financial KPI Dashboard spreadsheet with slicers."
    },
    {
        "career_path": "Data Analyst",
        "week_number": 3,
        "day_number": 1,
        "title": "Data Visualization Principles & Chart.js / Matplotlib",
        "skill_name": "Data Visualization",
        "description": "Understand chart choices (bar, line, scatter, radar), color contrast, labeling, and web dashboard charts.",
        "estimated_hours": 4.0,
        "resource_title": "Chart.js Official Documentation & Storytelling with Data",
        "resource_url": "https://www.chartjs.org/docs/latest/",
        "mini_project": "Create interactive web charts displaying employment trends across 5 sectors."
    },
    {
        "career_path": "Data Analyst",
        "week_number": 3,
        "day_number": 2,
        "title": "Practical Business Statistics for Analysts",
        "skill_name": "Statistics Basics",
        "description": "Central tendency (mean, median, mode), variance, standard deviation, normal distribution, and correlation vs causation.",
        "estimated_hours": 3.5,
        "resource_title": "Khan Academy: College Statistics Course",
        "resource_url": "https://www.khanacademy.org/math/statistics-probability",
        "mini_project": "Calculate statistical summary and correlation matrix for student exam scores."
    },
    {
        "career_path": "Data Analyst",
        "week_number": 4,
        "day_number": 1,
        "title": "Data Cleaning, Transformation & Quality Checks",
        "skill_name": "Python for Data",
        "description": "Identify outliers, impute missing values, convert data types, and validate data integrity before reporting.",
        "estimated_hours": 4.0,
        "resource_title": "Kaggle Learn: Data Cleaning",
        "resource_url": "https://www.kaggle.com/learn/data-cleaning",
        "mini_project": "Build an automated data validation pipeline that flags corrupted rows."
    },
    {
        "career_path": "Data Analyst",
        "week_number": 4,
        "day_number": 2,
        "title": "Capstone: End-to-End Business Intelligence Report",
        "skill_name": "Full Project Development",
        "description": "Clean messy real-world data, perform exploratory data analysis (EDA), and craft an actionable visual insights report.",
        "estimated_hours": 6.0,
        "resource_title": "Kaggle Learn: Intro to Machine Learning & Analytics",
        "resource_url": "https://www.kaggle.com/learn",
        "mini_project": "Produce an Employability Gap Analysis Report for UP Higher Education colleges."
    }
]

DEMO_OPPORTUNITIES = [
    {
        "title": "Junior Python Developer",
        "company": "TechVantage Software Labs",
        "opportunity_type": "Full-time Job",
        "career_path": "Python Developer",
        "location": "Lucknow / Hybrid",
        "is_remote": 0,
        "required_skills": "Python, SQL, Git, Problem Solving, Data Structures",
        "eligibility": "BCA / B.Tech / MCA (Final Year or Recent Graduate with 60%+)",
        "application_url": "https://www.ncs.gov.in/",
        "deadline": "2026-11-30",
        "source": "National Career Service (NCS Mock Index)",
        "status": "DEMO DATA — NOT A VERIFIED LIVE VACANCY",
        "description": "Seeking an enthusiastic Junior Python Developer to assist in building backend APIs, writing automated tests, and maintaining database integrations."
    },
    {
        "title": "Backend Engineering Intern",
        "company": "CodeCraft Solutions India",
        "opportunity_type": "Internship",
        "career_path": "Python Developer",
        "location": "Remote / Bengaluru",
        "is_remote": 1,
        "required_skills": "Python, Flask, SQL, Git, REST APIs",
        "eligibility": "Pre-final or Final Year Degree in CS/IT or related field",
        "application_url": "https://www.ncs.gov.in/",
        "deadline": "2026-11-15",
        "source": "University Placement Cell Listings",
        "status": "DEMO DATA — NOT A VERIFIED LIVE VACANCY",
        "description": "3-month stipend internship working on Flask microservices, database schemas, and unit testing for enterprise SaaS tools."
    },
    {
        "title": "Junior Web Developer",
        "company": "NextGen Infotech Pvt Ltd",
        "opportunity_type": "Full-time Job",
        "career_path": "Web Developer",
        "location": "Lucknow, UP",
        "is_remote": 0,
        "required_skills": "HTML, CSS, JavaScript, Bootstrap, Git, Flask",
        "eligibility": "Graduates in BCA, B.Sc (IT), B.Tech with responsive web portfolio",
        "application_url": "https://www.ncs.gov.in/",
        "deadline": "2026-12-05",
        "source": "UP Skill Development Mission (UPSDM Demo Index)",
        "status": "DEMO DATA — NOT A VERIFIED LIVE VACANCY",
        "description": "Join our web applications team to build responsive interfaces, integrate REST endpoints, and implement accessible UI components."
    },
    {
        "title": "Frontend Web Development Intern",
        "company": "ShikshaTech Innovations",
        "opportunity_type": "Internship",
        "career_path": "Web Developer",
        "location": "Remote",
        "is_remote": 1,
        "required_skills": "HTML, CSS, JavaScript, Bootstrap, Git",
        "eligibility": "Enrolled in 2nd/3rd/4th year college programs",
        "application_url": "https://www.ncs.gov.in/",
        "deadline": "2026-11-20",
        "source": "AICTE Internship Mock Directory",
        "status": "DEMO DATA — NOT A VERIFIED LIVE VACANCY",
        "description": "Hands-on internship designing student learning dashboards, optimizing mobile layouts, and writing clean modular JavaScript."
    },
    {
        "title": "Web Development Apprentice",
        "company": "Apex Digital Labs",
        "opportunity_type": "Apprenticeship",
        "career_path": "Web Developer",
        "location": "Kanpur / Lucknow",
        "is_remote": 0,
        "required_skills": "HTML, CSS, JavaScript, Git",
        "eligibility": "Diploma / Degree in IT/CS or self-taught web learners",
        "application_url": "https://www.ncs.gov.in/",
        "deadline": "2026-12-15",
        "source": "National Apprenticeship Promotion Scheme (NAPS Demo)",
        "status": "DEMO DATA — NOT A VERIFIED LIVE VACANCY",
        "description": "1-year structured apprenticeship program with dedicated mentorship, live client tickets, and stipend."
    },
    {
        "title": "Graduate Data Analyst Trainee",
        "company": "FinMetrics Analytics & Research",
        "opportunity_type": "Full-time Job",
        "career_path": "Data Analyst",
        "location": "Noida / Delhi NCR",
        "is_remote": 0,
        "required_skills": "Python, SQL, Excel, Data Visualization, Statistics",
        "eligibility": "BCA / B.Sc / B.Tech / B.Com with quantitative background",
        "application_url": "https://www.ncs.gov.in/",
        "deadline": "2026-11-25",
        "source": "National Career Service (NCS Mock Index)",
        "status": "DEMO DATA — NOT A VERIFIED LIVE VACANCY",
        "description": "Analyze financial transaction datasets, build executive dashboards in Excel and Python, and extract actionable business insights."
    },
    {
        "title": "Business Intelligence & Data Analyst Intern",
        "company": "UP Data Insights Collaborative",
        "opportunity_type": "Internship",
        "career_path": "Data Analyst",
        "location": "Lucknow / Remote",
        "is_remote": 1,
        "required_skills": "SQL, Excel, Data Visualization, Python",
        "eligibility": "College students with strong interest in business analytics & spreadsheets",
        "application_url": "https://www.ncs.gov.in/",
        "deadline": "2026-11-18",
        "source": "University Placement Cell Listings",
        "status": "DEMO DATA — NOT A VERIFIED LIVE VACANCY",
        "description": "Support regional data aggregation, clean survey datasets, and prepare weekly visualization charts for senior leadership."
    },
    {
        "title": "Junior Python Automation Engineer",
        "company": "AuraSys Cloud Technologies",
        "opportunity_type": "Full-time Job",
        "career_path": "Python Developer",
        "location": "Remote",
        "is_remote": 1,
        "required_skills": "Python, Git, Problem Solving, SQL",
        "eligibility": "Freshers with demonstrable Python scripts and problem solving skills",
        "application_url": "https://www.ncs.gov.in/",
        "deadline": "2026-12-10",
        "source": "National Career Service (NCS Mock Index)",
        "status": "DEMO DATA — NOT A VERIFIED LIVE VACANCY",
        "description": "Automate recurring backend maintenance tasks, schedule monitoring scripts, and write clear technical documentation."
    }
]

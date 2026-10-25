"""
Skill Assessment Service for Kaushal Setu.
Provides:
- Curated diagnostic questions for Python Developer, Web Developer, and Data Analyst
- Answer validation and dynamic scoring algorithms
- Assessment history persistence
"""

from database.db import get_db

ASSESSMENT_QUESTIONS = {
    "Python Developer": [
        {
            "id": "py_1",
            "category": "Python Fundamentals",
            "skill_key": "Python Fundamentals",
            "question": "In Python, which of the following data structures is mutable?",
            "options": [
                "Tuple (e.g., (1, 2, 3))",
                "String (e.g., 'Kaushal Setu')",
                "List (e.g., [1, 2, 3])",
                "FrozenSet (e.g., frozenset([1, 2]))"
            ],
            "correct_index": 2,
            "explanation": "Lists are mutable in Python; their elements can be appended, modified, or removed in place without creating a new object."
        },
        {
            "id": "py_2",
            "category": "Python Fundamentals",
            "skill_key": "Python Fundamentals",
            "question": "What is the expected output of: print(type([x for x in range(5) if x % 2 == 0]))?",
            "options": [
                "<class 'generator'>",
                "<class 'list'>",
                "<class 'tuple'>",
                "<class 'filter'>"
            ],
            "correct_index": 1,
            "explanation": "Square brackets [ ... ] denote a list comprehension, which constructs and returns a list instance."
        },
        {
            "id": "py_3",
            "category": "Functions & Data Structures",
            "skill_key": "Data Structures",
            "question": "What is the average time complexity for searching an element in a Python dictionary by key?",
            "options": [
                "O(n) linear time",
                "O(log n) logarithmic time",
                "O(1) constant time",
                "O(n^2) quadratic time"
            ],
            "correct_index": 2,
            "explanation": "Python dictionaries are implemented using hash tables, giving average-case key lookups O(1) constant time."
        },
        {
            "id": "py_4",
            "category": "Functions & Data Structures",
            "skill_key": "Data Structures",
            "question": "In Python object-oriented programming, what is the role of the '__init__' method?",
            "options": [
                "It serves as the class constructor/initializer called when a new instance is created.",
                "It deletes an instance and frees memory automatically.",
                "It converts any class instance to a JSON string representation.",
                "It imports external Python packages into the class scope."
            ],
            "correct_index": 0,
            "explanation": "'__init__' is the initializer method executed automatically when an object of a class is instantiated."
        },
        {
            "id": "py_5",
            "category": "SQL & Databases",
            "skill_key": "SQL & Databases",
            "question": "Which SQL clause is used to filter records after an aggregation using GROUP BY?",
            "options": [
                "WHERE",
                "HAVING",
                "FILTER BY",
                "ORDER BY"
            ],
            "correct_index": 1,
            "explanation": "HAVING filters aggregated groups (after GROUP BY), whereas WHERE filters individual rows before aggregation."
        },
        {
            "id": "py_6",
            "category": "SQL & Databases",
            "skill_key": "SQL & Databases",
            "question": "Why should developers use parameterized queries (e.g., db.execute('SELECT * FROM users WHERE id = ?', (user_id,)))?",
            "options": [
                "To speed up CSS rendering on the client side",
                "To prevent SQL Injection vulnerabilities and safely escape input",
                "To automatically compress SQLite databases to zip files",
                "To convert SQL rows into XML files"
            ],
            "correct_index": 1,
            "explanation": "Parameterized queries keep SQL code separate from user-supplied parameters, preventing SQL injection attacks."
        },
        {
            "id": "py_7",
            "category": "Git & GitHub",
            "skill_key": "Git & GitHub",
            "question": "Which command sequence creates a new branch named 'feature-auth' and immediately switches to it in Git?",
            "options": [
                "git branch -d feature-auth",
                "git checkout -b feature-auth (or git switch -c feature-auth)",
                "git merge feature-auth",
                "git clone feature-auth"
            ],
            "correct_index": 1,
            "explanation": "'git checkout -b <name>' or 'git switch -c <name>' creates a new branch and switches your HEAD to it."
        },
        {
            "id": "py_8",
            "category": "Git & GitHub",
            "skill_key": "Git & GitHub",
            "question": "What is the primary purpose of a Git Pull Request (PR)?",
            "options": [
                "To download Git updates to your local machine",
                "To propose, review, and discuss code changes before merging into a target branch",
                "To completely wipe the commit history of a repository",
                "To compile Python scripts into executable binaries"
            ],
            "correct_index": 1,
            "explanation": "A Pull Request (PR) allows team members to review code, run checks, and discuss changes before merging to main/master."
        },
        {
            "id": "py_9",
            "category": "Problem Solving",
            "skill_key": "Problem Solving",
            "question": "You have a list of numbers with duplicates: [3, 1, 2, 3, 2, 4]. What is the most idiomatic Python way to obtain unique elements in ascending order?",
            "options": [
                "sorted(list(set(numbers)))",
                "numbers.sort().unique()",
                "filter(unique, numbers)",
                "[x for x in numbers if x in numbers]"
            ],
            "correct_index": 0,
            "explanation": "Passing the list into 'set()' deduplicates it, and 'sorted()' produces a new sorted list."
        },
        {
            "id": "py_10",
            "category": "Problem Solving",
            "skill_key": "Problem Solving",
            "question": "How do you safely read file contents in Python without risking unclosed file handlers if an error occurs?",
            "options": [
                "f = open('data.txt'); f.read()",
                "with open('data.txt', 'r') as f: content = f.read()",
                "file.load_entirely('data.txt')",
                "import os; os.force_open('data.txt')"
            ],
            "correct_index": 1,
            "explanation": "The 'with' statement creates a context manager that guarantees the file is properly closed even if exceptions arise."
        },
        {
            "id": "py_11",
            "category": "Project Experience",
            "skill_key": "Project Experience",
            "question": "Which of the following best describes your hands-on experience building Python projects?",
            "options": [
                "I have only solved short textbook exercises without connecting multiple modules.",
                "I have written independent single-file scripts for automation or math calculations.",
                "I have built complete modular projects with SQLite databases, error handling, and Git version control.",
                "I have built and deployed production-grade Python web services with automated testing."
            ],
            "correct_index": 2, # Points scale: 0->25, 1->50, 2->75, 3->100
            "is_experience_scale": True,
            "explanation": "Project experience reflects applied engineering proficiency beyond theoretical knowledge."
        },
        {
            "id": "py_12",
            "category": "Project Experience",
            "skill_key": "Project Experience",
            "question": "How do you typically manage project dependencies in a Python project?",
            "options": [
                "I never track dependencies and rely on system-wide random pip installs.",
                "I use virtual environments (venv) and maintain a clean requirements.txt file.",
                "I manually copy python files from one folder to another without package managers.",
                "I hardcode third-party libraries into my source code directly."
            ],
            "correct_index": 1,
            "explanation": "Virtual environments (venv) isolate packages per project and requirements.txt enables reproducible builds."
        }
    ],

    "Web Developer": [
        {
            "id": "web_1",
            "category": "HTML5 & Semantics",
            "skill_key": "HTML5",
            "question": "Which HTML5 semantic element is most appropriate for the primary navigation menu of a web application?",
            "options": [
                "<div class='menu'>",
                "<nav>",
                "<section id='navigation'>",
                "<header-nav>"
            ],
            "correct_index": 1,
            "explanation": "The <nav> semantic element clearly denotes major navigation links for screen readers, search engines, and browsers."
        },
        {
            "id": "web_2",
            "category": "HTML5 & Semantics",
            "skill_key": "HTML5",
            "question": "In an HTML form, which attribute links an <input> field to its descriptive <label> for accessibility?",
            "options": [
                "The 'name' attribute of the input matching the 'title' of the label",
                "The 'id' of the input matching the 'for' attribute of the label",
                "The 'value' of the input matching the label text",
                "The 'placeholder' attribute matching the label class"
            ],
            "correct_index": 1,
            "explanation": "Setting <label for='input_id'> associates the label with the input having id='input_id', enabling screen readers and clickable labels."
        },
        {
            "id": "web_3",
            "category": "CSS3 & Responsive Design",
            "skill_key": "CSS3 & Responsive Design",
            "question": "Which CSS Flexbox property aligns child items along the cross axis (vertically in a row layout)?",
            "options": [
                "justify-content",
                "align-items",
                "flex-direction",
                "flex-wrap"
            ],
            "correct_index": 1,
            "explanation": "'justify-content' aligns items along the main axis, while 'align-items' aligns items along the cross axis."
        },
        {
            "id": "web_4",
            "category": "CSS3 & Responsive Design",
            "skill_key": "CSS3 & Responsive Design",
            "question": "What is the purpose of the CSS media query '@media (max-width: 768px)'?",
            "options": [
                "To enforce a maximum screen brightness",
                "To apply specific styling rules only on viewports/screens 768px wide or narrower (tablets/mobile)",
                "To limit the total download size of CSS stylesheets to 768 kilobytes",
                "To print documents at 768 DPI"
            ],
            "correct_index": 1,
            "explanation": "Media queries enable responsive web design by adapting layouts and font sizes to different screen widths."
        },
        {
            "id": "web_5",
            "category": "JavaScript ES6+",
            "skill_key": "JavaScript",
            "question": "What is the difference between 'let' and 'var' in modern JavaScript?",
            "options": [
                "'var' is block-scoped, whereas 'let' is function-scoped.",
                "'let' is block-scoped and prevents accidental redeclarations, whereas 'var' is function-scoped and hoisted.",
                "'let' cannot be reassigned once defined, but 'var' can.",
                "There is no difference; 'let' was merely an alias introduced for Internet Explorer."
            ],
            "correct_index": 1,
            "explanation": "'let' is block-scoped, does not allow redeclaration within the same block, and avoids common variable hoisting bugs."
        },
        {
            "id": "web_6",
            "category": "JavaScript ES6+",
            "skill_key": "JavaScript",
            "question": "How do you attach a click event handler to a button with id 'submit-btn' in vanilla JavaScript?",
            "options": [
                "document.getElementById('submit-btn').addEventListener('click', myFunction);",
                "document.select('#submit-btn').onClick = myFunction;",
                "window.bind('submit-btn', 'click', myFunction);",
                "Element.click('submit-btn', myFunction);"
            ],
            "correct_index": 0,
            "explanation": "'addEventListener' is the standard W3C method for registering event listeners on DOM elements."
        },
        {
            "id": "web_7",
            "category": "Python/Flask Backend",
            "skill_key": "Python/Flask Backend",
            "question": "In a Flask web application, how do you capture submitted form input from an HTTP POST request?",
            "options": [
                "request.args.get('field_name')",
                "request.form.get('field_name')",
                "flask.body['field_name']",
                "session.payload['field_name']"
            ],
            "correct_index": 1,
            "explanation": "In Flask, 'request.form' contains data sent via HTTP POST from HTML forms, whereas 'request.args' contains URL query parameters."
        },
        {
            "id": "web_8",
            "category": "Python/Flask Backend",
            "skill_key": "Python/Flask Backend",
            "question": "What Jinja2 syntax is used to output a dynamic variable inside an HTML template?",
            "options": [
                "<% variable %>",
                "{{ variable }}",
                "{# variable #}",
                "[[ variable ]]"
            ],
            "correct_index": 1,
            "explanation": "In Jinja2 templates, double curly braces {{ ... }} render variable expressions to the browser."
        },
        {
            "id": "web_9",
            "category": "Git & Version Control",
            "skill_key": "Git & Version Control",
            "question": "What is the role of the '.gitignore' file in a web project?",
            "options": [
                "To block unauthorized website visitors by IP",
                "To tell Git which files or directories (like .env, node_modules, or database files) to exclude from version tracking",
                "To minify CSS and JavaScript files before deploying",
                "To configure router redirects on the web server"
            ],
            "correct_index": 1,
            "explanation": "'.gitignore' prevents sensitive credentials, local database files, virtual environments, and temporary files from being committed."
        },
        {
            "id": "web_10",
            "category": "Git & Version Control",
            "skill_key": "Git & Version Control",
            "question": "How do you view recent Git commits with their commit hashes and messages in terminal?",
            "options": [
                "git status",
                "git log --oneline",
                "git diff --summary",
                "git remote -v"
            ],
            "correct_index": 1,
            "explanation": "'git log --oneline' displays the commit history compactly with short SHA hashes and commit messages."
        },
        {
            "id": "web_11",
            "category": "Project Experience",
            "skill_key": "Project Experience",
            "question": "Which best describes your real-world web project portfolio experience?",
            "options": [
                "I have only copied code snippets from YouTube tutorials without understanding structure.",
                "I have created simple static HTML/CSS web pages without forms or backend connections.",
                "I have designed responsive multi-page web applications with forms, dynamic backend routing, and SQLite storage.",
                "I have built, tested, and deployed full-stack web applications with authentication and REST APIs."
            ],
            "correct_index": 2,
            "is_experience_scale": True,
            "explanation": "Hands-on full-stack development demonstrates holistic readiness for junior web engineering roles."
        },
        {
            "id": "web_12",
            "category": "Project Experience",
            "skill_key": "Project Experience",
            "question": "How do you ensure web pages look good and function properly on both mobile smartphones and desktop monitors?",
            "options": [
                "I test only on desktop and assume mobile users will zoom in.",
                "I use viewport meta tags, responsive CSS frameworks (e.g. Bootstrap 5), fluid grid layouts, and test in browser developer tools.",
                "I build two completely separate websites and ask visitors to manually pick.",
                "I lock viewport width to 1920 pixels."
            ],
            "correct_index": 1,
            "explanation": "Mobile-first responsive design combines the viewport meta tag, flexible grid layouts, and media queries."
        }
    ],

    "Data Analyst": [
        {
            "id": "da_1",
            "category": "Python for Data",
            "skill_key": "Python for Data",
            "question": "In Python Pandas, which method is used to inspect summary statistics (mean, count, standard deviation, quartiles) of numerical columns?",
            "options": [
                "df.info()",
                "df.describe()",
                "df.summary()",
                "df.metrics()"
            ],
            "correct_index": 1,
            "explanation": "'df.describe()' computes count, mean, std, min, 25%, 50%, 75%, and max for all numerical series in a DataFrame."
        },
        {
            "id": "da_2",
            "category": "Python for Data",
            "skill_key": "Python for Data",
            "question": "How do you filter a Pandas DataFrame 'df' to keep only rows where the 'salary' column is greater than 50000?",
            "options": [
                "df[df['salary'] > 50000]",
                "df.filter(salary > 50000)",
                "df.where('salary' > 50000)",
                "df.select(df.salary > 50000)"
            ],
            "correct_index": 0,
            "explanation": "Boolean indexing 'df[df['salary'] > 50000]' evaluates the condition per row and filters the DataFrame."
        },
        {
            "id": "da_3",
            "category": "SQL & Databases",
            "skill_key": "SQL & Databases",
            "question": "Which SQL JOIN returns all rows from the left table, and the matched rows from the right table (filling NULL if no match exists)?",
            "options": [
                "INNER JOIN",
                "LEFT OUTER JOIN",
                "RIGHT OUTER JOIN",
                "CROSS JOIN"
            ],
            "correct_index": 1,
            "explanation": "LEFT JOIN preserves every record from the left table regardless of whether a matching record exists on the right."
        },
        {
            "id": "da_4",
            "category": "SQL & Databases",
            "skill_key": "SQL & Databases",
            "question": "What SQL query computes the average placement package per college branch from a 'placements' table?",
            "options": [
                "SELECT branch, AVG(package) FROM placements GROUP BY branch;",
                "SELECT branch, SUM(package) FROM placements WHERE branch = AVG;",
                "SELECT AVG(package) FROM placements ORDER BY branch;",
                "SELECT branch FROM placements HAVING AVG(package);"
            ],
            "correct_index": 0,
            "explanation": "'GROUP BY branch' aggregates rows by branch, enabling the aggregate function 'AVG(package)' to compute branch-wise averages."
        },
        {
            "id": "da_5",
            "category": "Excel / Spreadsheets",
            "skill_key": "Excel / Spreadsheets",
            "question": "In modern Excel/Google Sheets, which lookup formula replaces VLOOKUP with bidirectional search without requiring helper columns?",
            "options": [
                "HLOOKUP",
                "XLOOKUP",
                "MATCH_DIRECT",
                "SEARCH_ROW"
            ],
            "correct_index": 1,
            "explanation": "XLOOKUP looks up values to both the left and right, defaults to exact match, and handles missing values cleanly."
        },
        {
            "id": "da_6",
            "category": "Excel / Spreadsheets",
            "skill_key": "Excel / Spreadsheets",
            "question": "What is the primary analytical advantage of using an Excel Pivot Table?",
            "options": [
                "It automatically changes font colors to random themes.",
                "It allows rapid multidimensional grouping, summarization, and slicing of large datasets without manual formulas.",
                "It converts text files to PDF documents.",
                "It protects the workbook with 256-bit encryption."
            ],
            "correct_index": 1,
            "explanation": "Pivot Tables allow analysts to slice, dice, summarize, and cross-tabulate tabular data interactively in seconds."
        },
        {
            "id": "da_7",
            "category": "Data Visualization",
            "skill_key": "Data Visualization",
            "question": "Which chart type is best suited for visualizing the distribution and skewness of a single continuous numerical variable?",
            "options": [
                "Pie Chart",
                "Histogram (or Box Plot)",
                "Radar Chart",
                "Donut Chart"
            ],
            "correct_index": 1,
            "explanation": "Histograms show frequency distributions across bins; box plots display median, quartiles, and outliers."
        },
        {
            "id": "da_8",
            "category": "Data Visualization",
            "skill_key": "Data Visualization",
            "question": "When designing an executive dashboard, why should pie charts with more than 7 slices be avoided?",
            "options": [
                "Computers cannot calculate degrees for more than 7 slices.",
                "Human visual perception struggles to accurately judge small angle and area differences compared to a clean bar chart.",
                "Pie charts only accept text strings, not numbers.",
                "Browsers crash when rendering multi-slice SVG graphics."
            ],
            "correct_index": 1,
            "explanation": "Data visualization best practice recommends horizontal or vertical bar charts over crowded pie charts for readability."
        },
        {
            "id": "da_9",
            "category": "Statistics Basics",
            "skill_key": "Statistics Basics",
            "question": "When a salary distribution has extreme outliers (e.g., a few CEO multi-crore salaries), which metric best reflects the typical employee earnings?",
            "options": [
                "Mean (Arithmetic average)",
                "Median (Middle value)",
                "Standard Deviation",
                "Range (Max - Min)"
            ],
            "correct_index": 1,
            "explanation": "The median is robust against extreme outliers and skewed distributions, unlike the mean which gets pulled upward."
        },
        {
            "id": "da_10",
            "category": "Statistics Basics",
            "skill_key": "Statistics Basics",
            "question": "What does a Pearson correlation coefficient of r = -0.85 between two variables signify?",
            "options": [
                "No relationship exists between the variables.",
                "A strong negative linear relationship (as one variable increases, the other systematically decreases).",
                "85% of the data values are negative numbers.",
                "The analysis contains an 85% margin of calculation error."
            ],
            "correct_index": 1,
            "explanation": "Correlation r ranges from -1.0 to +1.0. A value of -0.85 indicates a strong negative linear association."
        },
        {
            "id": "da_11",
            "category": "Project Experience",
            "skill_key": "Project Experience",
            "question": "What describes your hands-on experience handling dirty or missing real-world datasets?",
            "options": [
                "I have only used perfectly clean 5-row toy tables in class slides.",
                "I have practiced handling null values, deduplicating records, and converting datetime formats in Pandas or SQL.",
                "I usually delete all columns that have even one empty cell.",
                "I have never handled datasets outside of pre-formatted PDFs."
            ],
            "correct_index": 1,
            "is_experience_scale": True,
            "explanation": "Real analytics tasks involve significant data wrangling, imputation, and validation before deriving insights."
        },
        {
            "id": "da_12",
            "category": "Project Experience",
            "skill_key": "Project Experience",
            "question": "How have you presented analytical conclusions to peers or mentors?",
            "options": [
                "I print raw terminal logs or 10,000 unformatted database rows.",
                "I structure insights into an executive summary, clear visual charts, and actionable business recommendations.",
                "I assume numbers speak for themselves without narrative or context.",
                "I avoid explaining results and let others guess."
            ],
            "correct_index": 1,
            "explanation": "Effective data analysts translate raw statistics into clear, actionable business recommendations for stakeholders."
        }
    ]
}

def get_questions_for_career(career_path):
    """Retrieve curated diagnostic questions for the specified career."""
    return ASSESSMENT_QUESTIONS.get(career_path, ASSESSMENT_QUESTIONS["Python Developer"])

def evaluate_assessment(career_path, submitted_answers):
    """
    Score the student's submission.
    submitted_answers: dict of {question_id: int(chosen_index)}
    
    Returns:
    - total_score: float
    - max_possible: float
    - overall_percentage: float
    - category_scores: dict {skill_key: {'score': float, 'max': float, 'percentage': float}}
    - question_results: list of detailed review objects
    """
    questions = get_questions_for_career(career_path)
    category_scores = {}
    question_results = []
    
    total_earned = 0.0
    total_max = 0.0
    
    for q in questions:
        qid = q["id"]
        skill_key = q["skill_key"]
        
        if skill_key not in category_scores:
            category_scores[skill_key] = {"earned": 0.0, "max": 0.0}
            
        chosen = submitted_answers.get(qid)
        is_answered = chosen is not None
        chosen_int = int(chosen) if is_answered and str(chosen).isdigit() else None
        
        # Scoring logic
        question_max = 10.0
        earned = 0.0
        
        if q.get("is_experience_scale"):
            # Experience questions scale points 0 to 10
            if chosen_int is not None:
                # 4 options: 0->2.5, 1->5.0, 2->7.5, 3->10.0
                scale_map = {0: 2.5, 1: 5.0, 2: 7.5, 3: 10.0}
                earned = scale_map.get(chosen_int, 0.0)
            is_correct = (chosen_int is not None and chosen_int >= 2)
        else:
            is_correct = (chosen_int == q["correct_index"])
            if is_correct:
                earned = question_max
                
        total_earned += earned
        total_max += question_max
        category_scores[skill_key]["earned"] += earned
        category_scores[skill_key]["max"] += question_max
        
        question_results.append({
            "id": qid,
            "question": q["question"],
            "options": q["options"],
            "chosen_index": chosen_int,
            "correct_index": q["correct_index"],
            "is_correct": is_correct,
            "explanation": q["explanation"],
            "category": q["category"],
            "skill_key": skill_key,
            "earned": earned,
            "max": question_max
        })
        
    overall_percentage = round((total_earned / total_max * 100), 1) if total_max > 0 else 0.0
    
    # Scale category scores to 0-100 scale
    normalized_skills = {}
    for skill, val in category_scores.items():
        if val["max"] > 0:
            pct = round((val["earned"] / val["max"]) * 100, 1)
        else:
            pct = 0.0
        normalized_skills[skill] = {
            "current_score": pct,
            "earned": val["earned"],
            "max": val["max"]
        }
        
    return {
        "total_score": total_earned,
        "max_possible": total_max,
        "overall_percentage": overall_percentage,
        "normalized_skills": normalized_skills,
        "question_results": question_results
    }

def save_assessment_record(user_id, career_path, evaluation_result):
    """Save assessment header record in SQLite and return assessment_id."""
    db = get_db()
    cursor = db.execute("""
        INSERT INTO assessments (user_id, career_path, total_score, max_possible, readiness_percentage)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        career_path,
        evaluation_result["total_score"],
        evaluation_result["max_possible"],
        evaluation_result["overall_percentage"]
    ))
    assessment_id = cursor.lastrowid
    db.commit()
    return assessment_id

def get_latest_assessment(user_id):
    """Retrieve the most recent assessment completed by the student."""
    db = get_db()
    row = db.execute("""
        SELECT * FROM assessments 
        WHERE user_id = ? 
        ORDER BY taken_at DESC 
        LIMIT 1
    """, (user_id,)).fetchone()
    return dict(row) if row else None

def get_assessment_history(user_id):
    """Retrieve assessment history list for student dashboard."""
    db = get_db()
    rows = db.execute("""
        SELECT * FROM assessments 
        WHERE user_id = ? 
        ORDER BY taken_at DESC
    """, (user_id,)).fetchall()
    return [dict(r) for r in rows]

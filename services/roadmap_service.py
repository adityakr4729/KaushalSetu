"""
Personalized Roadmap Service for Kaushal Setu.
Provides:
- 4-week structured 30-day curriculum adapted to student's career path
- Integration with identified skill gaps to highlight high-priority focus areas
- Dynamic task completion tracking in user_task_progress table
- Dynamic progress calculation (overall & per week)
"""

from database.db import get_db

def get_student_roadmap(user_id, career_path=None):
    """
    Retrieve roadmap tasks for the student, merged with their individual completion status
    and priority flags based on skill gap analysis.
    """
    db = get_db()
    
    # If career path not explicitly passed, inspect student profile
    if not career_path:
        profile = db.execute("SELECT target_career FROM student_profiles WHERE user_id = ?", (user_id,)).fetchone()
        career_path = profile["target_career"] if profile and profile["target_career"] else "Python Developer"
        
    # Get all roadmap tasks for this career
    tasks = db.execute("""
        SELECT * FROM roadmap_tasks 
        WHERE career_path = ?
        ORDER BY week_number ASC, day_number ASC
    """, (career_path,)).fetchall()
    
    # Get user's completed tasks
    progress_rows = db.execute("""
        SELECT task_id, is_completed, completed_at 
        FROM user_task_progress 
        WHERE user_id = ?
    """, (user_id,)).fetchall()
    
    progress_map = {r["task_id"]: (bool(r["is_completed"]), r["completed_at"]) for r in progress_rows}
    
    # Get user's latest skill gap priorities to highlight relevant tasks
    latest_assessment = db.execute("""
        SELECT id FROM assessments WHERE user_id = ? ORDER BY taken_at DESC LIMIT 1
    """, (user_id,)).fetchone()
    
    priority_skills = set()
    if latest_assessment:
        gap_rows = db.execute("""
            SELECT skill_name FROM skill_results 
            WHERE assessment_id = ? AND priority IN ('High', 'Medium')
        """, (latest_assessment["id"],)).fetchall()
        priority_skills = {r["skill_name"] for r in gap_rows}
        
    structured_weeks = {1: [], 2: [], 3: [], 4: []}
    total_tasks = len(tasks)
    completed_count = 0
    total_hours = 0.0
    completed_hours = 0.0
    
    merged_tasks = []
    for t in tasks:
        tid = t["id"]
        is_done, comp_date = progress_map.get(tid, (False, None))
        is_priority = (t["skill_name"] in priority_skills)
        
        task_obj = dict(t)
        task_obj["is_completed"] = is_done
        task_obj["completed_at"] = comp_date
        task_obj["is_priority_focus"] = is_priority
        
        if is_done:
            completed_count += 1
            completed_hours += t["estimated_hours"]
            
        total_hours += t["estimated_hours"]
        
        week_num = t["week_number"]
        if week_num in structured_weeks:
            structured_weeks[week_num].append(task_obj)
            
        merged_tasks.append(task_obj)
        
    completion_percentage = round((completed_count / total_tasks * 100), 1) if total_tasks > 0 else 0.0
    
    # Calculate per-week completion stats
    week_stats = {}
    for w in [1, 2, 3, 4]:
        w_tasks = structured_weeks.get(w, [])
        w_total = len(w_tasks)
        w_done = sum(1 for t in w_tasks if t["is_completed"])
        w_pct = round((w_done / w_total * 100), 1) if w_total > 0 else 0.0
        week_stats[w] = {
            "total": w_total,
            "completed": w_done,
            "percentage": w_pct
        }
        
    # Find next pending task recommendation
    next_task = next((t for t in merged_tasks if not t["is_completed"]), None)
    
    return {
        "career_path": career_path,
        "total_tasks": total_tasks,
        "completed_count": completed_count,
        "pending_count": total_tasks - completed_count,
        "completion_percentage": completion_percentage,
        "total_hours": total_hours,
        "completed_hours": completed_hours,
        "structured_weeks": structured_weeks,
        "week_stats": week_stats,
        "all_tasks": merged_tasks,
        "next_task": next_task
    }

def toggle_task_completion(user_id, task_id, is_completed=None):
    """
    Toggle or explicitly set a roadmap task completion for the authenticated user.
    Guarantees user-level record isolation.
    """
    db = get_db()
    
    # Check if entry exists
    existing = db.execute("""
        SELECT is_completed FROM user_task_progress 
        WHERE user_id = ? AND task_id = ?
    """, (user_id, task_id)).fetchone()
    
    if existing is None:
        new_status = 1 if is_completed is None else (1 if is_completed else 0)
        db.execute("""
            INSERT INTO user_task_progress (user_id, task_id, is_completed, completed_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (user_id, task_id, new_status))
    else:
        if is_completed is None:
            new_status = 0 if existing["is_completed"] == 1 else 1
        else:
            new_status = 1 if is_completed else 0
            
        timestamp_clause = "CURRENT_TIMESTAMP" if new_status == 1 else "NULL"
        db.execute(f"""
            UPDATE user_task_progress 
            SET is_completed = ?, completed_at = {timestamp_clause}
            WHERE user_id = ? AND task_id = ?
        """, (new_status, user_id, task_id))
        
    db.commit()
    return bool(new_status)

"""
Job & Internship Matching Service for Kaushal Setu.
Implements:
- Skill overlap matching algorithm between student skills and job requirements
- Dynamic filtering by Career, Opportunity Type, Location, and Required Skills
- Clear DEMO DATA labelling and readiness for National Career Service (NCS) API integration
"""

from database.db import get_db

def extract_student_skills(user_id):
    """
    Extract the union of skills from student's profile and assessment results.
    Returns: set of lowercase cleaned skill tokens and original display skill names.
    """
    db = get_db()
    
    # 1. Profile technical skills
    profile = db.execute("SELECT technical_skills, target_career FROM student_profiles WHERE user_id = ?", (user_id,)).fetchone()
    skills_set = set()
    
    if profile and profile["technical_skills"]:
        for s in profile["technical_skills"].split(","):
            token = s.strip().lower()
            if token:
                skills_set.add(token)
                
    # 2. Mastered or competent skills from latest assessment
    latest_assessment = db.execute("SELECT id FROM assessments WHERE user_id = ? ORDER BY taken_at DESC LIMIT 1", (user_id,)).fetchone()
    if latest_assessment:
        assessed_skills = db.execute("""
            SELECT skill_name, current_score FROM skill_results 
            WHERE assessment_id = ? AND current_score >= 50.0
        """, (latest_assessment["id"],)).fetchall()
        for r in assessed_skills:
            # Add general skill name
            name = r["skill_name"].lower()
            skills_set.add(name)
            # Add sub-tokens (e.g., 'python fundamentals' -> adds 'python')
            for part in name.replace("&", " ").replace("/", " ").split():
                if len(part) > 2:
                    skills_set.add(part)
                    
    # Fallback to default career foundation if brand new user
    if not skills_set and profile and profile["target_career"]:
        if "python" in profile["target_career"].lower():
            skills_set.update(["python", "problem solving"])
        elif "web" in profile["target_career"].lower():
            skills_set.update(["html", "css", "javascript"])
        elif "data" in profile["target_career"].lower():
            skills_set.update(["python", "excel", "sql"])
            
    return skills_set

def calculate_opportunity_match(student_skills_set, req_skills_str):
    """
    Compute skill overlap and percentage match.
    req_skills_str: comma-separated list of required skills.
    
    Returns:
    - match_percentage: int (0 to 100)
    - matched_skills: list of string
    - missing_skills: list of string
    - match_level: 'High', 'Moderate', 'Low'
    - match_reason: text explanation
    """
    if not req_skills_str:
        return 0, [], [], "Low", "No specific skill requirements listed."
        
    req_list = [s.strip() for s in req_skills_str.split(",") if s.strip()]
    if not req_list:
        return 0, [], [], "Low", "No specific skill requirements listed."
        
    matched = []
    missing = []
    
    for req in req_list:
        req_clean = req.lower()
        # Direct match or partial token match
        is_matched = False
        if req_clean in student_skills_set:
            is_matched = True
        else:
            # Check if any student skill token is part of required skill or vice versa
            for s in student_skills_set:
                if s in req_clean or req_clean in s:
                    is_matched = True
                    break
                    
        if is_matched:
            matched.append(req)
        else:
            missing.append(req)
            
    match_pct = round((len(matched) / len(req_list)) * 100)
    
    if match_pct >= 75:
        match_level = "High"
        level_class = "success"
        reason = f"Excellent match! You possess {len(matched)} of {len(req_list)} required core skills."
    elif match_pct >= 40:
        match_level = "Moderate"
        level_class = "warning"
        reason = f"Good foundational match ({len(matched)}/{len(req_list)} skills). Build your roadmap to cover {', '.join(missing[:2])}."
    else:
        match_level = "Growth Opportunity"
        level_class = "secondary"
        reason = f"Requires upskilling ({len(missing)} missing skills). Focus on {missing[0] if missing else 'prerequisites'} first."
        
    return match_pct, matched, missing, match_level, level_class, reason

def get_matched_opportunities(user_id, career_filter=None, type_filter=None, location_filter=None, skill_filter=None):
    """
    Retrieve demo opportunities filtered and sorted by student match score.
    """
    db = get_db()
    student_skills = extract_student_skills(user_id)
    
    query = "SELECT * FROM opportunities WHERE 1=1"
    params = []
    
    if career_filter and career_filter != "All":
        query += " AND career_path = ?"
        params.append(career_filter)
        
    if type_filter and type_filter != "All":
        query += " AND opportunity_type = ?"
        params.append(type_filter)
        
    if location_filter and location_filter != "All":
        if location_filter == "Remote":
            query += " AND is_remote = 1"
        else:
            query += " AND location LIKE ?"
            params.append(f"%{location_filter}%")
            
    if skill_filter and skill_filter.strip():
        query += " AND required_skills LIKE ?"
        params.append(f"%{skill_filter.strip()}%")
        
    rows = db.execute(query, params).fetchall()
    
    matched_listings = []
    for r in rows:
        pct, matched, missing, level, level_class, reason = calculate_opportunity_match(student_skills, r["required_skills"])
        listing = dict(r)
        listing["match_percentage"] = pct
        listing["matched_skills"] = matched
        listing["missing_skills"] = missing
        listing["match_level"] = level
        listing["match_level_class"] = level_class
        listing["match_reason"] = reason
        listing["all_required_skills"] = [s.strip() for s in r["required_skills"].split(",") if s.strip()]
        matched_listings.append(listing)
        
    # Sort listings: highest match percentage first
    matched_listings.sort(key=lambda x: x["match_percentage"], reverse=True)
    return matched_listings

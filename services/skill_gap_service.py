"""
Skill Gap Engine for Kaushal Setu.
Implements:
- Benchmark target skill standards per career path (0-100 scale)
- Gap calculation: Gap = max(0, Target Score - Current Score)
- Priority categorisation (High, Medium, Low, Mastered)
- Bounded Readiness Percentage = (Sum of Current / Sum of Target) * 100
- Chart dataset formatting for Chart.js
"""

from database.db import get_db

# Benchmark target standards required for entry-level employability
CAREER_SKILL_TARGETS = {
    "Python Developer": {
        "Python Fundamentals": 85.0,
        "Data Structures": 80.0,
        "SQL & Databases": 75.0,
        "Git & GitHub": 70.0,
        "Problem Solving": 80.0,
        "Project Experience": 75.0
    },
    "Web Developer": {
        "HTML5": 90.0,
        "CSS3 & Responsive Design": 85.0,
        "JavaScript": 80.0,
        "Python/Flask Backend": 75.0,
        "Git & Version Control": 70.0,
        "Project Experience": 75.0
    },
    "Data Analyst": {
        "Python for Data": 80.0,
        "SQL & Databases": 85.0,
        "Excel / Spreadsheets": 85.0,
        "Data Visualization": 75.0,
        "Statistics Basics": 75.0,
        "Project Experience": 70.0
    }
}

def get_target_skills(career_path):
    """Retrieve target benchmark skill scores for a career."""
    return CAREER_SKILL_TARGETS.get(career_path, CAREER_SKILL_TARGETS["Python Developer"])

def calculate_skill_gaps(career_path, current_skill_scores):
    """
    Calculate skill gaps and readiness based on:
    - Gap = max(0, Target Score - Current Score)
    - Readiness % = (Sum(Current) / Sum(Target)) * 100 [bounded 0-100]
    
    current_skill_scores: dict of {skill_name: score_0_to_100}
    """
    targets = get_target_skills(career_path)
    
    breakdown = []
    sum_current = 0.0
    sum_target = 0.0
    
    for skill_name, target_score in targets.items():
        curr_score = float(current_skill_scores.get(skill_name, 0.0))
        # Ensure current score bounded between 0 and 100
        curr_score = max(0.0, min(100.0, curr_score))
        gap = max(0.0, round(target_score - curr_score, 1))
        
        # Priority mapping
        if gap >= 30.0:
            priority = "High"
            badge_class = "danger"
            recommendation = "Immediate focus needed. Fundamental concepts require systematic practice."
        elif gap >= 15.0:
            priority = "Medium"
            badge_class = "warning"
            recommendation = "Moderate gap. Strengthen via targeted practice exercises and mini-projects."
        elif gap > 0.0:
            priority = "Low"
            badge_class = "info"
            recommendation = "Minor polish needed. Review best practices and practical nuances."
        else:
            priority = "Mastered"
            badge_class = "success"
            recommendation = "Target standard satisfied! Maintain proficiency through code reviews."
            
        breakdown.append({
            "skill_name": skill_name,
            "current_score": curr_score,
            "target_score": target_score,
            "gap": gap,
            "priority": priority,
            "badge_class": badge_class,
            "recommendation": recommendation
        })
        
        sum_current += curr_score
        sum_target += target_score
        
    readiness_percentage = round(min(100.0, max(0.0, (sum_current / sum_target) * 100.0)), 1) if sum_target > 0 else 0.0
    
    # Sort for analytical insights
    sorted_by_gap_desc = sorted(breakdown, key=lambda x: x["gap"], reverse=True)
    sorted_by_current_desc = sorted(breakdown, key=lambda x: x["current_score"], reverse=True)
    
    strongest_skills = [s for s in sorted_by_current_desc if s["current_score"] >= 60.0][:3]
    if not strongest_skills:
        strongest_skills = sorted_by_current_desc[:2]
        
    priority_gaps = [s for s in sorted_by_gap_desc if s["gap"] > 0][:3]
    
    # Prepare Chart.js compatible arrays
    chart_labels = [s["skill_name"] for s in breakdown]
    chart_current = [s["current_score"] for s in breakdown]
    chart_target = [s["target_score"] for s in breakdown]
    
    return {
        "career_path": career_path,
        "readiness_percentage": readiness_percentage,
        "sum_current": round(sum_current, 1),
        "sum_target": round(sum_target, 1),
        "breakdown": breakdown,
        "strongest_skills": strongest_skills,
        "priority_gaps": priority_gaps,
        "chart_data": {
            "labels": chart_labels,
            "current": chart_current,
            "target": chart_target
        }
    }

def save_skill_results(assessment_id, user_id, gap_analysis):
    """Persist skill gap breakdown records into SQLite."""
    db = get_db()
    
    # Remove older results for this assessment if any
    db.execute("DELETE FROM skill_results WHERE assessment_id = ?", (assessment_id,))
    
    for item in gap_analysis["breakdown"]:
        db.execute("""
            INSERT INTO skill_results (
                assessment_id, user_id, skill_name, current_score, target_score, gap, priority
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            assessment_id,
            user_id,
            item["skill_name"],
            item["current_score"],
            item["target_score"],
            item["gap"],
            item["priority"]
        ))
    db.commit()

def get_latest_skill_results(user_id):
    """Fetch latest stored skill results for student."""
    db = get_db()
    latest_assessment = db.execute("""
        SELECT * FROM assessments 
        WHERE user_id = ? 
        ORDER BY taken_at DESC 
        LIMIT 1
    """, (user_id,)).fetchone()
    
    if not latest_assessment:
        return None
        
    rows = db.execute("""
        SELECT * FROM skill_results 
        WHERE assessment_id = ? AND user_id = ?
        ORDER BY gap DESC
    """, (latest_assessment["id"], user_id)).fetchall()
    
    breakdown = [dict(r) for r in rows]
    # Augment badge class
    for b in breakdown:
        if b["priority"] == "High":
            b["badge_class"] = "danger"
        elif b["priority"] == "Medium":
            b["badge_class"] = "warning"
        elif b["priority"] == "Low":
            b["badge_class"] = "info"
        else:
            b["badge_class"] = "success"
            
    chart_labels = [r["skill_name"] for r in breakdown]
    chart_current = [r["current_score"] for r in breakdown]
    chart_target = [r["target_score"] for r in breakdown]
    
    strongest = [r for r in sorted(breakdown, key=lambda x: x["current_score"], reverse=True)][:3]
    priority_gaps = [r for r in breakdown if r["gap"] > 0][:3]
    
    return {
        "assessment": dict(latest_assessment),
        "career_path": latest_assessment["career_path"],
        "readiness_percentage": latest_assessment["readiness_percentage"],
        "breakdown": breakdown,
        "strongest_skills": strongest,
        "priority_gaps": priority_gaps,
        "chart_data": {
            "labels": chart_labels,
            "current": chart_current,
            "target": chart_target
        }
    }

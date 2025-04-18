import re
import spacy

nlp = spacy.load("en_core_web_sm")

def analyze(skills_list, text, results):
    matched_skills = []
    missing_skills = []
    for skill in skills_list:
        if skill in text.lower():
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)
    skill_match_percentage = len(matched_skills) / len(skills_list) * 100
    resume_improvement_suggestions = []
    linkedin_pattern = r"(https?://)?(www\.)?linkedin\.com/(in|company)/[a-zA-Z0-9_-]+"
    if not re.search(linkedin_pattern, text):
        resume_improvement_suggestions.append("Add your LinkedIn profile URL.")
    if not re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text):
        resume_improvement_suggestions.append("Add a valid email address.")
    if not re.search(r'\+?(\d[\d\-\+\(\) ]{7,}\d)', text):
        resume_improvement_suggestions.append("Add your phone number.")
    if not re.search(r'work experience|employment', text, re.IGNORECASE):
        resume_improvement_suggestions.append("Add your work experience section.")
    if not re.search(r'education|degree|university', text, re.IGNORECASE):
        resume_improvement_suggestions.append("Add your educational background.")
    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_percentage": skill_match_percentage,
        "resume_improvement_suggestions": resume_improvement_suggestions
    }
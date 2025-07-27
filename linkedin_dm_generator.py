#!/usr/bin/env python3

def generate_linkedin_dm(jd, me):
    """
    Generate a LinkedIn DM under 300 characters.
    
    Args:
        jd (str): Job description
        me (str): Resume blurb
    
    Returns:
        str: LinkedIn DM with matching skill, result, and call-to-chat
    """
    
    # Extract key skills from JD (simplified matching)
    jd_lower = jd.lower()
    me_lower = me.lower()
    
    # Common skills to match
    skills = ['python', 'javascript', 'react', 'sql', 'aws', 'docker', 'kubernetes', 
              'machine learning', 'data science', 'project management', 'agile',
              'typescript', 'node.js', 'java', 'c++', 'git', 'ci/cd', 'devops']
    
    matching_skill = None
    for skill in skills:
        if skill in jd_lower and skill in me_lower:
            matching_skill = skill
            break
    
    if not matching_skill:
        matching_skill = "relevant experience"
    
    # Extract a quantified result from resume blurb
    import re
    numbers = re.findall(r'\d+[%x]|\d+\+|increased.*?\d+|reduced.*?\d+|improved.*?\d+', me_lower)
    result = numbers[0] if numbers else "strong results"
    
    # Generate DM
    dm = f"Hi! Saw your {matching_skill} role. My background includes {matching_skill} with {result} in similar projects. Would love to chat about how I could contribute. Free for a quick call?"
    
    # Ensure under 300 characters
    if len(dm) > 300:
        dm = f"Hi! Saw your {matching_skill} role. My {matching_skill} experience delivered {result}. Would love to chat about contributing. Free for a call?"
    
    return dm

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python linkedin_dm_generator.py '<job_description>' '<resume_blurb>'")
        sys.exit(1)
    
    jd = sys.argv[1]
    me = sys.argv[2]
    
    dm = generate_linkedin_dm(jd, me)
    print(dm)
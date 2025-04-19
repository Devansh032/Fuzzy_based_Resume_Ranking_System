import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import json
import sys

candidate_data_x = {
    "status": True,
    "message": "python Developer 1",
    "data": {
        "rank": "80",
        "skills": [
            {
                "low": [
                    "JavaScript",
                    "TypeScript",
                    "ReactJS",
                    "NextJS",
                    "NodeJS",
                    "ExpressJS"
                ]
            },
            {
                "medium": [
                    "Python",
                    "C++",
                    "C",
                    "PyTorch",
                    "Pandas",
                    "Matplotlib",
                    "Seaborn",
                    "NumPy",
                    "Scikit-learn",
                    "VS Code",
                    "Git",
                    "MongoDB",
                    "MySQL",
                    "Redis"
                ]
            },
            {
                "high": [
                    "Docker",
                    "Machine Learning Algorithms",
                    "Deep Learning",
                    "Data Science and Analytics",
                    "AI and Problem Solving"
                ]
            }
        ],
        "total_experience": "0",
        "project_category": [
            "Data Science & Analytics",
            "Web Development"
        ]
    }
}

job_requirements_x = {
    "Python": 1.0,
    "Data Science and Analytics": 0.9,
    "Machine Learning Algorithms": 0.85,
    "Deep Learning": 0.8,
    "NumPy": 0.7,
    "Pandas": 0.7,
    "Scikit-learn": 0.7,
    "Docker": 0.6,
    "Git": 0.5,
    "MongoDB": 0.4,
    "MySQL": 0.4,
    "JavaScript": 0.3,
    "ReactJS": 0.3
}



def calculate_skill_score(skills_data:dict, job_reqs):
    # Define fuzzy membership values
    membership_values = {
        "medium": 0.5,  # Base value for medium proficiency
    }
    
    # Apply concentration/dilation operators
    k_low = 1/2
    k_high = 2
    
    fuzzy_membership = {
        "low": membership_values["medium"] ** k_low,   # Dilation for low skills
        "medium": membership_values["medium"],      # Keep medium as is
        "high": membership_values["medium"] ** k_high # Concentration for high skills
    }
    
    # Extract skills from each category
    all_skills = {}
    for proficiency, skill_list in skills_data.items():
        for skill in skill_list:
            all_skills[skill] = fuzzy_membership[proficiency]
    
    # Calculate weighted skill score
    total_weight = 0
    weighted_score = 0
    
    for skill, weight in job_reqs.items():
        if skill in all_skills:
            weighted_score += all_skills[skill] * weight
            total_weight += weight
    
    # Normalize to 0-100 scale
    if total_weight > 0:
        normalized_score = (weighted_score / total_weight) * 100
        return normalized_score
    else:
        return 0

def calculate_project_relevance(project_categories, job_position):
    # Define relevance scores for different project categories based on job position
    if "python developer" in job_position.lower() :
        relevance_scores = {
            "Data Science & Analytics": 90,
            "Web Development": 50,
            "Mobile App Development": 40,
            "DevOps": 60,
            "Backend Development": 65
        }
    else:
        # Default relevance scores
        relevance_scores = {
            "Data Science & Analytics": 50,
            "Web Development": 50,
            "Mobile App Development": 50,
            "DevOps": 50,
            "Backend Development": 50
        }
    
    # Calculate average relevance score
    total_relevance = 0
    for category in project_categories:
        if category in relevance_scores:
            total_relevance += relevance_scores[category]
    
    if project_categories:
        return total_relevance / len(project_categories)
    else:
        return 0

def fuzzy_candidate_Scoring() : 
    # Set up fuzzy logic system
    # Define input variables
    skills = ctrl.Antecedent(np.arange(0, 101, 1), 'skills')
    experience = ctrl.Antecedent(np.arange(0, 11, 1), 'experience')
    project_relevance = ctrl.Antecedent(np.arange(0, 101, 1), 'project_relevance')

    # Define output variable
    candidate_score = ctrl.Consequent(np.arange(0, 101, 1), 'candidate_score')

    # Define membership functions
    skills['low'] = fuzz.trimf(skills.universe, [0, 0, 40])
    skills['medium'] = fuzz.trimf(skills.universe, [20, 50, 80])
    skills['high'] = fuzz.trimf(skills.universe, [60, 100, 100])

    experience['none'] = fuzz.trimf(experience.universe, [0, 0, 1])
    experience['junior'] = fuzz.trimf(experience.universe, [0, 2, 4])
    experience['mid'] = fuzz.trimf(experience.universe, [3, 5, 7])
    experience['senior'] = fuzz.trimf(experience.universe, [6, 10, 10])

    project_relevance['low'] = fuzz.trimf(project_relevance.universe, [0, 0, 40])
    project_relevance['medium'] = fuzz.trimf(project_relevance.universe, [20, 50, 80])
    project_relevance['high'] = fuzz.trimf(project_relevance.universe, [60, 100, 100])

    candidate_score['poor'] = fuzz.trimf(candidate_score.universe, [0, 0, 40])
    candidate_score['average'] = fuzz.trimf(candidate_score.universe, [20, 50, 80])
    candidate_score['good'] = fuzz.trimf(candidate_score.universe, [60, 100, 100])

    # Define rules
    rule1 = ctrl.Rule(skills['high'] & experience['senior'] & project_relevance['high'], candidate_score['good'])
    rule2 = ctrl.Rule(skills['high'] & experience['mid'] & project_relevance['high'], candidate_score['good'])
    rule3 = ctrl.Rule(skills['medium'] & experience['senior'] & project_relevance['high'], candidate_score['good'])
    rule4 = ctrl.Rule(skills['high'] & experience['junior'] & project_relevance['high'], candidate_score['good'])
    rule5 = ctrl.Rule(skills['high'] & experience['none'] & project_relevance['high'], candidate_score['average'])
    rule6 = ctrl.Rule(skills['medium'] & experience['mid'] & project_relevance['medium'], candidate_score['average'])
    rule7 = ctrl.Rule(skills['medium'] & experience['junior'] & project_relevance['medium'], candidate_score['average'])
    rule8 = ctrl.Rule(skills['medium'] & experience['none'] & project_relevance['medium'], candidate_score['average'])
    rule9 = ctrl.Rule(skills['low'] & experience['senior'] & project_relevance['high'], candidate_score['average'])
    rule10 = ctrl.Rule(skills['low'] & experience['none'] & project_relevance['low'], candidate_score['poor'])
    rule11 = ctrl.Rule(skills['high'] & experience['none'] & project_relevance['medium'], candidate_score['average'])
    rule12 = ctrl.Rule(skills['medium'] & experience['none'] & project_relevance['low'], candidate_score['poor'])

    # Create control system
    candidate_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12])
    candidate_scoring = ctrl.ControlSystemSimulation(candidate_ctrl)

    return candidate_scoring


def process_candidate(job_position,job_requirements,calculate_skill_score,calculate_project_relevance,fuzzy_candidate_Scoring):
    # Extract data
    with open("temp_resume.json", "r") as f:
        candidate_data = json.load(f)  # ✅ Parses the JSON into a Python dictionary
    # print(candidate_data)
    skills_data = candidate_data["skills"]
    # print(skills_data)
    experience_years = float(candidate_data["total_experience"])
    # print(experience_years)
    project_categories = candidate_data["project_category"]
    # print(project_categories)
    job_position = job_position
    # print(job_position)
    
    # Calculate input values for fuzzy system
    # print("po")
    skill_score = calculate_skill_score(skills_data, job_requirements)
    # print("1")
    proj_relevance = calculate_project_relevance(project_categories, job_position)
    # print("2")
    # print(f"Calculated inputs for fuzzy system:")
    # print(f"Skill Score: {skill_score:.2f}/100")
    # print(f"Experience: {experience_years} years")
    # print(f"Project Relevance: {proj_relevance:.2f}/100")
    
    candidate_scoring = fuzzy_candidate_Scoring()

    # Input values to fuzzy system
    candidate_scoring.input['skills'] = skill_score
    candidate_scoring.input['experience'] = experience_years
    candidate_scoring.input['project_relevance'] = proj_relevance
    
    # Compute fuzzy result
    candidate_scoring.compute()
    
    # Get defuzzified result
    final_score = candidate_scoring.output['candidate_score']
    
    return final_score

# Process the sample candidate
# final_score = process_candidate(candidate_data,job_requirements)
# print(f"\nFinal candidate score after defuzzification: {final_score:.2f}/100")


if __name__ == "__main__":
    function_name = sys.argv[1] 
    job_position = sys.argv[2]
    job_requirements = json.loads(sys.argv[3])
    # print(type(job_requirements))

    # dataPath = r"C:\Users\Admin\Desktop\AVI\CODING\PROJECTS\Resume_Ranking_System\analysis_data\output.json"

    # # Example data to write (you can modify this as per your requirement)
    # data_to_write = {"message": "Hello, this is a test write!"}

    # # Open the file in write mode and write JSON data
    # with open(dataPath, 'w') as file:
    #     json.dump(data_to_write, file, indent=4)

    # print("Data written successfully.")

    if function_name == "process_candidate":
        print(process_candidate(job_position,job_requirements,calculate_skill_score,calculate_project_relevance,fuzzy_candidate_Scoring))
    else:
        print("Invalid function name")
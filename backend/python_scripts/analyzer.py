import fitz
import os   
import re
from groq import Groq
import json
import unicodedata

import fitz
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as pdf:
            for page in pdf:
                # Extract text with sorting
                page_text = page.get_text("text", sort=True)
                
                # Normalize Unicode characters
                page_text = unicodedata.normalize('NFKD', page_text)
                
                # Remove or replace problematic characters
                page_text = page_text.encode('ascii', 'ignore').decode('ascii')
                
                text += page_text + "\n"

        return text

    except Exception as e:
        print(f"Error: {e}")
        return ""

def analyse_resume_with_llm(resume_text: str, job_description: str) -> dict:
    API_KEY="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"
    temp_file = "temp_resume.json"
    prompt = f"""
        You are an AI assistant specialized in analyzing resumes for software engineering job applications. Your goal is to evaluate a given resume against a specific job description and extract key insights.

        Your tasks:
        1. Extract Candidate Information:
           - Full Name
           - Email
           - Phone Number
        
        2. Skill Categorization: Identify all skills mentioned in the resume, including both technical skills and soft skills, as well as relevant courses studied in college. Classify them into three categories based on their relevance to the job description:
        Low: Skills that are mentioned in the resume but are less relevant to the specific job role. These could be generic programming languages or tools that do not significantly impact the job.
        Medium: Core skills that are essential and mandatory for the job role as per the job description. These include the primary technologies, frameworks, and methodologies required for the position.
        High: Advanced or specialized skills that significantly enhance the candidate's profile. These are highly desirable and give a competitive edge, such as expertise in Docker, Kubernetes, cloud platforms (AWS, GCP, Azure), CI/CD, deep mastery of Git & GitHub, and performance optimization techniques.

        3. Experience Calculation: Extract total years of experience based on work history.
        
        4. Project Categorization: Identify and categorize projects into domains (e.g., AI, Web Dev, DevOps, etc.).
        
        5. Certifications: Extract any certifications mentioned in the resume.
        
        6. Resume Ranking: Assign a relevance score (0-100) based on job description.
        
        Resume:
        {resume_text}

        Job Description:
        {job_description}
        
        Provide the output in valid JSON format with this structure:
        {{
            "candidate_name": "<full_name>",
            "email": "<email>",
            "phone": "<phone>",
            "rank": "<percentage>",
            "skills": {{"low": ["skill1", "skill2"], "medium": ["skill1", "skill2"], "high": ["skill1", "skill2"]}},
            "total_experience": "<years>",
            "project_category": ["category1", "category2"],
            "certifications": ["certification1", "certification2"],
        }}

        give a direct parsable output in json format ,no extra char ,no new line char etc 
    """
    try:
        client = Groq(api_key=API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages = [{'role' : 'user','content' : prompt}],
            temperature=0.7,
            response_format={'type': "json_object"}
        )
        # result = response.choices[0].message.content
        # return json.dumps(result)
    
        result = json.loads(response.choices[0].message.content)
        
        # Save to temp file
        with open(temp_file, "w") as f:
            json.dump(result, f)

        print(f"Data written to {temp_file}")  # Optional, just for logs

        # except Exception as e:
        #     with open(temp_file, "w") as f:
        #         json.dump({"error": str(e)}, f)



    except Exception as e:
        print(e)


# def analyse_resume_with_llm(resume_text:str,job_description:str,
#     API_KEY = "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") -> dict :
#     prompt = f"""
#         You are an AI assistant specialized in analyzing resumes for software engineering job applications. Your goal is to evaluate a given resume against a specific job description and extract key insights.

#         Your tasks:
#         1. Skill Categorization: Identify all skills mentioned in the resume, including both technical skills and soft skills, as well as relevant courses studied in college. Classify them into three categories based on their relevance to the job description:
#         Low: Skills that are mentioned in the resume but are less relevant to the specific job role. These could be generic programming languages or tools that do not significantly impact the job.
#         Medium: Core skills that are essential and mandatory for the job role as per the job description. These include the primary technologies, frameworks, and methodologies required for the position.
#         High: Advanced or specialized skills that significantly enhance the candidate's profile. These are highly desirable and give a competitive edge, such as expertise in Docker, Kubernetes, cloud platforms (AWS, GCP, Azure), CI/CD, deep mastery of Git & GitHub, and performance optimization techniques.

#         2. Experience Calculation: Extract and calculate the total years of experience based on the candidate's work history, ensuring you consider all relevant job roles.

#         3. Project Categorization: Identify and categorize the candidate's projects based on their domain. Common categories include:
#         AI & Machine Learning
#         Web Development
#         Cloud Computing & DevOps
#         Cybersecurity
#         Data Science & Analytics
#         Embedded Systems & IoT
#         Blockchain & FinTech

#         4. Resume Ranking: Assign a relevance score (0 to 100) that reflects how well the candidate's resume matches the job description.        

#         Ensure your analysis is structured, objective, and data-driven, avoiding bias while ranking resumes.

        # Resume:
        # {resume_text}

        # Job Description:
        # {job_description}

#         Provide the output in valid JSON format with this strucure :
#         {{
#             "rank" : "<percentage>",
#             "skills": [["low" : "skill1", "skill2", "skill3"],["medium : "skill1", "skill2", "skill3"],["high" : "skill1", "skill2", "skill3"]],
#             "total_experience": "<number of years>",
#             "project_category": ["category1","category2",....]
#         }}

#         give a direct parsable output in json format ,no extra char ,no new line char etc 

#     """ 

#     try:
#         client = Groq(api_key=API_KEY)
#         response = client.chat.completions.create(
#             model= "llama-3.3-70b-specdec",
#             messages = [{'role' : 'user','content' : prompt}],
#             temperature=0.7,
#             response_format={'type': "json_object"}
#         )
#         result = response.choices[0].message.content
#         return json.loads(result)
    
#     except Exception as e:
#         print(e)

def analyse_job_description_with_llm(job_description:str) -> dict :
    API_KEY = "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"
    temp_file = "temp_job_desc.json"
    prompt = f"""
        You are an AI assistant specialized in analyzing resumes for software engineering job applications. Your goal is to evaluate a given resume against a specific job description and extract key insights.

        Your tasks:

        1. Extract the title of the job role from the job_description.

        2. Skill Categorization: Identify all skills mentioned in the job_description, including both technical skills and soft skills.
        Classify acc to the key words used like expertise,profecient,prominent,required,mandatory,essential,desired,preferred,good to have,optional,etc. and give them 
        a score from 0 to 1.0 based on the importance of the skill to the job role.
        Take help of the given eg. to understand the scoring system.
        For Eg : 
        jobTitle = "Python Developer"
        job_requirements = [
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
        ]
        
        Ensure your analysis is structured, objective, and data-driven, avoiding bias.

        Job Description:
        {job_description}

        Provide the output in valid JSON format with this strucure :
        {{
            "jobTitle" : "<job_title>",
            "jobSkills": {{
                "skill1": 0.9,
                "skill2": 0.3,
                "skill3": 0.5
            }}
        }}

        give a direct parsable output in json format ,no extra char ,no new line char etc 


    """ 

    try:
        client = Groq(api_key=API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages = [{'role' : 'user','content' : prompt}],
            temperature=0.7,
            response_format={'type': "json_object"}
        )
        # result = response.choices[0].message.content
        # return json.dumps(result)
    
        result = json.loads(response.choices[0].message.content)
        
        # Save to temp file
        with open(temp_file, "w") as f:
            json.dump(result, f)

        print(f"Data written to {temp_file}")  # Optional, just for logs

        # except Exception as e:
        #     with open(temp_file, "w") as f:
        #         json.dump({"error": str(e)}, f)



    except Exception as e:
        print(e)


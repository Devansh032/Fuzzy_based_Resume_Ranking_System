
from analyzer import extract_text_from_pdf,analyse_resume_with_llm,analyse_job_description_with_llm
import json
import sys

def process_resume(pdf_path,job_description) :
    try : 
        resume_text = extract_text_from_pdf(pdf_path)
        data = analyse_resume_with_llm(resume_text,job_description)
        return data
    except Exception as e:
        print(e)
        return None
    
def process_job_description(job_description) :
    try : 
        job_data = analyse_job_description_with_llm(job_description)
        return job_data
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    function_name = sys.argv[1] 
    resume_path = sys.argv[2]
    job_description = sys.argv[3]

    if function_name == "process_resume":
        print(process_resume(resume_path, job_description))  # Output will be read by Node.js
    elif function_name == "process_job_description":
        print(process_job_description(job_description))
    else:
        print("Invalid function name")
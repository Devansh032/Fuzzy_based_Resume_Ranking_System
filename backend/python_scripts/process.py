
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
    
def process_job_description(job_description_path) :
    try : 
        job_description = extract_text_from_pdf(job_description_path)
        job_data = analyse_job_description_with_llm(job_description)
        return job_data
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    function_name = sys.argv[1] 
    resume_path = r"C:\Users\Admin\Desktop\AVI\CODING\PROJECTS\Resume_Ranking_System\backend" + "\\" + sys.argv[2]
    job_description_path = r"C:\Users\Admin\Desktop\AVI\CODING\PROJECTS\Resume_Ranking_System\backend" + "\\" + sys.argv[3]
    job_description = sys.argv[3]



    dataPath = r"C:\Users\Admin\Desktop\AVI\CODING\PROJECTS\Resume_Ranking_System\analysis_data\output.json"

    # Example data to write (you can modify this as per your requirement)
    data_to_write = {"message": "Hello, this is a test write!"}

    # Open the file in write mode and write JSON data
    with open(dataPath, 'w') as file:
        json.dump(data_to_write, file, indent=4)

    print("Data written successfully.")

    if function_name == "process_resume":
        print(process_resume(resume_path, job_description))
    elif function_name == "process_job_description":
        print(process_job_description(job_description_path))
    else:
        print("Invalid function name")
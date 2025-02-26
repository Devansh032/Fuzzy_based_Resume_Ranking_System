import fitz
import os   
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text.strip()

path = r"resume_uploaded\Resume_Data_Science_Devansh_Singhal (5).pdf"
print(extract_text_from_pdf(path))


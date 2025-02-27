# pymuPDF
import fitz 
import re
from fuzzywuzzy import fuzz

def extract_text(pdf_path) :
    text = ""
    with fitz.open(pdf_path) as doc :
        for page in doc : 
            text += page.get_text("text") + "\n"
    return text.lower()


resume_text = extract_text(r"resume_uploaded\Resume_Data_Science_Devansh_Singhal (5).pdf")
print(resume_text)


def extract_resume_section(text):
    # Define section headers (common in resumes)
    section_mapping = {
        "personal info." : ["personal info."],
        "Skills": ["Technical Skills", "Soft Skills", "Hard Skills", "Programming Skills", "Skills", "Coursework/Skills"],
        "Experience": ["Work Experience", "Employment History", "Experience"],
        "Education": ["Academic Background", "Degrees", "Education"],
        "Projects": ["Personal Projects", "Academic Projects", "Work Projects", "Research Projects", "Projects"],
        "Certifications": ["Certifications"]
    }
    
    # Precompute a lookup dictionary for exact & fuzzy matching
    section_lookup = {}
    for main_label, synonyms in section_mapping.items():
        for synonym in synonyms:
            section_lookup[synonym.lower()] = main_label.lower()  # Store lowercase for case-insensitive lookup

    lines = text.split('\n')
    all_section = [["personal info.","personal info."]]
    
    for line in (lines):
        line_lower = line.strip().lower()

        # Step 1: Exact Match Check
        if line_lower in section_lookup:
            all_section.append([line_lower,line_lower])
            continue  # Skip further processing

        # Step 2: Fuzzy Matching (Only if No Exact Match)
        best_match = None
        best_score = 0
        for synonym in section_lookup.keys():
            similarity = fuzz.ratio(line_lower, synonym)
            if similarity > best_score:
                print(".............................................")
                # print(similarity)
                # print(line_lower)
                # print(synonym)
                best_score = similarity
                best_match = line_lower

        if best_match and best_score > 70:  # Adjust threshold if needed
            all_section.append([best_match,synonym])
            print(best_score)
            print(line_lower)
            print(synonym)

    # Step 3: Extract Resume Sections**
    all_section.append(["garbage","garbage"])  # Dummy section to handle the last segment
    dic = {}
    itr = 0

    print(all_section)

    for i in range(len(all_section) - 1):
        current_section = []

        # Get the mapped section name
        section_name = section_lookup.get(all_section[i][1])

        if section_name and section_name not in dic:
            # Only initialize if it does not exist
            print(section_name)
            dic[section_name] = []

        for index in range(itr, len(lines)):
            if all_section[i + 1][0] == lines[index]:
                itr = index + 1
                break
            current_section.append(lines[index])

        dic[section_name] += current_section

    return dic

# Extract structured sections
resume_sections = extract_resume_section(resume_text)

print("------------------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------------------")

# # Print extracted sections
# for section, content in resume_sections.items():
#     print(f"\n🔹 {section}:\n", "\n".join(content))

# Print extracted sections with key-value pairs
# for key, value in resume_sections.items():
#     print(f"Section: {key}")
#     for line in value:
#         print(f"  {line}")


print(resume_sections["certifications"])

print(resume_sections.keys())



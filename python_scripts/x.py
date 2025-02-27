import fitz  # PyMuPDF for PDF text extraction
import re

def extract_text_from_pdf(pdf_path):
    """Extracts and normalizes text from a PDF file."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text.lower().strip()

def extract_resume_sections(pdf_path):
    """Extracts structured sections from a resume PDF using a lookup-based approach."""
    
    # Load resume text
    resume_text = extract_text_from_pdf(pdf_path)
    lines = resume_text.split("\n")

    # Define section mappings (lookup table for different section headers)
    section_mapping = {
        "Personal Info": ["personal info"],
        "Skills": ["technical skills", "soft skills", "hard skills", "programming skills", "skills", "coursework/skills"],
        "Experience": ["work experience", "employment history", "experience"],
        "Education": ["academic background", "degrees", "education"],
        "Projects": ["personal projects", "academic projects", "work projects", "research projects", "projects"],
        "Certifications": ["certifications"]
    }

    # Create a lookup dictionary for fast section matching
    section_lookup = {}
    for main_label, synonyms in section_mapping.items():
        for synonym in synonyms:
            section_lookup[synonym] = main_label  # Map all variations to a single section name

    # Compile regex pattern to match any section title
    section_pattern = re.compile(r"(?i)(" + "|".join(section_lookup.keys()) + r")\b")

    # Detect section headers and store their indices
    section_indices = {}
    for i, line in enumerate(lines):
        match = section_pattern.search(line)
        if match:
            section_indices[i] = section_lookup[match.group(0).strip().lower()]  # Store mapped section name

    # Extract structured sections
    resume_sections = {}
    sorted_indices = sorted(section_indices.keys())

    for i in range(len(sorted_indices)):
        start_idx = sorted_indices[i]
        section_name = section_indices[start_idx]  # Get standardized section name

        # Determine end index (start of next section or end of document)
        end_idx = sorted_indices[i + 1] if i + 1 < len(sorted_indices) else len(lines)

        # Store the section content
        resume_sections.setdefault(section_name, []).extend(lines[start_idx + 1:end_idx])

    return resume_sections

# Example usage:
resume_sections = extract_resume_sections(r"resume_uploaded\Resume_Data_Science_Devansh_Singhal (5).pdf")

# Print structured sections
for section, content in resume_sections.items():
    print(f"\n🔹 {section.upper()}:\n", "\n".join(content))

import os
import spacy
import pdfplumber
from docx import Document
import tempfile
import re
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set.")

client = Groq(api_key=GROQ_API_KEY)

#extract text from PDF and DOCX files
def extract_text(file_path, suffix):
    text = ""
    if suffix == ".pdf":
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # Add a space after each page
                text += page.extract_text(layout=True) + " " 
    
    elif suffix == ".docx":
        doc = Document(file_path)
        # Force a space/newline between paragraphs
        text_parts = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        
        for table in doc.tables:
            for row in table.rows:
                # Force spaces between table cells
                row_content = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                text_parts.append(" ".join(row_content))
        
        # Use " \n " to ensure words at the end of a line don't touch the next line
        text = " \n ".join(text_parts)
    return text

# Remove personally identifiable information from the resume before sending to the AI for analysis
def sanitize_resume(text):
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'\+?\d[\d\s\-]{8,}\d', '', text)
    return text

def fix_merged_words(text):
    # Splits "SUMMARYMotivated" -> "SUMMARY Motivated"
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # Splits "SKILLSPython" -> "SKILLS Python"
    text = re.sub(r'([A-Z]{2,})([A-Z][a-z])', r'\1 \2', text)
    return text

def clean_text_minimal(text):
    # For dense embeddings, we want to preserve as much context as possible, so we only do basic cleaning
    text = fix_merged_words(text) 
    return text.lower().strip()

# clean text with spaCy
def clean_text_sparse(text):
    nlp = spacy.load("en_core_web_sm")
    text = fix_merged_words(text)
    doc = nlp(text.lower())
    return " ".join([t.lemma_ for t in doc if not t.is_stop and not t.is_punct])

#generate embeddings and Similarity Check 
def similarity_check(safe_resume, safe_jd, clean_resume, clean_jd, model):

    #Generate Embeddings
    resume_vector = model.embed_query(safe_resume)
    jd_vector = model.embed_query(safe_jd)
    # Similarity Check 
    # Reshape for the cosine_similarity function
    r_vec = np.array(resume_vector).reshape(1, -1)
    j_vec = np.array(jd_vector).reshape(1, -1)
    #calculate cosine similarity
    dense_score = cosine_similarity(r_vec, j_vec)[0][0]

    # TF-IDF Similarity as a fallback for cases where embeddings might not capture nuances
    tfidf = TfidfVectorizer()
    try:
        tfidf_matrix = tfidf.fit_transform([clean_resume, clean_jd])
        sparse_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except Exception:
        sparse_score = dense_score
    print(f"Dense: {dense_score}, Sparse: {sparse_score}")
    # Combine dense and sparse scores with weighted average
    match_percentage = round(((0.8 * dense_score) + (0.2 * sparse_score))* 100, 2)
    return match_percentage

def analyze_resume(resume_text, jd_text):
    prompt = f"""
    You are an AI Resume Career Coach. Compare the RESUME and JOB DESCRIPTION.
    Return ONLY valid JSON.
    Do not include markdown, explanations, or extra text.
    Provide actionable improvements in EXACTLY this JSON format:
    {{
       
        "matched_skills": ["Skill A", "Skill B"],
        "missing_skills": ["Skill C", "Skill D"],
        "sentence_improvements": [
            {{"original": "sentence 1", "improved": "better version 1"}},
            {{"original": "sentence 2", "improved": "better version 2"}},
            {{"original": "sentence 3", "improved": "better version 3"}}
        ],
        "structural_tips": ["TIP: Brief title. EXPLANATION: Why this matters. EXAMPLE: How to do it."]
    }}
     Rules for structural_tips:
    1. Don't just give a title. Explain the benefit.
    2. Provide a concrete example based on the user's data.

    Resume: {resume_text}
    Job Description: {jd_text}
    """
    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],temperature=0.1,
    )
    result = response.choices[0].message.content
    clean_json = result.replace( "```json", "").replace("```", "").strip()
        
    try:
        return json.loads(clean_json)
    except Exception as e:
        print(f"JSON Error: {e}")
        # Return fallback data to prevent crash
        return {
            "matched_skills": [],
            "missing_skills": [],
            "sentence_improvements": [],
            "structural_tips": ["Error parsing AI response"]
        }

def calculate_ats_score(text, file_extension):
    score = 0
    details = []

    # Contact Info Check (25 points)
    has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+', text))
    has_phone = bool(re.search(r'\+?\d[\d -]{8,12}\d', text))
    has_linkedin = bool(re.search(r'linkedin\.com/in/[a-zA-Z0-9_-]+', text))
    if has_email and has_phone and has_linkedin:
        score += 25
        details.append("✅ Complete contact info found (Email, Phone, LinkedIn).")
    elif has_email and has_phone:
        score += 15
        details.append("⚠️ Email and Phone found, but adding LinkedIn could improve your score.")
    else:
        score += 5
        details.append("❌ Major contact details (Email or Phone) are missing.")

    # Section Header Check (25 points)
    sections = {
        "Experience": ["experience", "employment", "work history", "professional background"],
        "Education": ["education", "academic", "qualifications"],
        "Skills": ["skills", "technical proficiencies", "expertise"],
        "Projects": ["projects", "personal work", "portfolio"]
    }
    
    found_count = 0
    for section, keywords in sections.items():
        if any(kw in text.lower() for kw in keywords):
            found_count += 1
    
    # Calculate score based on found standard sections
    score += (found_count / len(sections)) * 25
    
    if found_count < 3:
        details.append("⚠️ Missing standard section headers (e.g., Experience, Education). Use standard titles to help ATS scan your resume.")
    
    # Word Count Check (25 points)
    word_count = len(text.split())
    if word_count < 400:
        details.append("⚠️ Content is too short (under 400 words); add more details about your achievements.")
    elif word_count > 1000:
        details.append("⚠️ Content is too long (over 1000 words); try to condense your experience.")
    else:
        score += 25
        details.append("✅ Ideal document length for ATS readability.")
    
    # File Format Check (25 points)
    if file_extension.lower() in ['.pdf', '.docx']:
        score += 25
        details.append(f"✅ {file_extension.upper()} is an ATS-compatible format.")
    else:
        details.append("❌ Non-standard format. Use PDF or DOCX for better parsing.")
    
    return int(score), details

def process_uploaded_file(uploaded_file,job_description):
    model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    suffix = ".pdf" if uploaded_file.filename.endswith('.pdf') else ".docx"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_path = tmp_file.name

    raw_text = extract_text(tmp_path, suffix)
    os.unlink(tmp_path)

    if not raw_text.strip():
        raise ValueError("Could not extract text from resume.")
    

    #remove private info and clean text for better analysis  
    safe_resume = sanitize_resume(raw_text) 
    # Dense inputs
    dense_res = clean_text_minimal(safe_resume)
    dense_jd = clean_text_minimal(job_description)

    # Sparse inputs
    sparse_res = clean_text_sparse(safe_resume)
    sparse_jd = clean_text_sparse(job_description)

    match_percentage = similarity_check(dense_res, dense_jd, sparse_res, sparse_jd, model)
    ats_score, ats_details = calculate_ats_score(raw_text, suffix)
    analysis = analyze_resume(safe_resume, job_description)

     # Inject the ATS report data into the analysis dictionary
    analysis['ats_score'] = ats_score
    analysis['ats_details'] = ats_details

    return match_percentage, analysis
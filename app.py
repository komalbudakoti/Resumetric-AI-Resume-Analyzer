from flask import Flask, render_template, request
from resume_analyzer import process_uploaded_file

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analyze')
def index():
    # This is your current uploader page
    return render_template('analyze.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files or 'job_description' not in request.form:
        return "Please upload a resume and provide a job description."
    
    uploaded_file = request.files['resume']

    if not allowed_file(uploaded_file.filename):
        return "Only PDF and DOCX files are allowed."
    
    job_description = request.form['job_description']

    if uploaded_file.filename == '':
        return "Please select a file to upload."
    
    try:
        match_percentage, analysis = process_uploaded_file(uploaded_file, job_description)
    except Exception as e:
        return f"An error occurred: {str(e)}"

    return render_template(
        "result.html",
        match_percentage=match_percentage,
        ats_score=analysis.get("ats_score", 0),
        ats_details=analysis.get("ats_details", []),
        matched_skills=analysis["matched_skills"],
        missing_skills=analysis["missing_skills"],
        sentence_improvements=analysis["sentence_improvements"],
        structural_tips=analysis["structural_tips"]
    )

if __name__ == "__main__":
    app.run(debug=False)
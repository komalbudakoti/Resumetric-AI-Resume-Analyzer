# Resume Analyzer

This project is a Flask-based resume analyzer that accepts a PDF or DOCX resume upload, receives a pasted job description, and returns a similarity match score with detailed analysis.

## What it does

- Upload a PDF or DOCX resume
- Paste a job description
- Extract text from the resume
- Compute semantic similarity using HuggingFace embeddings through `langchain-community`
- Combine similarity with TF-IDF fallback scoring
- Generate ATS-style resume feedback using Groq AI chat completions
- Display matched skills, missing skills, sentence improvements, and structural tips

## Project files

- `app.py` — Flask application routes and upload handling
- `resume_analyzer.py` — resume extraction, cleaning, similarity scoring, ATS scoring, and AI feedback
- `templates/` — HTML templates for home, analyze, about, and result pages
- `static/style.css` — styling for the web interface

## Requirements

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

Then install the spaCy English model:

```bash
python -m spacy download en_core_web_sm
```

## Configuration

Create a `.env` file in the project root with your Groq API key:

```env
GROQ_API_KEY=your_api_key_here
```

## Running the app

Start the Flask server:

```bash
python app.py
```

Open your browser at `http://127.0.0.1:5000/`.

## Notes

- The resume parser uses `pdfplumber` for PDF extraction and `python-docx` for DOCX extraction.
- The similarity engine uses SentenceTransformer embeddings through `langchain-community`.
- The AI feedback is generated with Groq chat completions and expects `GROQ_API_KEY`.
- This project is designed for text-based resumes, not scanned images.

## Troubleshooting

- If resume extraction fails, confirm your file is not a scanned image.
- If the Flask app fails to start, ensure dependencies are installed and your `.env` file is present.
- If spaCy fails to load `en_core_web_sm`, rerun the model download command.

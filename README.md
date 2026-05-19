# ResumeAnalazer

A small Streamlit-based resume analysis app that extracts and evaluates resume content to provide insights and recommendations.

## Features
- Upload resume files (PDF/DOCX) and extract text
- Analyze skills and match against job requirements
- Provide scoring and suggestions
- Uses ML/NLP libraries for embeddings and classification

## Installation
1. Create a Python virtual environment (recommended):

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. If using spaCy model, install it (if not bundled):

```bash
python -m pip install "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl"
python -m spacy download en_core_web_sm
```

## Running the app

```bash
streamlit run app.py
```
Then open the provided local URL in your browser.

## Dependencies
The project lists the following dependencies in `requirements.txt`:

- torch
- torchvision
- streamlit
- python-docx>=0.8.11
- pdfplumber>=0.10.0
- numpy>=1.26.0
- scikit-learn>=1.3.2
- langchain-huggingface
- groq>=0.2.0
- sentence-transformers>=2.2.2
- nltk
- spacy>=3.7.5,<3.8.0
- en_core_web_sm (spaCy model wheel)

## Project Structure
- `app.py` - Streamlit or Flask front-end runner
- `resume_analyzer.py` - Core resume parsing and analysis logic
- `components.py` - UI components for the app
- `styles.py` - Styling utilities

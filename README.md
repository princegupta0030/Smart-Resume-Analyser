# Smart Resume Analyzer

A working MVP web application built with Streamlit that allows a user to upload a resume (PDF/DOCX) and paste a job description to analyze how well the resume matches the job.

This repository contains the foundational structure of the project. Advanced analysis logic will be integrated in future sessions.

## Features (MVP Foundation)
- Clean, professional Streamlit interface.
- Resume upload supporting **PDF** and **DOCX** formats.
- Parsing logic leveraging `PyMuPDF` and `python-docx` to extract text from resumes.
- Full AI integration using Gemini 1.5 Flash to extract skills, calculate match scores, and provide explanations.

## Project Structure
```text
smart-resume-analyzer/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules for Python/Streamlit
├── src/
│   ├── __init__.py
│   ├── resume_parser.py        # Core text extraction (PDF & DOCX)
│   ├── skill_extractor.py      # Placeholder: Skill extraction logic
│   ├── matcher.py              # Placeholder: Resume vs Job Matching logic
│   └── scoring.py              # Placeholder: Match scoring logic
└── tests/
    └── test_basic.py           # Pytest tests for the resume parser
```

## Installation Instructions

1. Ensure you have Python 3.8+ installed.
2. Clone this repository and navigate to the project root.
3. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run the App

1. Ensure your virtual environment is active.
2. Start the Streamlit application:
   ```bash
   PYTHONPATH=. streamlit run app.py
   ```
3. Open the provided Local URL (typically `http://localhost:8501`) in your browser.

## Running Tests

To run the basic parsing tests using `pytest`, use the following command:
```bash
PYTHONPATH=. pytest tests/test_basic.py
```

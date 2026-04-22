# PYQ Smart Assistant 

AI-powered previous year question paper assistant demo 
Covers Semester 6, 7, 8 — B.Tech IT — 2023 papers.

## What this demo tests

- Loads all 3 question paper PDFs (18 subjects across 3 semesters)
- System finds the relevant paper and generates a structured answer via Gemini AI
- Browse questions paper-by-paper, or search any keyword across all papers

---

## Setup (one time)

### 1. Install system dependencies

```bash
# Ubuntu / Debian / WSL
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract
```

### 2. Clone and install Python packages

```bash
git clone https://github.com/ANSHRAJCODE/pdfqanda.git
cd pdfqanda

pip install -r requirements.txt
```

### 3. Add Gemini API key

Get a free key at https://aistudio.google.com

```bash
copy .env.example .env
# Open .env in any text editor and set:
# GEMINI_API_KEY=your_key_here
```

Alternatively, the key can be entered directly in the app sidebar — no .env needed.

### 4. Add the question paper PDFs

```bash
mkdir papers
# Copy the 3 PDF files into this folder:
#   IT_Question_Papers_2022-2023_6th_Semester.pdf
#   IT_Question_Papers_2022-2023_7th_Semester.pdf
#   IT_Question_Papers_2022-2023_8th_Semester.pdf
```

The PDFs are excluded from this repository (.gitignore). Add your own copies.

### 5. Run

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

**First run:** OCR processing takes approximately 1–2 minutes per PDF.
After that, results are cached — subsequent runs start instantly.

---

## Papers loaded (18 subjects)

### Semester 8 (7 papers)
| Code | Subject |
|------|---------|
| ETCS-404 | Human Computer Interaction |
| ETEC-404 | Satellite Communication |
| ETEC-406 | Ad Hoc and Sensor Networks |
| ETHS-402 | Human Values and Professional Ethics-II |
| ETIT-402 | Mobile Computing |
| ETIT-410 | Soft Computing |
| ETIT-422 | GPS and GIS |

### Semester 7 (5 papers)
| Code | Subject |
|------|---------|
| ETEC-405 | Wireless Communication |
| ETHS-419 | Sociology and Elements of Indian History for Engineers |
| ETIT-401 | Advanced Computer Networks |
| ETIT-403 | Cryptography and Network Security |
| ETIT-427 | Advanced Database Administration |

### Semester 6 (6 papers)
| Code | Subject |
|------|---------|
| ETCS-302 | Compiler Design |
| ETCS-304 | Operating Systems |
| ETCS-308 | Web Engineering / Web Technology |
| ETCS-310/312 | Artificial Intelligence |
| ETEC-310 | Data Communication and Networks |
| ETEE-310 | Microprocessors and Microcontrollers |

---

## Tech stack

| Component | Technology |
|-----------|-----------|
| PDF extraction | PyMuPDF (text layer) + Tesseract OCR (scanned fallback) |
| AI model | Gemini 1.5 Flash — google-genai |
| UI | Streamlit |
| Language | Python 3.10+ |

Note: This is a testing/demo build. The production system will use FastAPI backend,
PostgreSQL with pgvector for semantic search, and a Flutter Android app.

---

## Gemini free tier limits
- 15 requests per minute
- 1 million tokens per day
- No credit card required

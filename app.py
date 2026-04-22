# """
# PYQ Smart Assistant — Supervisor Testing Build
# Covers: 6th, 7th, 8th Semester | B.Tech IT | 2023
# PDFs: 3 files, 18 subjects total

# Stack: PyMuPDF + Tesseract OCR + Gemini 1.5 Flash + Streamlit
# """

# import streamlit as st
# import os
# import re
# import io
# import json
# import hashlib
# import time
# import fitz
# import pytesseract
# from PIL import Image
# from google import genai
# from google.genai import types
# from dotenv import load_dotenv
# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# load_dotenv()

# PAPERS_DIR = "papers"
# CACHE_DIR = "cache"
# CACHE_VERSION = "v2"  # bump this to force re-extraction of all PDFs
# os.makedirs(CACHE_DIR, exist_ok=True)

# st.set_page_config(
#     page_title="PYQ Assistant",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ── Styling: clean, minimal, no emoji ────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

# html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
# #MainMenu, footer, header { visibility: hidden; }
# .block-container { padding: 1.5rem 2rem 2rem; }

# [data-testid="stSidebar"] {
#     background: #111827;
#     border-right: 1px solid #1f2937;
# }
# [data-testid="stSidebar"] * { color: #d1d5db !important; }
# [data-testid="stSidebar"] input {
#     background: #1f2937 !important;
#     border: 1px solid #374151 !important;
#     color: #f9fafb !important;
#     font-family: 'JetBrains Mono', monospace !important;
#     font-size: 0.75rem !important;
#     border-radius: 3px !important;
# }
# [data-testid="stSidebar"] hr { border-color: #1f2937 !important; }

# .main { background: #f9fafb; }

# .app-header {
#     border-bottom: 2px solid #111827;
#     padding-bottom: 0.75rem;
#     margin-bottom: 1.25rem;
# }
# .app-title {
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 1rem;
#     font-weight: 500;
#     color: #111827;
#     letter-spacing: 0.01em;
# }
# .app-meta {
#     font-size: 0.72rem;
#     color: #6b7280;
#     margin-top: 0.2rem;
#     font-family: 'JetBrains Mono', monospace;
# }

# .stTabs [data-baseweb="tab-list"] {
#     gap: 0;
#     background: transparent;
#     border-bottom: 1px solid #e5e7eb;
# }
# .stTabs [data-baseweb="tab"] {
#     font-size: 0.78rem;
#     font-weight: 500;
#     color: #6b7280;
#     padding: 0.55rem 1.1rem;
#     border-bottom: 2px solid transparent;
#     background: transparent;
#     letter-spacing: 0.02em;
# }
# .stTabs [aria-selected="true"] {
#     color: #111827 !important;
#     border-bottom: 2px solid #111827 !important;
#     background: transparent !important;
# }

# .stButton > button {
#     background: #111827 !important;
#     color: #fff !important;
#     border: none !important;
#     border-radius: 3px !important;
#     font-family: 'Inter', sans-serif !important;
#     font-size: 0.8rem !important;
#     font-weight: 500 !important;
#     padding: 0.45rem 1.1rem !important;
#     letter-spacing: 0.02em !important;
# }
# .stButton > button:hover { background: #374151 !important; }

# .stTextArea textarea, .stTextInput > div > div > input {
#     border: 1px solid #d1d5db !important;
#     border-radius: 3px !important;
#     font-size: 0.875rem !important;
#     font-family: 'Inter', sans-serif !important;
#     background: #fff !important;
# }
# .stTextArea textarea:focus, .stTextInput > div > div > input:focus {
#     border-color: #111827 !important;
#     box-shadow: none !important;
# }

# .stSelectbox > div > div {
#     border: 1px solid #d1d5db !important;
#     border-radius: 3px !important;
#     font-size: 0.875rem !important;
# }

# .answer-card {
#     background: #ffffff;
#     border: 1px solid #e5e7eb;
#     border-left: 3px solid #111827;
#     padding: 1.25rem 1.5rem;
#     margin-top: 0.75rem;
#     font-size: 0.875rem;
#     line-height: 1.75;
#     color: #1f2937;
# }
# .source-row {
#     margin-top: 0.75rem;
#     display: flex;
#     flex-wrap: wrap;
#     gap: 0.4rem;
# }
# .source-chip {
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.65rem;
#     background: #f3f4f6;
#     color: #4b5563;
#     padding: 0.2rem 0.5rem;
#     border: 1px solid #e5e7eb;
#     border-radius: 2px;
#     display: inline-block;
# }
# .section-label {
#     font-size: 0.7rem;
#     font-weight: 600;
#     color: #6b7280;
#     text-transform: uppercase;
#     letter-spacing: 0.08em;
#     margin-bottom: 0.4rem;
# }
# .info-row {
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.7rem;
#     color: #6b7280;
#     margin: 0.5rem 0 1rem;
#     padding: 0.4rem 0.75rem;
#     background: #f3f4f6;
#     border-left: 2px solid #d1d5db;
# }
# .q-text {
#     font-size: 0.85rem;
#     color: #1f2937;
#     line-height: 1.65;
#     padding: 0.5rem 0;
# }
# .sidebar-section {
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.65rem;
#     font-weight: 600;
#     color: #6b7280 !important;
#     text-transform: uppercase;
#     letter-spacing: 0.1em;
#     margin: 1rem 0 0.4rem;
# }
# .paper-item {
#     font-size: 0.72rem;
#     color: #9ca3af !important;
#     padding: 0.2rem 0;
#     border-bottom: 1px solid #1f2937;
#     font-family: 'JetBrains Mono', monospace;
#     line-height: 1.4;
# }
# .paper-code { color: #e5e7eb !important; font-weight: 500; }
# </style>
# """, unsafe_allow_html=True)


# # ── Gemini client ─────────────────────────────────────────────────────────────
# def get_gemini_client(api_key: str):
#     if not api_key:
#         return None
#     try:
#         return genai.Client(api_key=api_key)
#     except Exception:
#         return None


# # ── PDF extraction ─────────────────────────────────────────────────────────────
# def ocr_pdf(pdf_path: str, dpi: int = 200) -> str:
#     doc = fitz.open(pdf_path)
#     pages = []
#     mat = fitz.Matrix(dpi / 72, dpi / 72)
#     for i in range(len(doc)):
#         page = doc[i]
#         native = page.get_text("text").strip()
#         if len(native) > 80:
#             pages.append(native)
#         else:
#             pix = page.get_pixmap(matrix=mat)
#             img = Image.open(io.BytesIO(pix.tobytes("png")))
#             pages.append(pytesseract.image_to_string(img, config="--psm 3"))
#     doc.close()
#     return "\n".join(pages)


# def parse_papers(raw_text: str, filename: str) -> list[dict]:
#     """
#     Split combined PDF text into individual subject papers.
#     Each paper starts with 'Paper Code: XXXX  Subject: YYYY'.
#     Handles: hyphens, slashes, missing hyphens in paper codes.
#     """
#     SEM_MAP = {
#         "FIRST": 1, "SECOND": 2, "THIRD": 3, "FOURTH": 4,
#         "FIFTH": 5, "SIXTH": 6, "SEVENTH": 7, "EIGHTH": 8,
#     }

#     header_re = re.compile(
#         r"Paper\s+Code\s*[:\-]?\s*"
#         r"([A-Z]{2,6}[-\s/]?\d{3,4}(?:[/-]\d+)?[A-Z]?)"
#         r"\s+"
#         r"Subject\s*[:\-]?\s*"
#         r"(.+?)(?=\n(?:Time|Max\.?\s*Marks?|Note|Attempt)|\Z)",
#         re.IGNORECASE | re.DOTALL,
#     )
#     sem_re = re.compile(
#         r"(FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH|EIGHTH)\s+SEMESTER",
#         re.IGNORECASE,
#     )
#     year_re = re.compile(
#         r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?"
#         r"|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
#         r"[\s\-]+(\d{4})",
#         re.IGNORECASE,
#     )

#     # Detect semester and year from the file header (first 1500 chars)
#     file_header = raw_text[:1500]
#     sem_m = sem_re.search(file_header)
#     file_sem_num = SEM_MAP.get(sem_m.group(1).upper(), 0) if sem_m else 0
#     file_sem_label = f"Semester {file_sem_num}" if file_sem_num else "Unknown Semester"
#     yr_m = year_re.search(file_header)
#     if not yr_m:
#         yr_m = re.search(r"\b(20\d{2})\b", file_header)
#     file_year = yr_m.group(1) if yr_m else "2023"

#     headers = list(header_re.finditer(raw_text))

#     if not headers:
#         return [{
#             "paper_code": "UNKNOWN",
#             "subject": filename.replace(".pdf", "").replace("_", " ").title(),
#             "semester": file_sem_label,
#             "semester_num": file_sem_num,
#             "year": file_year,
#             "filename": filename,
#             "content": raw_text,
#         }]

#     papers = []
#     for i, match in enumerate(headers):
#         start = match.start()
#         end = headers[i + 1].start() if i + 1 < len(headers) else len(raw_text)
#         section = raw_text[start:end]

#         # Clean up paper code
#         code = re.sub(r"\s+", "", match.group(1)).upper()

#         # Subject: take only the first line, strip trailing whitespace
#         subject_raw = match.group(2).strip()
#         subject = re.sub(r"\s+", " ", subject_raw.split("\n")[0]).strip()[:120]

#         # Semester: per-section first, then file-level
#         sec_sem_m = sem_re.search(section[:800]) or sem_m
#         sem_num = SEM_MAP.get(sec_sem_m.group(1).upper(), 0) if sec_sem_m else file_sem_num
#         sem_label = f"Semester {sem_num}" if sem_num else file_sem_label

#         # Year: per-section first, then file-level
#         sec_yr_m = year_re.search(section[:600])
#         if not sec_yr_m:
#             sec_yr_m = re.search(r"\b(20\d{2})\b", section[:600])
#         year = sec_yr_m.group(1) if sec_yr_m else file_year

#         papers.append({
#             "paper_code": code,
#             "subject": subject,
#             "semester": sem_label,
#             "semester_num": sem_num,
#             "year": year,
#             "filename": filename,
#             "content": section,
#         })

#     return papers


# def pdf_cache_path(pdf_path: str) -> str:
#     mtime = str(os.path.getmtime(pdf_path))
#     key = hashlib.md5((pdf_path + mtime + CACHE_VERSION).encode()).hexdigest()[:12]
#     return os.path.join(CACHE_DIR, f"{key}.json")


# def load_pdf(pdf_path: str) -> list[dict]:
#     cache = pdf_cache_path(pdf_path)
#     if os.path.exists(cache):
#         with open(cache, "r", encoding="utf-8") as f:
#             return json.load(f)
#     raw = ocr_pdf(pdf_path)
#     papers = parse_papers(raw, os.path.basename(pdf_path))
#     with open(cache, "w", encoding="utf-8") as f:
#         json.dump(papers, f, ensure_ascii=False, indent=2)
#     return papers


# def load_all_papers(papers_dir: str) -> list[dict]:
#     pdf_files = sorted(f for f in os.listdir(papers_dir) if f.lower().endswith(".pdf"))
#     if not pdf_files:
#         return []
#     all_papers = []
#     progress = st.progress(0, text="Loading papers...")
#     for idx, fname in enumerate(pdf_files):
#         progress.progress(
#             (idx + 1) / len(pdf_files),
#             text=f"Processing {fname}  ({idx + 1}/{len(pdf_files)})",
#         )
#         all_papers.extend(load_pdf(os.path.join(papers_dir, fname)))
#     progress.empty()
#     return all_papers


# # ── Question extraction ───────────────────────────────────────────────────────
# def extract_questions(content: str) -> list[dict]:
#     """
#     Extract individual questions from paper content.
#     Detects: Q1 compulsory sub-parts, Q2-Q9 main questions, unit boundaries, marks.
#     """
#     UNIT_RE = re.compile(r"UNIT\s*[-–]?\s*(I{1,3}V?|IV|VI?I?I?|\d)", re.IGNORECASE)
#     Q_START_RE = re.compile(r"^\s*Q\.?\s*(\d+)\b", re.IGNORECASE)
#     MARKS_RE = re.compile(r"[\[\(](\d+(?:\.\d+)?)\s*(?:marks?)?\s*[\]\)]", re.IGNORECASE)

#     ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6}

#     questions = []
#     current_lines: list[str] = []
#     current_qnum = ""
#     current_unit = 0
#     current_is_compulsory = False

#     def flush():
#         if not current_lines:
#             return
#         text = " ".join(l.strip() for l in current_lines if l.strip())
#         text = re.sub(r"\s+", " ", text).strip()
#         if len(text) > 30:
#             m = MARKS_RE.search(text)
#             questions.append({
#                 "number": current_qnum,
#                 "text": text,
#                 "marks": float(m.group(1)) if m else None,
#                 "unit": current_unit,
#                 "is_compulsory": current_is_compulsory,
#             })

#     for line in content.split("\n"):
#         stripped = line.strip()

#         # Detect unit boundary
#         unit_m = UNIT_RE.search(stripped)
#         if unit_m and len(stripped) < 30:
#             token = unit_m.group(1).upper()
#             current_unit = ROMAN.get(token, int(token) if token.isdigit() else 0)

#         # Detect new question
#         q_m = Q_START_RE.match(stripped)
#         if q_m:
#             flush()
#             current_lines = [stripped]
#             qnum = int(q_m.group(1))
#             current_qnum = f"Q{qnum}"
#             current_is_compulsory = (qnum == 1)
#         else:
#             current_lines.append(stripped)

#     flush()
#     return questions


# # ── Relevance search ──────────────────────────────────────────────────────────
# def find_relevant(query: str, papers: list[dict], top_k: int = 3) -> list[dict]:
#     words = set(re.findall(r"\b\w{4,}\b", query.lower()))
#     if not words:
#         return papers[:top_k]
#     scored = []
#     for p in papers:
#         hits = sum(1 for w in words if w in p["content"].lower())
#         subj_hits = sum(1 for w in words if w in p["subject"].lower())
#         score = hits + subj_hits * 5
#         if score > 0:
#             scored.append((score, p))
#     scored.sort(key=lambda x: x[0], reverse=True)
#     return [p for _, p in scored[:top_k]]


# # ── Answer generation ─────────────────────────────────────────────────────────
# def generate_answer(client, question: str, papers: list[dict]) -> tuple[str, list[str]]:
#     if not client:
#         return "Gemini API key not configured. Add your key in the sidebar.", []

#     context_parts = []
#     for p in papers:
#         header = f"[{p['paper_code']} | {p['subject']} | {p['semester']} | {p['year']}]"
#         context_parts.append(f"{header}\n{p['content'][:2500].strip()}")
#     context = ("\n\n" + "=" * 50 + "\n\n").join(context_parts)

#     sources = [
#         f"{p['paper_code']} — {p['subject']} ({p['semester']}, {p['year']})"
#         for p in papers
#     ]

#     prompt = f"""You are an expert engineering professor preparing B.Tech students for End Term Examinations.

# The following content is extracted from actual previous year question papers:

# {context}

# QUESTION:
# {question}

# INSTRUCTIONS:
# - Answer at B.Tech engineering level, thoroughly and accurately.
# - If this question or a similar one appears in the papers above, use that context.
# - If the topic is NOT found in these papers, state: "This topic does not appear in the provided question papers." then give a general answer.
# - Use clear headings and structure where the question demands it.
# - Be precise and exam-ready.

# Answer:"""

#     models_to_try = [
#         "gemini-2.5-flash",
#         "gemini-2.5-pro",
#     ]
#     for model_name in models_to_try:
#         for attempt in range(2):
#             try:
#                 response = client.models.generate_content(
#                     model=model_name,
#                     contents=prompt,
#                     config=types.GenerateContentConfig(
#                         temperature=0.3,
#                         max_output_tokens=1500,
#                     ),
#                 )
#                 return response.text, sources
#             except Exception as e:
#                 err = str(e)
#                 if "503" in err or "UNAVAILABLE" in err:
#                     if attempt == 0:
#                         time.sleep(3)
#                         continue
#                     # try next model
#                     break
#                 return f"API error: {err}", []
#     return "Gemini is overloaded right now. Wait 30 seconds and try again.", []


# # ── Sidebar ───────────────────────────────────────────────────────────────────
# def render_sidebar(papers: list[dict]) -> str:
#     with st.sidebar:
#         st.markdown(
#             '<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.85rem;'
#             'font-weight:500;color:#f9fafb;padding:0.25rem 0 0.75rem;">PYQ Assistant</div>',
#             unsafe_allow_html=True,
#         )

#         api_key = st.text_input(
#             "API Key",
#             label_visibility="collapsed",
#             type="password",
#             value=os.getenv("GEMINI_API_KEY", ""),
#             placeholder="Gemini API key...",
#             key="api_key_field",
#         )
#         if api_key:
#             os.environ["GEMINI_API_KEY"] = api_key

#         if not papers:
#             return api_key

#         st.divider()

#         # Group by semester
#         by_sem: dict[int, list] = {}
#         for p in papers:
#             by_sem.setdefault(p["semester_num"], []).append(p)

#         n_sems = len(by_sem)
#         n_subjects = len(papers)
#         st.markdown(
#             f'<div style="font-size:0.7rem;color:#4b5563;font-family:\'JetBrains Mono\','
#             f'monospace;margin-bottom:0.75rem;">'
#             f'{n_subjects} subjects across {n_sems} semesters</div>',
#             unsafe_allow_html=True,
#         )

#         for sem_num in sorted(by_sem.keys()):
#             sem_papers = sorted(by_sem[sem_num], key=lambda x: x["paper_code"])
#             label = f"Semester {sem_num}  ({len(sem_papers)} papers)"
#             with st.expander(label, expanded=False):
#                 for p in sem_papers:
#                     subj = p["subject"][:40] + ("..." if len(p["subject"]) > 40 else "")
#                     st.markdown(
#                         f'<div class="paper-item">'
#                         f'<span class="paper-code">{p["paper_code"]}</span><br>'
#                         f'{subj}</div>',
#                         unsafe_allow_html=True,
#                     )

#     return api_key


# # ── Main app ──────────────────────────────────────────────────────────────────
# def main():
#     if not os.path.exists(PAPERS_DIR):
#         os.makedirs(PAPERS_DIR, exist_ok=True)

#     pdfs = [f for f in os.listdir(PAPERS_DIR) if f.lower().endswith(".pdf")]
#     if not pdfs:
#         st.error("No PDF files found in `papers/` folder. Add your question papers and restart.")
#         st.stop()

#     # Load papers — cached to disk, only OCRs once per file
#     if "papers" not in st.session_state:
#         with st.spinner("Processing PDFs... (cached after first run, takes ~1 min)"):
#             st.session_state["papers"] = load_all_papers(PAPERS_DIR)

#     papers: list[dict] = st.session_state["papers"]

#     if not papers:
#         st.error("Could not extract content from PDFs. Check file quality.")
#         st.stop()

#     api_key = render_sidebar(papers)
#     client = get_gemini_client(api_key)

#     # Compute summary stats
#     sems = sorted(set(p["semester_num"] for p in papers if p["semester_num"] > 0))
#     years = sorted(set(p["year"] for p in papers))
#     year_str = f"{years[0]}" if len(years) == 1 else f"{years[0]}–{years[-1]}"
#     sem_str = ", ".join(str(s) for s in sems)

#     # Header
#     st.markdown(
#         f'<div class="app-header">'
#         f'<div class="app-title">PYQ Smart Assistant</div>'
#         f'<div class="app-meta">'
#         f'{len(papers)} subjects &nbsp;·&nbsp; Sem {sem_str} &nbsp;·&nbsp; {year_str} &nbsp;·&nbsp; {len(pdfs)} PDFs loaded'
#         f'</div></div>',
#         unsafe_allow_html=True,
#     )

#     tab_ask, tab_browse, tab_search = st.tabs(["Ask", "Browse", "Search"])

#     # ── Ask tab ───────────────────────────────────────────────────────────────
#     with tab_ask:
#         st.markdown(
#             '<div class="section-label">Ask any question from your syllabus</div>',
#             unsafe_allow_html=True,
#         )
#         st.markdown(
#             '<div style="font-size:0.8rem;color:#6b7280;margin-bottom:0.75rem;">'
#             'The system searches across all loaded papers and generates a structured answer using Gemini AI.'
#             '</div>',
#             unsafe_allow_html=True,
#         )

#         col_q, col_hint = st.columns([3, 1])
#         with col_q:
#             # Optional subject filter
#             subject_opts = ["All subjects"] + sorted(
#                 set(f"{p['paper_code']}  —  {p['subject']}" for p in papers)
#             )
#             sel_sub = st.selectbox(
#                 "Filter by subject",
#                 subject_opts,
#                 label_visibility="visible",
#             )
#             question = st.text_area(
#                 "Question",
#                 label_visibility="collapsed",
#                 placeholder="Type your question here...",
#                 height=100,
#             )
#             ask_btn = st.button("Get Answer", type="primary")

#         with col_hint:
#             st.markdown(
#                 '<div style="font-size:0.72rem;color:#9ca3af;line-height:2;margin-top:2rem;">'
#                 '<b style="color:#6b7280;display:block;margin-bottom:0.3rem;">Sample questions</b>'
#                 'Explain DES algorithm<br>'
#                 'Explain banker\'s algorithm<br>'
#                 'What is OSI model?<br>'
#                 'Explain TCP three-way handshake<br>'
#                 'What is deadlock? How to avoid it?<br>'
#                 'Explain Bluetooth protocol stack<br>'
#                 'What is fuzzy logic?<br>'
#                 'Explain A* algorithm'
#                 '</div>',
#                 unsafe_allow_html=True,
#             )

#         if ask_btn:
#             if not question.strip():
#                 st.warning("Enter a question.")
#             elif not api_key:
#                 st.warning("Add your Gemini API key in the sidebar.")
#             else:
#                 pool = papers
#                 if sel_sub != "All subjects":
#                     code = sel_sub.split("  —  ")[0].strip()
#                     filtered = [p for p in papers if p["paper_code"] == code]
#                     if filtered:
#                         pool = filtered

#                 with st.spinner("Searching papers and generating answer..."):
#                     relevant = find_relevant(question, pool, top_k=3)
#                     if not relevant:
#                         relevant = papers[:2]
#                     answer, sources = generate_answer(client, question, relevant)

#                 st.markdown(
#                     f'<div class="answer-card">{answer.replace(chr(10), "<br>")}</div>',
#                     unsafe_allow_html=True,
#                 )
#                 if sources:
#                     chips = "".join(f'<span class="source-chip">{s}</span>' for s in sources)
#                     st.markdown(
#                         f'<div class="source-row">{chips}</div>',
#                         unsafe_allow_html=True,
#                     )

#     # ── Browse tab ────────────────────────────────────────────────────────────
#     with tab_browse:
#         st.markdown(
#             '<div class="section-label">Browse questions by paper</div>',
#             unsafe_allow_html=True,
#         )

#         col_s, col_p = st.columns(2)
#         sem_opts = sorted(set(p["semester"] for p in papers),
#                           key=lambda s: next((p["semester_num"] for p in papers if p["semester"] == s), 0))
#         sel_sem = col_s.selectbox("Semester", sem_opts)

#         sem_papers = [p for p in papers if p["semester"] == sel_sem]
#         paper_opts = [f"{p['paper_code']}  —  {p['subject']}" for p in sem_papers]
#         sel_paper_label = col_p.selectbox("Subject / Paper", paper_opts)

#         sel_paper = next(
#             (p for p in sem_papers
#              if f"{p['paper_code']}  —  {p['subject']}" == sel_paper_label),
#             None,
#         )

#         if sel_paper:
#             st.markdown(
#                 f'<div class="info-row">'
#                 f'{sel_paper["paper_code"]} &nbsp;·&nbsp; {sel_paper["subject"]} &nbsp;·&nbsp; '
#                 f'{sel_paper["semester"]} &nbsp;·&nbsp; July {sel_paper["year"]}'
#                 f'</div>',
#                 unsafe_allow_html=True,
#             )

#             questions = extract_questions(sel_paper["content"])

#             if questions:
#                 st.markdown(
#                     f'<div style="font-size:0.72rem;color:#6b7280;margin-bottom:0.5rem;">'
#                     f'{len(questions)} questions detected</div>',
#                     unsafe_allow_html=True,
#                 )
#                 for i, q in enumerate(questions):
#                     label = q["number"] or f"Q{i+1}"
#                     marks_str = f" [{q['marks']} marks]" if q["marks"] else ""
#                     unit_str = f" Unit {q['unit']}" if q["unit"] else ""
#                     tag = " [Compulsory]" if q["is_compulsory"] else ""
#                     preview = q["text"][:75] + ("..." if len(q["text"]) > 75 else "")
#                     with st.expander(f"{label}{unit_str}{marks_str}{tag}  —  {preview}"):
#                         st.markdown(
#                             f'<div class="q-text">{q["text"]}</div>',
#                             unsafe_allow_html=True,
#                         )
#                         if st.button("Generate Answer", key=f"b_ans_{sel_paper['paper_code']}_{i}"):
#                             if not api_key:
#                                 st.warning("Add Gemini API key in sidebar.")
#                             else:
#                                 with st.spinner("Generating..."):
#                                     ans, _ = generate_answer(client, q["text"], [sel_paper])
#                                 st.markdown(
#                                     f'<div class="answer-card">{ans.replace(chr(10), "<br>")}</div>',
#                                     unsafe_allow_html=True,
#                                 )
#             else:
#                 st.info("Could not parse individual questions from this paper. Showing raw extracted text:")
#                 st.code(sel_paper["content"][:3000], language=None)

#     # ── Search tab ────────────────────────────────────────────────────────────
#     with tab_search:
#         st.markdown(
#             '<div class="section-label">Search across all papers</div>',
#             unsafe_allow_html=True,
#         )
#         query = st.text_input(
#             "Search",
#             label_visibility="collapsed",
#             placeholder="Enter a keyword or topic (e.g. deadlock, TCP, neural network, DES...)",
#         )

#         if query:
#             results = find_relevant(query, papers, top_k=10)
#             if results:
#                 st.markdown(
#                     f'<div style="font-size:0.72rem;color:#6b7280;margin-bottom:0.75rem;">'
#                     f'Found in {len(results)} papers</div>',
#                     unsafe_allow_html=True,
#                 )
#                 for p in results:
#                     label = f"{p['paper_code']}  —  {p['subject']}  ({p['semester']}, {p['year']})"
#                     with st.expander(label):
#                         content = p["content"]
#                         idx = content.lower().find(query.lower())
#                         if idx > -1:
#                             s = max(0, idx - 200)
#                             e = min(len(content), idx + 600)
#                             snippet = "..." + content[s:e] + "..."
#                         else:
#                             snippet = content[:700] + "..."
#                         st.code(snippet, language=None)
#                         if st.button(
#                             "Answer from this paper",
#                             key=f"s_ans_{p['paper_code']}",
#                         ):
#                             if not api_key:
#                                 st.warning("Add Gemini API key in sidebar.")
#                             else:
#                                 with st.spinner("Generating..."):
#                                     ans, srcs = generate_answer(client, query, [p])
#                                 st.markdown(
#                                     f'<div class="answer-card">{ans.replace(chr(10), "<br>")}</div>',
#                                     unsafe_allow_html=True,
#                                 )
#             else:
#                 st.info(f'No papers matched "{query}". Try different keywords.')


# if __name__ == "__main__":
#     main()


"""
PYQ Smart Assistant
Semester 6, 7, 8 | B.Tech IT | 2023 | 18 subjects across 3 PDFs
"""

import streamlit as st
import os
import re
import io
import json
import hashlib
import time
import fitz
import pytesseract
from PIL import Image
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

PAPERS_DIR = "papers"
CACHE_DIR = "cache"
CACHE_VERSION = "v4"
os.makedirs(CACHE_DIR, exist_ok=True)

st.set_page_config(page_title="PYQ Assistant", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 2rem; }
[data-testid="stSidebar"] { background: #111827; border-right: 1px solid #1f2937; }
[data-testid="stSidebar"] * { color: #d1d5db !important; }
[data-testid="stSidebar"] input { background: #1f2937 !important; border: 1px solid #374151 !important; color: #f9fafb !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.75rem !important; border-radius: 3px !important; }
[data-testid="stSidebar"] hr { border-color: #1f2937 !important; }
.main { background: #f9fafb; }
.app-header { border-bottom: 2px solid #111827; padding-bottom: 0.75rem; margin-bottom: 1.25rem; }
.app-title { font-family: 'JetBrains Mono', monospace; font-size: 1rem; font-weight: 500; color: #111827; }
.app-meta { font-size: 0.72rem; color: #6b7280; margin-top: 0.2rem; font-family: 'JetBrains Mono', monospace; }
.stTabs [data-baseweb="tab-list"] { gap: 0; background: transparent; border-bottom: 1px solid #e5e7eb; }
.stTabs [data-baseweb="tab"] { font-size: 0.78rem; font-weight: 500; color: #6b7280; padding: 0.55rem 1.1rem; border-bottom: 2px solid transparent; background: transparent; }
.stTabs [aria-selected="true"] { color: #111827 !important; border-bottom: 2px solid #111827 !important; background: transparent !important; }
.stButton > button { background: #111827 !important; color: #fff !important; border: none !important; border-radius: 3px !important; font-size: 0.8rem !important; font-weight: 500 !important; padding: 0.45rem 1.1rem !important; }
.stButton > button:hover { background: #374151 !important; }
.stTextArea textarea, .stTextInput > div > div > input { border: 1px solid #d1d5db !important; border-radius: 3px !important; font-size: 0.875rem !important; background: #fff !important; }
.stSelectbox > div > div { border: 1px solid #d1d5db !important; border-radius: 3px !important; font-size: 0.875rem !important; }
.answer-card { background: #fff; border: 1px solid #e5e7eb; border-left: 3px solid #111827; padding: 1.25rem 1.5rem; margin-top: 0.75rem; font-size: 0.875rem; line-height: 1.75; color: #1f2937; }
.source-row { margin-top: 0.75rem; display: flex; flex-wrap: wrap; gap: 0.4rem; }
.source-chip { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; background: #f3f4f6; color: #4b5563; padding: 0.2rem 0.5rem; border: 1px solid #e5e7eb; border-radius: 2px; display: inline-block; }
.section-label { font-size: 0.7rem; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.4rem; }
.info-row { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #6b7280; margin: 0.5rem 0 1rem; padding: 0.4rem 0.75rem; background: #f3f4f6; border-left: 2px solid #d1d5db; }
.q-text { font-size: 0.85rem; color: #1f2937; line-height: 1.65; padding: 0.5rem 0; }
.paper-item { font-size: 0.72rem; color: #9ca3af !important; padding: 0.2rem 0; border-bottom: 1px solid #1f2937; font-family: 'JetBrains Mono', monospace; line-height: 1.4; }
.paper-code { color: #e5e7eb !important; font-weight: 500; }
</style>
""", unsafe_allow_html=True)


def get_gemini_client(api_key):
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception:
        return None


def ocr_page(page):
    native = page.get_text("text").strip()
    if len(native) > 80:
        return native
    mat = fitz.Matrix(300 / 72, 300 / 72)
    pix = page.get_pixmap(matrix=mat)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    return pytesseract.image_to_string(img, config="--oem 3 --psm 6")


def ocr_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    pages = [ocr_page(doc[i]) for i in range(len(doc))]
    doc.close()
    return pages


def parse_papers(pages, filename):
    SEM_MAP = {"FIRST": 1, "SECOND": 2, "THIRD": 3, "FOURTH": 4,
               "FIFTH": 5, "SIXTH": 6, "SEVENTH": 7, "EIGHTH": 8}

    header_re = re.compile(
        r"Paper\s+(?:Code|C[ao0]de)\s*[:\-]?\s*"
        r"([A-Z]{2,6}[-\s/]?\d{3,4}(?:[/-]\d+)?[A-Z]?)"
        r"[\s\S]{0,80}?"
        r"(?:Subject|Subjeet|Sub[jli1]ect)\s*[:\-]?\s*"
        r"([^\n]{3,100})",
        re.IGNORECASE,
    )
    code_re = re.compile(r"\b(ET(?:CS|EC|EE|IT|HS)-?\d{3,4}(?:/\d+)?)\b", re.IGNORECASE)
    sem_re = re.compile(r"(FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH|EIGHTH)\s+SEMESTER", re.IGNORECASE)
    year_re = re.compile(
        r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?"
        r"|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
        r"[\s\-]+(\d{4})", re.IGNORECASE)

    file_header_text = " ".join(pages[:2])
    sem_m = sem_re.search(file_header_text)
    file_sem_num = SEM_MAP.get(sem_m.group(1).upper(), 0) if sem_m else 0
    file_sem_label = "Semester {}".format(file_sem_num) if file_sem_num else "Unknown Semester"
    yr_m = year_re.search(file_header_text) or re.search(r"\b(20\d{2})\b", file_header_text)
    file_year = yr_m.group(1) if yr_m else "2023"

    papers = []
    current_pages = []
    current_code = None
    current_subject = None
    current_sem_num = file_sem_num
    current_year = file_year

    def flush_paper():
        if current_pages and current_code:
            content = "\n".join(current_pages)
            sem_label = "Semester {}".format(current_sem_num) if current_sem_num else file_sem_label
            papers.append({
                "paper_code": current_code,
                "subject": current_subject or current_code,
                "semester": sem_label,
                "semester_num": current_sem_num,
                "year": current_year,
                "filename": filename,
                "content": content,
            })

    for page_text in pages:
        page_flat = page_text.replace("\n", " ")
        m = header_re.search(page_flat)
        if m:
            flush_paper()
            current_pages = [page_text]
            current_code = re.sub(r"\s+", "", m.group(1)).upper()
            current_subject = re.sub(r"\s+", " ", m.group(2)).strip()[:120]
            pg_sem = sem_re.search(page_text)
            if pg_sem:
                current_sem_num = SEM_MAP.get(pg_sem.group(1).upper(), file_sem_num)
            pg_yr = year_re.search(page_text) or re.search(r"\b(20\d{2})\b", page_text)
            current_year = pg_yr.group(1) if pg_yr else file_year
            continue

        cm = code_re.search(page_text)
        if cm:
            found_code = re.sub(r"\s+", "", cm.group(1)).upper()
            if found_code != current_code:
                is_header = (
                    len(page_text.strip()) < 1500
                    or "END TERM" in page_text.upper()
                    or "EXAMINATION" in page_text.upper()
                    or "ANNUAL EXAMINATION" in page_text.upper()
                )
                if is_header:
                    flush_paper()
                    current_pages = [page_text]
                    current_code = found_code
                    subj_m = re.search(r"Subject\s*[:\-]?\s*([^\n]{3,80})", page_text, re.IGNORECASE)
                    current_subject = re.sub(r"\s+", " ", subj_m.group(1)).strip() if subj_m else found_code
                    pg_sem = sem_re.search(page_text)
                    if pg_sem:
                        current_sem_num = SEM_MAP.get(pg_sem.group(1).upper(), file_sem_num)
                    pg_yr = year_re.search(page_text) or re.search(r"\b(20\d{2})\b", page_text)
                    current_year = pg_yr.group(1) if pg_yr else file_year
                    continue

        if current_code:
            current_pages.append(page_text)
        else:
            current_pages.append(page_text)
            current_code = "UNKNOWN"
            current_subject = filename.replace(".pdf", "").replace("_", " ").title()

    flush_paper()

    merged = {}
    for p in papers:
        code = p["paper_code"]
        if code in merged:
            merged[code]["content"] = merged[code]["content"] + "\n" + p["content"]
        else:
            merged[code] = p
    return list(merged.values())


def pdf_cache_path(pdf_path):
    mtime = str(os.path.getmtime(pdf_path))
    key = hashlib.md5((pdf_path + mtime + CACHE_VERSION).encode()).hexdigest()[:12]
    return os.path.join(CACHE_DIR, "{}.json".format(key))


def load_pdf(pdf_path):
    cache = pdf_cache_path(pdf_path)
    if os.path.exists(cache):
        with open(cache, "r", encoding="utf-8") as f:
            return json.load(f)
    pages = ocr_pdf(pdf_path)
    papers = parse_papers(pages, os.path.basename(pdf_path))
    with open(cache, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)
    return papers


def load_all_papers(papers_dir):
    pdf_files = sorted(f for f in os.listdir(papers_dir) if f.lower().endswith(".pdf"))
    if not pdf_files:
        return []
    all_papers = []
    progress = st.progress(0, text="Loading papers...")
    for idx, fname in enumerate(pdf_files):
        progress.progress((idx + 1) / len(pdf_files),
                          text="Processing {}  ({}/{})".format(fname, idx + 1, len(pdf_files)))
        all_papers.extend(load_pdf(os.path.join(papers_dir, fname)))
    progress.empty()
    return all_papers


def extract_questions(content):
    UNIT_RE = re.compile(r"UNIT\s*[-]?\s*(I{1,3}V?|IV|VI{0,3}|\d)", re.IGNORECASE)
    Q_RE = re.compile(r"^\s*Q\.?\s*(\d+)\b", re.IGNORECASE)
    MARKS_RE = re.compile(r"[\[\(](\d+(?:\.\d+)?)\s*(?:marks?)?\s*[\]\)]", re.IGNORECASE)
    ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6}
    questions = []
    cur_lines, cur_qnum, cur_unit, cur_comp = [], "", 0, False

    def flush():
        if not cur_lines:
            return
        text = re.sub(r"\s+", " ", " ".join(l.strip() for l in cur_lines if l.strip())).strip()
        if len(text) > 30:
            m = MARKS_RE.search(text)
            questions.append({"number": cur_qnum, "text": text,
                               "marks": float(m.group(1)) if m else None,
                               "unit": cur_unit, "is_compulsory": cur_comp})

    for line in content.split("\n"):
        s = line.strip()
        um = UNIT_RE.search(s)
        if um and len(s) < 30:
            tok = um.group(1).upper()
            cur_unit = ROMAN.get(tok, int(tok) if tok.isdigit() else 0)
        qm = Q_RE.match(s)
        if qm:
            flush()
            cur_lines = [s]
            qnum = int(qm.group(1))
            cur_qnum = "Q{}".format(qnum)
            cur_comp = (qnum == 1)
        else:
            cur_lines.append(s)
    flush()
    return questions


def find_relevant(query, papers, top_k=3):
    words = set(re.findall(r"\b\w{4,}\b", query.lower()))
    if not words:
        return papers[:top_k]
    scored = []
    for p in papers:
        hits = sum(1 for w in words if w in p["content"].lower())
        subj_hits = sum(1 for w in words if w in p["subject"].lower())
        score = hits + subj_hits * 5
        if score > 0:
            scored.append((score, p))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored[:top_k]]


def generate_answer(client, question, papers):
    if not client:
        return "API key not set. Add your Gemini key in the sidebar.", []

    context_parts = []
    for p in papers:
        header = "[{} | {} | {} | {}]".format(p["paper_code"], p["subject"], p["semester"], p["year"])
        content = p["content"]
        first_word = re.sub(r"\W+", "", question.split()[0]).lower() if question.split() else ""
        idx = content.lower().find(first_word) if len(first_word) >= 4 else -1
        snippet = content[max(0, idx - 150): idx + 650].strip() if idx > -1 else content[:800].strip()
        context_parts.append("{}\n{}".format(header, snippet))

    context = ("\n\n" + "=" * 50 + "\n\n").join(context_parts)
    sources = ["{} - {} ({}, {})".format(p["paper_code"], p["subject"], p["semester"], p["year"]) for p in papers]

    prompt = (
        "You are an expert engineering professor helping B.Tech students prepare for exams.\n\n"
        "Content from previous year question papers:\n\n{}\n\n"
        "QUESTION: {}\n\n"
        "Give a clear, structured answer at B.Tech level. "
        "If this question appears in the papers above, use that context. "
        "If not found, say so briefly then answer from general knowledge.\n\nAnswer:"
    ).format(context, question)

    models_to_try = ["gemini-2.0-flash", "gemini-2.5-flash"]

    for model_name in models_to_try:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.3, max_output_tokens=1200),
                )
                return response.text, sources
            except Exception as e:
                err = str(e)
                if "503" in err or "UNAVAILABLE" in err:
                    if attempt == 0:
                        time.sleep(4)
                        continue
                    break
                if "429" in err or "RESOURCE_EXHAUSTED" in err:
                    if attempt == 0:
                        time.sleep(12)
                        continue
                    break
                return "API error ({}): {}".format(model_name, err[:300]), []

    return ("All models busy or quota exhausted. Wait 1 minute and try again. "
            "Free tier: 15 req/min, 1500 req/day."), []


def render_sidebar(papers):
    with st.sidebar:
        st.markdown(
            '<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.85rem;font-weight:500;'
            'color:#f9fafb;padding:0.25rem 0 0.75rem;">PYQ Assistant</div>',
            unsafe_allow_html=True,
        )
        api_key = st.text_input("API Key", label_visibility="collapsed", type="password",
                                value=os.getenv("GEMINI_API_KEY", ""),
                                placeholder="Gemini API key...", key="api_key_field")
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key

        if not papers:
            return api_key

        st.divider()
        by_sem = {}
        for p in papers:
            by_sem.setdefault(p["semester_num"], []).append(p)

        st.markdown(
            '<div style="font-size:0.7rem;color:#4b5563;font-family:\'JetBrains Mono\',monospace;'
            'margin-bottom:0.75rem;">{} subjects across {} semesters</div>'.format(len(papers), len(by_sem)),
            unsafe_allow_html=True,
        )
        for sem_num in sorted(by_sem.keys()):
            sem_papers = sorted(by_sem[sem_num], key=lambda x: x["paper_code"])
            with st.expander("Semester {}  ({} papers)".format(sem_num, len(sem_papers)), expanded=False):
                for p in sem_papers:
                    subj = p["subject"][:40] + ("..." if len(p["subject"]) > 40 else "")
                    st.markdown(
                        '<div class="paper-item"><span class="paper-code">{}</span><br>{}</div>'.format(
                            p["paper_code"], subj),
                        unsafe_allow_html=True,
                    )
    return api_key


def main():
    if not os.path.exists(PAPERS_DIR):
        os.makedirs(PAPERS_DIR, exist_ok=True)

    pdfs = [f for f in os.listdir(PAPERS_DIR) if f.lower().endswith(".pdf")]
    if not pdfs:
        st.error("No PDF files in `papers/` folder.")
        st.stop()

    if "papers" not in st.session_state:
        with st.spinner("Processing PDFs... (cached after first run)"):
            st.session_state["papers"] = load_all_papers(PAPERS_DIR)

    papers = st.session_state["papers"]
    if not papers:
        st.error("Could not extract content from PDFs.")
        st.stop()

    api_key = render_sidebar(papers)
    client = get_gemini_client(api_key)

    sems = sorted(set(p["semester_num"] for p in papers if p["semester_num"] > 0))
    years = sorted(set(p["year"] for p in papers))
    year_str = years[0] if len(years) == 1 else "{}-{}".format(years[0], years[-1])

    st.markdown(
        '<div class="app-header"><div class="app-title">PYQ Smart Assistant</div>'
        '<div class="app-meta">{} subjects &nbsp;·&nbsp; Sem {} &nbsp;·&nbsp; {} &nbsp;·&nbsp; {} PDFs</div></div>'.format(
            len(papers), ", ".join(str(s) for s in sems), year_str, len(pdfs)),
        unsafe_allow_html=True,
    )

    tab_ask, tab_browse, tab_search = st.tabs(["Ask", "Browse", "Search"])

    with tab_ask:
        st.markdown('<div class="section-label">Ask any question from your syllabus</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.8rem;color:#6b7280;margin-bottom:0.75rem;">Searches across all papers and generates a structured answer via Gemini.</div>', unsafe_allow_html=True)

        col_q, col_hint = st.columns([3, 1])
        with col_q:
            subject_opts = ["All subjects"] + sorted(set("{}  -  {}".format(p["paper_code"], p["subject"]) for p in papers))
            sel_sub = st.selectbox("Filter by subject", subject_opts, label_visibility="visible")
            question = st.text_area("Question", label_visibility="collapsed", placeholder="Type your question here...", height=100)
            ask_btn = st.button("Get Answer", type="primary")
        with col_hint:
            st.markdown('<div style="font-size:0.72rem;color:#9ca3af;line-height:2;margin-top:2rem;"><b style="color:#6b7280;display:block;margin-bottom:0.3rem;">Examples</b>Explain DES algorithm<br>Explain banker\'s algorithm<br>What is OSI model?<br>TCP three-way handshake<br>Deadlock avoidance<br>Bluetooth protocol stack<br>What is fuzzy logic?<br>Explain A* algorithm</div>', unsafe_allow_html=True)

        if ask_btn:
            if not question.strip():
                st.warning("Enter a question.")
            elif not api_key:
                st.warning("Add your Gemini API key in the sidebar.")
            else:
                pool = papers
                if sel_sub != "All subjects":
                    code = sel_sub.split("  -  ")[0].strip()
                    filtered = [p for p in papers if p["paper_code"] == code]
                    if filtered:
                        pool = filtered
                with st.spinner("Generating answer..."):
                    relevant = find_relevant(question, pool, top_k=3) or papers[:2]
                    answer, sources = generate_answer(client, question, relevant)
                st.markdown('<div class="answer-card">{}</div>'.format(answer.replace("\n", "<br>")), unsafe_allow_html=True)
                if sources:
                    st.markdown('<div class="source-row">{}</div>'.format("".join('<span class="source-chip">{}</span>'.format(s) for s in sources)), unsafe_allow_html=True)

    with tab_browse:
        st.markdown('<div class="section-label">Browse questions by paper</div>', unsafe_allow_html=True)
        col_s, col_p = st.columns(2)
        sem_opts = sorted(set(p["semester"] for p in papers), key=lambda s: next((p["semester_num"] for p in papers if p["semester"] == s), 0))
        sel_sem = col_s.selectbox("Semester", sem_opts)
        sem_papers = [p for p in papers if p["semester"] == sel_sem]
        paper_opts = ["{}  -  {}".format(p["paper_code"], p["subject"]) for p in sem_papers]
        sel_label = col_p.selectbox("Subject", paper_opts)
        sel_paper = next((p for p in sem_papers if "{}  -  {}".format(p["paper_code"], p["subject"]) == sel_label), None)

        if sel_paper:
            st.markdown('<div class="info-row">{} &nbsp;·&nbsp; {} &nbsp;·&nbsp; {} &nbsp;·&nbsp; {}</div>'.format(sel_paper["paper_code"], sel_paper["subject"], sel_paper["semester"], sel_paper["year"]), unsafe_allow_html=True)
            questions = extract_questions(sel_paper["content"])
            if questions:
                st.markdown('<div style="font-size:0.72rem;color:#6b7280;margin-bottom:0.5rem;">{} questions detected</div>'.format(len(questions)), unsafe_allow_html=True)
                for i, q in enumerate(questions):
                    label = q["number"] or "Q{}".format(i + 1)
                    marks_str = " [{} marks]".format(q["marks"]) if q["marks"] else ""
                    unit_str = " Unit {}".format(q["unit"]) if q["unit"] else ""
                    tag = " [Compulsory]" if q["is_compulsory"] else ""
                    preview = q["text"][:75] + ("..." if len(q["text"]) > 75 else "")
                    with st.expander("{}{}{}{}  --  {}".format(label, unit_str, marks_str, tag, preview)):
                        st.markdown('<div class="q-text">{}</div>'.format(q["text"]), unsafe_allow_html=True)
                        if st.button("Generate Answer", key="b_{}_{}".format(sel_paper["paper_code"], i)):
                            if not api_key:
                                st.warning("Add Gemini API key in sidebar.")
                            else:
                                with st.spinner("Generating..."):
                                    ans, _ = generate_answer(client, q["text"], [sel_paper])
                                st.markdown('<div class="answer-card">{}</div>'.format(ans.replace("\n", "<br>")), unsafe_allow_html=True)
            else:
                st.info("Could not parse individual questions. Showing raw text:")
                st.code(sel_paper["content"][:3000], language=None)

    with tab_search:
        st.markdown('<div class="section-label">Search across all papers</div>', unsafe_allow_html=True)
        query = st.text_input("Search", label_visibility="collapsed", placeholder="Enter keyword (e.g. deadlock, TCP, DES)...")
        if query:
            results = find_relevant(query, papers, top_k=10)
            if results:
                st.markdown('<div style="font-size:0.72rem;color:#6b7280;margin-bottom:0.75rem;">Found in {} papers</div>'.format(len(results)), unsafe_allow_html=True)
                for p in results:
                    with st.expander("{}  -  {}  ({}, {})".format(p["paper_code"], p["subject"], p["semester"], p["year"])):
                        content = p["content"]
                        idx = content.lower().find(query.lower())
                        snippet = ("..." + content[max(0, idx - 200): idx + 600] + "...") if idx > -1 else content[:700] + "..."
                        st.code(snippet, language=None)
                        if st.button("Answer from this paper", key="s_{}".format(p["paper_code"])):
                            if not api_key:
                                st.warning("Add Gemini API key in sidebar.")
                            else:
                                with st.spinner("Generating..."):
                                    ans, srcs = generate_answer(client, query, [p])
                                st.markdown('<div class="answer-card">{}</div>'.format(ans.replace("\n", "<br>")), unsafe_allow_html=True)
            else:
                st.info('No papers matched "{}". Try different keywords.'.format(query))


if __name__ == "__main__":
    main()

import json
import traceback
import PyPDF2

def _clean_text(s: str) -> str:
    if not s:
        return ""
    # Remove invalid surrogate code points by re-encoding
    return s.encode("utf-8", "ignore").decode("utf-8", "ignore")

def read_file(file):
    """Read and extract text from PDF or TXT file, with Unicode cleanup."""
    text = ""
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                raw = page.extract_text() or ""
                text += raw
        except Exception as e:
            raise Exception("Error reading the PDF file") from e
    elif file.name.endswith(".txt"):
        text = file.read().decode("utf-8", "ignore")
    else:
        raise Exception("Unsupported file format; only PDF and TXT are supported.")
    return _clean_text(text)

def get_table_data(quiz_obj):
    """Accepts a dict or JSON string and returns rows suitable for a DataFrame."""
    try:
        if isinstance(quiz_obj, dict):
            quiz_dict = quiz_obj
        else:
            cleaned = str(quiz_obj).strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.strip("`")
                if cleaned.lower().startswith("json"):
                    cleaned = cleaned[4:].strip()
            quiz_dict = json.loads(cleaned)
        quiz_table_data = []
        # Normalize keys to strings "1","2"...
        items = quiz_dict.items()
        for _, value in items:
            mcq = value.get("mcq", "")
            options_map = value.get("options", {}) or {}
            options = " || ".join([f"{k} -> {v}" for k, v in options_map.items()])
            correct = value.get("correct", "")
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        return quiz_table_data if quiz_table_data else None
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return None

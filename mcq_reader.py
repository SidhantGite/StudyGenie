# mcq_generator.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import json
import os

# ---------------------------------------------------------
# ✅ Gemini init (FLASH model) — uses your direct key first;
#    if env var GOOGLE_API_KEY/GENAI_API_KEY is set, it overrides.
# ---------------------------------------------------------
_HARDCODED_KEY = "AIzaSyDatfjdPnshQp7erzGchPYzV5fsxajH4aY"  # your key
_GOOGLE_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GENAI_API_KEY") or _HARDCODED_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,
    api_key=_GOOGLE_KEY  # keep param name "api_key" to match your installed lib
)

# ---------------------------------------------------------
# Templates for quiz generation and expert review
# ---------------------------------------------------------
with open(os.path.join(os.path.dirname(__file__), "response.json"), "r", encoding="utf-8") as f:
    RESPONSE_JSON = json.load(f)

TEMPLATE = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
- No repeated questions.
- Every question must strictly follow the provided text.
- Return ONLY a valid JSON object exactly like this template:
{RESPONSE_JSON}
"""

TEMPLATE2 = """
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students:
- Give a complexity evaluation in ≤50 words.
- Provide a brief expert review and improve any weak questions (if needed) while preserving the JSON format and count.

Quiz_MCQs:
{quiz}
Return a short paragraph review (not JSON).
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "RESPONSE_JSON"],
    template=TEMPLATE
)

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=TEMPLATE2
)

quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)
review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "subject", "tone", "RESPONSE_JSON"],
    output_variables=["quiz", "review"],
    verbose=True
)

# ---------------------------------------------------------
# Flashcards (JSON list of {"question","answer"})
# ---------------------------------------------------------
_flash_prompt = PromptTemplate(
    input_variables=["text", "count"],
    template=(
        "Create {count} concise flashcards in JSON LIST format only. "
        "Each item must be an object with 'question' and 'answer' fields. "
        "Use only facts from this content:\n{text}\n"
        "Return ONLY JSON like: "
        "[{{\"question\":\"...\",\"answer\":\"...\"}}, {{\"question\":\"...\",\"answer\":\"...\"}}]"
    )
)

def generate_flashcards(text: str, count: int = 10):
    """Generate flashcards as a Python list of dicts with 'question' and 'answer'."""
    prompt = _flash_prompt.format(text=text, count=count)
    resp = llm.invoke(prompt)
    raw = getattr(resp, "content", None) or str(resp)

    # Strip potential code fences
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    try:
        data = json.loads(cleaned)
        if isinstance(data, list):
            out = []
            for item in data:
                if isinstance(item, dict) and "question" in item and "answer" in item:
                    out.append({"question": item["question"], "answer": item["answer"]})
            return out[:count] if out else None
    except Exception:
        return None

import os
import json
import re
import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY") or "AIzaSyCBwv0mmP3dkN7mNUdqbJL8pg96BYgtB0o"

if not google_api_key:
    st.error("❌ Google Gemini API key not found! Please set it in .env")
    st.stop()

# Configure Gemini
genai.configure(api_key=google_api_key)

# Streamlit UI
st.set_page_config(page_title="📘 PDF Quiz Generator", layout="wide")
st.title("📘 PDF Quiz Generator with Gemini")

# Upload PDF
uploaded_file = st.file_uploader("📂 Upload your PDF", type="pdf")

if uploaded_file:
    pdf_reader = PdfReader(uploaded_file)
    pdf_text = ""
    for page in pdf_reader.pages:
        pdf_text += page.extract_text() + "\n"

    # ✅ Clean invalid surrogate characters
    pdf_text = re.sub(r'[\ud800-\udfff]', '', pdf_text)

    st.success("✅ PDF uploaded and text extracted!")
    st.write(pdf_text[:1500] + "..." if len(pdf_text) > 1500 else pdf_text)

    # User input: number of MCQs
    num_mcq = st.number_input("Enter number of MCQs you want", min_value=1, max_value=50, value=5)

    # Subject input
    subject = st.text_input("Enter subject (e.g., Biology, History, etc.)", value="General Knowledge")

    # Tone input
    tone = st.selectbox("Choose tone", ["simple", "moderate", "challenging"], index=0)

    if st.button("Generate Quiz"):
        with st.spinner("🔎 Generating quiz..."):
            prompt = f"""
            Text: {pdf_text}
            You are an expert MCQ maker. Based on the above text, create {num_mcq} multiple-choice questions 
            for {subject} students in a {tone} tone.
            Each question must have 4 options (A, B, C, D) and provide the correct answer.
            Return the output in JSON format like this:
            {{
              "quiz": [
                {{
                  "question": "....",
                  "options": ["A", "B", "C", "D"],
                  "answer": "A"
                }}
              ]
            }}
            """

            response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
            quiz_text = response.text

            try:
                quiz_data = json.loads(quiz_text)
                quiz = quiz_data.get("quiz", [])
            except Exception:
                st.error("⚠️ Failed to parse quiz. Here’s the raw output:")
                st.code(quiz_text)
                quiz = []

            if quiz:
                st.subheader("📝 Take the Quiz")
                score = 0

                for i, q in enumerate(quiz, 1):
                    st.markdown(f"**Q{i}. {q['question']}**")
                    user_ans = st.radio(
                        f"Choose answer for Q{i}",
                        q["options"],
                        key=f"q{i}"
                    )
                    if user_ans == q["answer"]:
                        st.success("✅ Correct!")
                        score += 1
                    else:
                        st.error(f"❌ Wrong! Correct Answer: {q['answer']}")
                    st.markdown("---")

                st.subheader(f"🎯 Your Score: {score}/{len(quiz)}")

import os
import uuid
import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load API key
google_api_key = "AIzaSyCBwv0mmP3dkN7mNUdqbJL8pg96BYgtB0o"
if not google_api_key:
    st.error("❌ Gemini API Key not found! Please set it in .env or environment variables.")
    st.stop()

# Initialize Gemini client
genai.configure(api_key=google_api_key)

# ✅ Unicode cleaning function
def clean_text(text):
    return text.encode("utf-8", "ignore").decode("utf-8")

# Page config
st.set_page_config(page_title="📘 AI Tutor + PDF Analyzer", layout="wide")
st.title("🎓 AI-Powered Tutor, Quiz & PDF Analyzer")

# Sidebar
with st.sidebar:
    st.header("Learning Preferences")
    subject = st.selectbox("📖 Select Subject",
                        ["Mathematics", "Physics", "Computer Science",
                         "History", "Biology", "Programming"])
    
    level = st.selectbox("📚 Select Learning Level",
                      ["Beginner", "Intermediate", "Advanced"])
    
    learning_style = st.selectbox("🧠 Learning Style",
                               ["Visual", "Text-based", "Hands-on"])
    
    language = st.selectbox("🌍 Preferred Language",
                         ["English", "Hindi", "Spanish", "French"])
    
    background = st.selectbox("📊 Background Knowledge",
                           ["Beginner", "Some Knowledge", "Experienced"])

# Tabs
tab1, tab2 = st.tabs(["📝 Ask a Question", "📘 PDF Analyzer"])

# -------- Tab 1: Tutor --------
with tab1:
    st.header("Ask Your Question")
    question = st.text_area("❓ What would you like to learn today?",
                         "Explain Newton's Second Law of Motion.")
    
    if st.button("Get Explanation 🧠"):
        with st.spinner("Generating personalized explanation..."):
            try:
                # Build prompt
                prompt = f"""
                Subject: {subject}
                Level: {level}
                Style: {learning_style}
                Language: {language}
                Background: {background}

                Question: {question}

                Provide a clear, structured explanation suitable for this learner.
                """
                prompt = clean_text(prompt)

                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)

                st.success("Here's your personalized explanation:")
                st.markdown(response.text, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")

# -------- Tab 2: PDF Analyzer --------
with tab2:
    st.header("Upload and Analyze PDF")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file:
        pdf_reader = PdfReader(uploaded_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                pdf_text += text + "\n"

        pdf_text = clean_text(pdf_text)

        st.subheader("📄 Extracted Content")
        st.write(pdf_text[:1500] + "..." if len(pdf_text) > 1500 else pdf_text)

        if st.button("✨ Generate Quiz & Flashcards"):
            with st.spinner("Analyzing PDF and generating content..."):
                prompt = f"""
Analyze the following PDF content and do the following:
1. Create a 10-question multiple choice quiz with 4 options each and the correct answer marked.
2. Create 10 flashcards with Question-Answer format for quick revision.

PDF Content:
{pdf_text}
                """
                prompt = clean_text(prompt)

                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                result = response.text

            st.success("✅ Quiz & Flashcards Generated!")

            # Display results
            st.subheader("📝 Quiz")
            st.write(result.split("2. Create 10 flashcards")[0])

            st.subheader("📌 Flashcards")
            st.write(result.split("2. Create 10 flashcards")[-1])

# Footer
st.markdown("---")
st.markdown("Powered by AI - Your Personal Learning Assistant")

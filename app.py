import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
from pypdf import PdfReader

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Page config
st.set_page_config(
    page_title="AI Onboarding Assistant",
    page_icon="🤖",
    layout="wide"
)

# ================= HR SIDEBAR =================
st.sidebar.title("🧑‍💼 HR Panel")

hr_text = st.sidebar.text_area(
    "Paste onboarding content here",
    height=220,
    placeholder="Paste company policies, tools, timings, etc..."
)

uploaded_pdf = st.sidebar.file_uploader(
    "Or upload onboarding PDF",
    type=["pdf"]
)

def extract_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

onboarding_context = ""

if uploaded_pdf:
    onboarding_context = extract_pdf_text(uploaded_pdf)
    st.sidebar.success("PDF uploaded successfully")

elif hr_text.strip():
    onboarding_context = hr_text
    st.sidebar.success("Text added successfully")

else:
    st.sidebar.info("Waiting for HR content")

# ================= MAIN UI =================
st.title("🤖 AI Onboarding Assistant")
st.write("Ask any onboarding-related question")

user_question = st.text_input("Your question")

if st.button("Ask AI"):
    if not onboarding_context:
        st.warning("HR has not provided onboarding content yet.")
    elif not user_question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an AI onboarding assistant. "
                            "Answer ONLY using the onboarding content provided below. "
                            "If the answer is not present, reply exactly with: "
                            "'Please contact HR.'\n\n"
                            f"{onboarding_context}"
                        )
                    },
                    {
                        "role": "user",
                        "content": user_question
                    }
                ],
                temperature=0.2
            )

            answer = response.choices[0].message.content
            st.success(answer)
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
import streamlit as st

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Movie Information Extractor",
    page_icon="🎬",
    layout="centered"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.stApp{
    background-color:#0E1117;
}

.main-title{
    text-align:center;
    font-size:52px;
    font-weight:800;
    color:white;
    margin-bottom:20px;
}

.stTextArea textarea{
    background:#262730;
    color:white;
    border:2px solid #C63C46;
    border-radius:15px;
    font-size:17px;
}

.stButton>button{
    width:100%;
    background:#C63C46;
    color:white;
    border:none;
    border-radius:10px;
    height:50px;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#E14C56;
}

.result-box{
    background:#1A1D24;
    padding:20px;
    border-radius:12px;
    border:1px solid #444;
    color:white;
    white-space:pre-wrap;
    font-size:16px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Model
# -----------------------------
model = ChatMistralAI(
    model="mistral-small-2506"
)

# -----------------------------
# Prompt Template
# -----------------------------
prompt = ChatPromptTemplate.from_messages(
[
(
"system",
"""
You are a professional Movie Information Extraction Assistant.

Your task:
Extract useful structured information from a movie paragraph and present it in the format below.

Rules:
- Do NOT add explanations
- Do NOT add extra commentary
- Follow the exact format
- If information is missing → write NULL
- Keep summary short (2–3 lines max)
- Do NOT guess unknown facts

Output Format:

Title:
Genre:
Director:
Main Cast:
Setting/Location:
Plot:
Themes:
Ratings:
Notable Features:

Short Summary:
"""
),

(
"human",
"""
Extract information from this paragraph:

{paragraph}
"""
)
]
)

# -----------------------------
# UI
# -----------------------------

st.markdown(
'<div class="main-title">🎬 Movie Information Extractor</div>',
unsafe_allow_html=True
)

paragraph = st.text_area(
"Enter movie paragraph:",
height=280,
placeholder="Paste any movie description here..."
)

if st.button("🎯 Extract Information"):

    if paragraph.strip() == "":
        st.warning("Please enter a movie paragraph.")
    else:

        with st.spinner("Extracting information..."):

            final_prompt = prompt.invoke(
                {
                    "paragraph": paragraph
                }
            )

            response = model.invoke(final_prompt)

        st.markdown("## 📄 Extracted Information")

        st.markdown(
            f"""
<div class="result-box">

{response.content}

</div>
""",
unsafe_allow_html=True
)
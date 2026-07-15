import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>

.stApp{
    background:#0f172a;
}

/* Main content */
.block-container{
    max-width:900px;
    padding-top:1.5rem;
    padding-bottom:2rem;
}

/* Header */
.title{
    font-size:42px;
    font-weight:700;
    text-align:center;
    color:white;
    margin-bottom:0;
}

.subtitle{
    text-align:center;
    color:#94a3b8;
    margin-bottom:30px;
}

/* Chat messages */
[data-testid="stChatMessage"]{
    padding:15px;
    border-radius:18px;
    margin-bottom:15px;
    border:1px solid #263247;
    background:#1e293b;
}

/* Chat input */
[data-testid="stChatInput"]{
    margin-top:20px;
}

/* Button */
.stButton>button{
    width:100%;
    border-radius:10px;
    height:42px;
    background:#2563eb;
    color:white;
    border:none;
    font-weight:600;
}

.stButton>button:hover{
    background:#1d4ed8;
}

hr{
    border:none;
    height:1px;
    background:#263247;
    margin-top:10px;
    margin-bottom:25px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- MODEL ---------------- #
model = init_chat_model(
    "groq:llama-3.3-70b-versatile",
    temperature=0.9,
    max_tokens=50
)

# ---------------- SESSION ---------------- #
if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- HEADER ---------------- #
left, right = st.columns([6,1])

with left:
    st.markdown(
        "<div class='title'>🤖 AI Chatbot</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='subtitle'>Powered by LangChain + Groq</div>",
        unsafe_allow_html=True
    )

with right:
    st.write("")
    if st.button("🗑 Clear"):
        st.session_state.messages.clear()
        st.session_state.history.clear()
        st.rerun()

st.divider()

# ---------------- CHAT HISTORY ---------------- #
chat_box = st.container()

with chat_box:

    if len(st.session_state.history) == 0:
        st.info("👋 Welcome! Ask me anything.")

    for role, message in st.session_state.history:

        if role == "user":
            avatar = "👤"
        else:
            avatar = "🤖"

        with st.chat_message(role, avatar=avatar):
            st.markdown(message)

# ---------------- INPUT ---------------- #
prompt = st.chat_input("Type your message...")

if prompt:

    st.session_state.messages.append(prompt)
    st.session_state.history.append(("user", prompt))

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    response = model.invoke(st.session_state.messages)

    st.session_state.messages.append(response.content)
    st.session_state.history.append(("assistant", response.content))

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response.content)
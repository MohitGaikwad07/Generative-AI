import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

load_dotenv()

st.set_page_config(
    page_title="AI Mood Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ---------------- CSS ---------------

st.markdown("""
<style>

.stApp{
    background:#0F172A;
}

.block-container{
    max-width:850px;
    padding-top:4rem !important;
}

.title{
    text-align:center;
    color:white;
    font-size:42px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:#94A3B8;
    margin-bottom:25px;
}

[data-testid="stChatMessage"]{
    background:#1E293B;
    border-radius:15px;
    padding:15px;
    margin-bottom:12px;
    border:1px solid #334155;
}

.stButton>button{
    width:100%;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Model ---------------- #

model = init_chat_model(
    "groq:llama-3.3-70b-versatile",
    temperature=0.9,
    max_tokens=50
)

# ---------------- Header ---------------- #

st.markdown("<div class='title'>🤖 AI Mood Chatbot</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Powered by LangChain + Groq</div>", unsafe_allow_html=True)

# ---------------- Session ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- Top Bar ---------------- #

col1, col2 = st.columns([5,1])

with col1:
    st.markdown("### 🎭 Choose Chatbot Personality")

    mood = st.radio(
        label="",
        options=["😊 Happy", "😢 Sad", "😡 Angry"],
        horizontal=True,
        label_visibility="collapsed"
    )

with col2:
    st.write("")
    st.write("")

    if st.button("🗑 Clear"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

# ---------------- System Prompt ---------------- #

if mood=="😊 Happy":
    system_prompt = "You are a happy chatbot. Respond cheerfully, positively and energetically."

elif mood=="😢 Sad":
    system_prompt = "You are a sad chatbot. Respond emotionally and sadly."

else:
    system_prompt = "You are an angry chatbot. Respond in an angry tone without using abusive language."

# Always keep system prompt first
messages = [SystemMessage(content=system_prompt)]

for msg in st.session_state.messages:
    messages.append(msg)

# ---------------- History ---------------- #

for role, text in st.session_state.chat_history:

    avatar="👤"

    if role=="assistant":
        avatar="🤖"

    with st.chat_message(role, avatar=avatar):
        st.markdown(text)

# ---------------- Input ---------------- #

prompt = st.chat_input("Type your message...")

if prompt:

    human = HumanMessage(content=prompt)

    messages.append(human)

    st.session_state.messages.append(human)

    st.session_state.chat_history.append(
        ("user",prompt)
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    response = model.invoke(messages)

    ai = AIMessage(content=response.content)

    st.session_state.messages.append(ai)

    st.session_state.chat_history.append(
        ("assistant",response.content)
    )

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response.content)
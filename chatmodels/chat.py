from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model("groq:llama-3.3-70b-versatile",temperature=0.9,max_tokens=50)


print("-------Welcome to the Chatbot Enter 0 t exit chat-------")

while True:
    prompt = input("You: ") 
    if prompt=="0":
        break
    response = model.invoke(prompt)
    print("Bot: ", response.content)
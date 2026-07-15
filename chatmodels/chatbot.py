from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model("groq:llama-3.3-70b-versatile",temperature=0.9,max_tokens=50)

messages=[

]

print("-------Welcome to the Chatbot Enter 0 to exit chat-------")

while True:
    prompt = input("You: ") 
    messages.append(prompt)
    if prompt=="0":
        break
    response = model.invoke(messages)
    messages.append(response.content)
    print("Bot: ", response.content)
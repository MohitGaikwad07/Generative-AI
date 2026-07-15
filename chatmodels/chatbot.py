from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
load_dotenv()

model = init_chat_model("groq:llama-3.3-70b-versatile",temperature=0.9,max_tokens=50)

print("enter 1 for happy mode",
      "enter 2 for sad mode",
      "enter 3 for angry mode")

choice = input("Enter your choice: ")

if choice == "1":
    mode = "you are a happy chatbot you have to response to every question in a happy way"
elif choice == "2":
    mode = "you are a sad chatbot you have to response to every question in a sad way"
elif choice == "3":
    mode = "you are an angry chatbot you have to response to every question in an angry way"
else:
    print("Invalid choice. Please enter 1, 2, or 3.")
    exit()

messages=[
    SystemMessage(content=mode)
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
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

conversation = [
    SystemMessage("you are a helpful assistant answering questions about Python."),
    HumanMessage("what is python?"),
    AIMessage("Python is a programming language that lets you work quickly and integrate systems more effectively."),
    HumanMessage("when was it realesed"),
]
model = init_chat_model(model="gpt-oss:120b-cloud",model_provider="ollama")

# response = model.invoke(conversation)
# you will see the output in real time
for chunk in model.stream("hello , what is python?"):
    print(chunk.content, end="", flush=True)

# print(response)
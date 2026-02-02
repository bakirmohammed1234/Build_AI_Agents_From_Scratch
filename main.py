import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
# from langchain.tools  import ToolRuntime
# from langchain_ollama import OllamaLLM
# from langchain_ollama import ChatOllama
from tools import get_weather, locate_user
from langchain_groq import ChatGroq
from langchain.chat_models import init_chat_model
from dataClassFormat import Context, ResponseFormat
from langgraph.checkpoint.memory import InMemorySaver
load_dotenv()






# print(get_weather.invoke("Paris"))
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)
checkpointer = InMemorySaver()
agent = create_agent(
    model= llm ,
    tools=[get_weather, locate_user],
    system_prompt= "You are a helpful weather assistant, who always cracks jokes and is humorous while remaining helpful.",
    context_schema= Context,
    response_format= ResponseFormat,
    checkpointer= checkpointer
    )

config = {'configurable': {'thread_id': 1}}

# Remplacez votre bloc de fin par celui-ci :
# response = agent.invoke({
#     'messages': [('user', 'What is the weather like in Paris today?')]
# })

response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "What is the weather like?"}
        ]
    },
    config=config,
    context=Context(user_id="ABC123")
)


# Print (response)
# print("---------------------------------------------------------------------")
# print(response['messages'][-1].content)
print(response['structured_response'])
print("---------------------------------------------------------------------")
print(response['structured_response'].summary)
print(f"Temperature in Celsius: {response['structured_response'].temperature_celsius}°C")
print(f"Temperature in Fahrenheit: {response['structured_response'].temperature_fahrenheit}°F")
print(f"Humidity: {response['structured_response'].humidity}%")
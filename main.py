import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools  import tool, ToolRuntime
# from langchain_ollama import OllamaLLM
# from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain.chat_models import init_chat_model
from dataclasses import dataclass
from langgraph.checkpoint.memory import InMemorySaver
load_dotenv()

@dataclass
class Context:
    user_id: str

@dataclass
class ResponseFormat:
    summary: str
    temperature_celsius: float
    temperature_fahrenheit: float
    humidity : float


@tool('get_weather', description="Return weather information for a given city.", return_direct=False)
def get_weather(city: str) -> str:
    try:
        # On demande le format 2 qui est plus "verbeux" et sans emojis bizarres
        response = requests.get(f"https://wttr.in/{city}?format=%l:+%C+%t", timeout=10)
        
        if response.status_code == 200:
            # Exemple de retour : "Paris: Partly cloudy +8°C"
            return response.text.strip()
        return "Error: Weather service unavailable."
    except Exception as e:
        return f"Error: {str(e)}"

@tool('locate_user', description="Look Up a user's city based  on context.")    
def locate_user(runtime: ToolRuntime[Context]):
    match runtime.context.user_id:
        case "ABC123":
            return "Vienna"
        case "XYZ456":
            return "London"
        case "HJKL111":
            return "Paris"
        case _:
            return "Unknown"


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


# print (response)
# print("---------------------------------------------------------------------")
# print(response['messages'][-1].content)
print(response['structured_response'])
print("---------------------------------------------------------------------")
print(response['structured_response'].summary)
print(f"Temperature in Celsius: {response['structured_response'].temperature_celsius}°C")
print(f"Temperature in Fahrenheit: {response['structured_response'].temperature_fahrenheit}°F")
print(f"Humidity: {response['structured_response'].humidity}%")
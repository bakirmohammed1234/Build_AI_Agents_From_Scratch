import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools  import tool
from langchain_ollama import OllamaLLM
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq

load_dotenv()
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


# print(get_weather.invoke("Paris"))
llm = ChatGroq(model="llama-3.1-8b-instant")

agent = create_agent(
    model= llm ,
    tools=[get_weather],
    system_prompt= "You are a helpful assistant that provides weather information."
)

# Remplacez votre bloc de fin par celui-ci :
# response = agent.invoke({
#     'messages': [('user', 'What is the weather like in Paris today?')]
# })

response = agent.invoke({
'messages': [
{'role': 'user', 'content': 'What is the weather like in Paris?'}
]
})

print (response)
# print("---------------------------------------------------------------------")
print(response['messages'][-1].content)
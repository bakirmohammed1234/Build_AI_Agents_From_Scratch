from langchain.tools  import tool, ToolRuntime
import requests
from dataClassFormat import Context
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
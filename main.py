from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

from langchain_ollama import OllamaLLM
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
load_dotenv()

""" Example usage of Groq LLM with LangChain 
llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
  
)

ai_msg = llm.invoke("Explique la théorie de la relativité restreinte en termes simples.")
print(ai_msg.content)
"""
## local solutio with Ollama

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]
    

llm = OllamaLLM(
    model="gpt-oss:120b-cloud",
    temperature=0
)
#Response = llm.invoke("Quel est le sens de la vie ?")
# print(response)

parser = PydanticOutputParser(pydantic_object=ResearchResponse)




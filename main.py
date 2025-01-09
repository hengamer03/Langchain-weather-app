import json
import os
import requests

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def fetch_weather_data(location):
    try:
        api_key = os.getenv("API_KEY")
        url  = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        data = response.json()

    except Exception as e:
        print("An error occured: ", e)
        return None
    
    return data

prompt = PromptTemplate(
    input_variables=["location"],
    template="What is the weather in {location}?", 
)

# LLM setup
local_llm = "llama3.1"
llm = ChatOllama(model=local_llm, temperature=0)
llm_json_mode = ChatOllama(model=local_llm, temperature=0, format="json")

chain = prompt | llm | StrOutputParser()

user_input = input("ask for the weather in a norwegian city or location: ")

if user_input.strip():
    weather_data = fetch_weather_data(user_input)
    if weather_data: 
        weather_data_json = json.dumps(weather_data, indent=2)
        prompt = prompt.format(weather_data=weather_data_json, location=user_input)
        instruction = "convert from json to a more human readable format, make sure to include the temprature and forecast"
        question = f"this is your instructions:\n {instruction} \n\n this is the weather data:\n {weather_data_json} \n\n"
        response = llm.invoke(question)
        print(response.content)
else:
    print("Please provide a location in Norway")







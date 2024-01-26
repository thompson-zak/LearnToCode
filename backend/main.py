from typing import Annotated
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict
from openai import OpenAI
import time


class Settings(BaseSettings):
    openai_api_key: str
    frontend_api_auth: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=settings.openai_api_key
)

prompts = {
    "Variables": {
        1: {

        },
        2: {

        },
        3: {

        }
    },
    "Data": {},
    "Conditionals": {},
    "OOP": {}
}

# 
# API used from front-end to call for ChatGPT responses to fill the various exercises provided to students
#
# Section - this is the title of the section that the user is currently on
# Id - this is the specific exercise within the section that needs to be populated with data
# Auth_header - this will be used to identify requests and deny users
#
@app.get("/")
async def root(section: str, id: int, auth_header: Annotated[str | None, Header()] = None):

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a computer science professor, skilled in explaining complex programming concepts to beginners."},
            {"role": "user", "content": "Please provide a prompt and code outline to help a student who has never coded before learn python syntax and variables.."}
        ]
    )

    return {
        "completion": completion
    }


@app.get("/test")
async def test():
    time.sleep(5)
    return {
        "message": "Hello World!"
    }
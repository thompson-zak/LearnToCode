from typing import Annotated
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from openai import OpenAI
import time
import asyncio

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
        1: "Please provide a prompt and code outline for a very basic problem to help a student who has never coded before learn python syntax and variables.",
        2: "Please provide a prompt and code outline for a problem to help a student who has never coded before learn python syntax and variables.",
        3: "Please provide a prompt and code outline for a challenging problem to help a student who has never coded before learn python syntax and variables."
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
#   -- If a positive value is provided, only that particular exercise will be run through OpenAI
#   -- If no value or '-1' is provided, all exercises within the section will be run and returned together
# Auth_header - this will be used to identify requests and deny users

class CompletionsResponse(BaseModel):
    completions: dict = {}
    error: str = ""

@app.get("/")
async def root(section: str, id: int = -1, auth_header: Annotated[str | None, Header()] = None) -> CompletionsResponse:

    requestedPrompts = []

    section = prompts.get(section, None)
    if(section == None):
        return { "completions": {}, "error": "Invalid section provided."}
    
    if(id != -1):
        exercisePrompt = section.get(id, None)
        if(exercisePrompt == None):
            return { "completions": {}, "error": "Exercise ID provided is invalid for given section"}
        
        requestedPrompts.append((id, exercisePrompt))
    else:
        # Empty dictionaries evaluate to false
        if(not section):
            return { "completions": {}, "error": "Section provided is empty"}
        
        for key in section:
            requestedPrompts.append((key, section.get(key)))
    
    print(requestedPrompts)

    # Not sure this is guaranteed to load in order. Look to attach keys to prompts when gathering.
    completions = await asyncio.gather(*[getOpenaiCompletion(prompt[0], prompt[1]) for prompt in requestedPrompts])

    formattedCompletions = {}
    for completion in completions:
        formattedCompletions[completion["key"]] = completion["completion"]
    return { "completions": formattedCompletions, "error": "" }




async def getOpenaiCompletion(key: int, prompt: str):
    #completion = await client.chat.completions.create(
    #    model="gpt-3.5-turbo",
    #    messages=[
    #        {"role": "system", "content": "You are a computer science professor, skilled in explaining complex programming concepts to beginners."},
    #        {"role": "user", "content": prompt}
    #    ]
    #)

    completion = {}

    return { 
        "key": key,
        "completion": completion
     }


@app.get("/test")
async def test():
    time.sleep(5)
    return {
        "message": "Hello World!"
    }
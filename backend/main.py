from typing import Annotated
from fastapi import FastAPI, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from openai import AsyncOpenAI
import time
import asyncio
import json
from random import randint
from utils import *
from codeExecution import execute
from formatting import formatCompletions, formatValidityCompletion


class Settings(BaseSettings):
    openai_api_key: str
    frontend_api_pass: str
    api_auth_enabled: bool
    mongo_db_user: str
    mongo_db_pass: str

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
app.tokenCache = {}
client = AsyncOpenAI(
    api_key=settings.openai_api_key
)

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
    executionTime: float = -1.0

@app.get("/")
async def root(section: str, id: int = -1, track: str = "None", auth_header: Annotated[str | None, Header()] = None) -> CompletionsResponse:

    startTime = time.time()

    requestedPrompts = validateAndParsePrompts(section, id, track, auth_header, settings, app.tokenCache)

    print("------------Prompts------------")
    print(requestedPrompts)
    print("----------------------------------")

    completions = await asyncio.gather(*[getOpenaiCompletion(prompt[1]) for prompt in requestedPrompts])

    completionsWithKeys = [{"key": index+1, "completion": completions[index]} for index in range(0, len(completions))]

    formattedCompletions = formatCompletions(completionsWithKeys)
    
    return { 
        "completions": formattedCompletions, 
        "executionTime": round(time.time() - startTime, 2) 
    }


async def getOpenaiCompletion(prompt: str):
    return await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )


@app.post("/execute/code/validation")
async def validateUserSolution(request: Request, auth_header: Annotated[str | None, Header()] = None):
    validateAuthHeader(auth_header, settings, app.tokenCache)

    jsonRequest = await request.json()
    assistantMessage = jsonRequest["assistantMessage"]
    code = jsonRequest["code"]
    userMessage = "Is this code a correct solution to the above problem? Please provide a yes or no answer.\n{code}".format(code=code)

    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant", "content": assistantMessage},
            {"role": "user", "content": userMessage}
        ]
    )

    return formatValidityCompletion(completion)


@app.get("/login")
async def login(auth_header: Annotated[str | None, Header()] = None):
    if(auth_header == settings.frontend_api_pass):
        token = createAndStoreUserToken(settings, app.tokenCache)
        return { "token": token }
    else:
        raise HTTPException(status_code=400, detail="That password is not correct")


@app.get("/checkToken")
async def checkToken(auth_header: Annotated[str | None, Header()] = None):
    try:
        valid = validateAuthHeader(auth_header, settings, app.tokenCache)
    except Exception as e:
        valid = False

    return { "valid": valid }


@app.post("/execute/code")
async def executeCode(request: Request, auth_header: Annotated[str | None, Header()] = None):
    startTime = time.time()

    jsonRequest = await request.json()
    code = jsonRequest["code"]
    validateCode(code, auth_header, settings, app.tokenCache)

    output, error = execute(code) 

    return {
        "output": str(output),
        "error": error,
        "executionTime": round(time.time() - startTime)
    } 


# Endpoint used for development purposes to minimize actual calls to OpenAI services
@app.get("/test")
async def test(requestTriple: bool = True, auth_header: Annotated[str | None, Header()] = None):

    validateAuthHeader(auth_header, settings, app.tokenCache)

    # Simulates loading times for OpenAI requests
    startTime = time.time()
    time.sleep(2)

    if requestTriple:
        # Loads the pre-fetched and pre-formatted chat completion containing all 3 sample exercises
        filePath = "./test/variables/sample_multiple_formatted_completion.json"
    else:
        # Loads one of two pre-fetched and pre-formatted chat completion responses
        filePath = "./test/variables/sample_formatted_completion_" + str(randint(1,2)) + ".json"

    file = open(filePath)
    formattedResponse = json.load(file)
    return {
        "completions": formattedResponse,
        "exectionTime": round(time.time() - startTime, 2)
    }


@app.get("/ping")
async def ping():
    return { "detail": "pong" }
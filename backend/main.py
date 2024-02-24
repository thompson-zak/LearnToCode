from typing import Annotated
from fastapi import FastAPI, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from openai import AsyncOpenAI
import time
import asyncio
import json
import multiprocessing as mp
import sys
from random import randint
from utilities import *
from prompts import *
from io import StringIO
from contextlib import redirect_stdout
import traceback


class Settings(BaseSettings):
    openai_api_key: str
    frontend_api_pass: str
    api_auth_enabled: bool
    mongo_db_user: str
    mongo_db_pass: str

    model_config = SettingsConfigDict(env_file=".env")

class CaptureOutput:
    def __enter__(self):
        self._stdout_output = ''
        self._stderr_output = ''

        self._stdout = sys.stdout
        sys.stdout = StringIO()

        self._stderr = sys.stderr
        sys.stderr = StringIO()

        return self

    def __exit__(self, *args):
        self._stdout_output = sys.stdout.getvalue()
        sys.stdout = self._stdout

        self._stderr_output = sys.stderr.getvalue()
        sys.stderr = self._stderr

    def get_stdout(self):
        return self._stdout_output

    def get_stderr(self):
        return self._stderr_output


settings = Settings()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = AsyncOpenAI(
    api_key=settings.openai_api_key
)
prompts = getPrompts()

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
async def root(section: str, id: int = -1, auth_header: Annotated[str | None, Header()] = None) -> CompletionsResponse:

    startTime = time.time()

    requestedPrompts = validateAndParsePrompts(section, id, auth_header, prompts, settings)

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
            #{"role": "system", "content": "You are a computer science professor, skilled in explaining complex programming concepts to beginners."},
            {"role": "user", "content": prompt}
        ]
    )


@app.get("/login")
async def login(auth_header: Annotated[str | None, Header()] = None):
    if(auth_header == settings.frontend_api_pass):
        token = createAndStoreUserToken(settings)
        return { "token": token }
    else:
        raise HTTPException(status_code=400, detail="That password is not correct")


@app.get("/checkToken")
async def checkToken(auth_header: Annotated[str | None, Header()] = None):
    try:
        valid = validateAuthHeader(auth_header, settings)
    except Exception as e:
        valid = False

    return { "valid": valid }


@app.post("/execute/code")
async def executeCode(request: Request, auth_header: Annotated[str | None, Header()] = None):
    startTime = time.time()

    jsonRequest = await request.json()
    code = jsonRequest["code"]
    validateCode(code, auth_header, settings)

    queue = mp.Queue()
    p = mp.Process(target=worker, args=(code, queue))
    p.start()
    # Must do this call before call to join:

    timeout = False
    try:
        stdout_output, stderr_output = queue.get(True, 5.0)
    except Exception:
        stdout_output = ""
        stderr_output = ""
        print("There has been a timeout waiting for queue")
        timeout = True

    # Check to see if the process timed out and add error message for that
    p.join(1.0)
    if p.is_alive():
        print("There has been a timeout waiting for join")
        trimmedError = "[ERROR] Your code timed out after 5 seconds and did not complete."
        timeout = True

    # This will kill the process if it is still running past timeout
    p.terminate()
    p.join()
    
    # Check to see whether process has been ended
    if p.is_alive():
        print("Code execution process orphaned.")
    else:
        # This will release all resource associated with the process
        p.close()
        print("Code execution process successfully closed.")

    if not timeout:
        trimmedError = stderr_output
        strippedError = str(stderr_output).strip()
        if(len(strippedError) != 0):
            # We only want to grab the error type and string, not the stack trace from the execution engine
            firstNewline = strippedError.rindex('\n')
            trimmedError = strippedError[firstNewline + 1 : ]

    return {
        "output": str(stdout_output),
        "error": trimmedError,
        "executionTime": round(time.time() - startTime)
    } 


def worker(code, queue):
    with CaptureOutput() as capturer:
        try:
            runCode(code)
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
    queue.put((capturer.get_stdout(), capturer.get_stderr()))


def runCode(code : str):
    # set globals parameter to none
    globalsParameter = {'__builtins__' : None}
    # set locals parameter to take only print()
    localsParameter = {'print': print}
    # successful execution will result in None returned
    return exec(code, globalsParameter, localsParameter)
    

# Endpoint used for development purposes to minimize actual calls to OpenAI services
@app.get("/test")
async def test(requestTriple: bool = True, auth_header: Annotated[str | None, Header()] = None):

    validateAuthHeader(auth_header, settings)

    # Simulates loading times for OpenAI requests
    startTime = time.time()
    time.sleep(2)

    if requestTriple:
        # Loads the pre-fetched and pre-formatted chat completion containing all 3 sample exercises
        filePath = "./test_resources/variables/sample_multiple_formatted_completion.json"
    else:
        # Loads one of two pre-fetched and pre-formatted chat completion responses
        filePath = "./test_resources/variables/sample_formatted_completion_" + str(randint(1,2)) + ".json"

    file = open(filePath)
    formattedResponse = json.load(file)
    return {
        "completions": formattedResponse,
        "exectionTime": round(time.time() - startTime, 2)
    }


@app.get("/ping")
async def ping():
    return { "detail": "pong" }
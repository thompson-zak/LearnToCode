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

class Settings(BaseSettings):
    openai_api_key: str
    frontend_api_auth: str
    api_auth_enabled: bool

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


@app.post("/execute/code")
async def executeCode(request: Request, auth_header: Annotated[str | None, Header()] = None):
    jsonRequest = await request.json()
    code = jsonRequest["code"]
    validateCode(code, auth_header, settings)

    queue = mp.Queue()
    p = mp.Process(target=worker, args=(code, queue))
    p.start()
    # Must do this call before call to join:
    result, stdout_output, stderr_output = queue.get()
    
    # This will result in the join timing out, but it won't necessary kill the
    # thread which is actually running the code
    p.join(5.0)

    print("result: " + str(result))
    print("stdout: " + str(stdout_output))
    print("stderr: " + str(stderr_output))

    return {
        "output": str(stdout_output),
        "error": str(stderr_output)
    } 


def worker(code, queue):
    import traceback

    with CaptureOutput() as capturer:
        try:
            result = runCode(code)
        except Exception as e:
            result = e
            print(traceback.format_exc(), file=sys.stderr)
    queue.put((result, capturer.get_stdout(), capturer.get_stderr()))


def runCode(code : str):
    # set globals parameter to none
    globalsParameter = {'__builtins__' : None}
    # set locals parameter to take only print()
    localsParameter = {'print': print}
    # successful execution will result in None returned
    return exec(code, globalsParameter, localsParameter)
    

@app.post("/execute/code/test")
async def executeCodeTest():
    time.sleep(3)
    return { 
        "output": "Hello World!" 
    }

# Endpoint used for development purposes to minimize actual calls to OpenAI services
@app.get("/test")
async def test(requestTriple: bool = True):
    # Simulates loading times for OpenAI requests
    startTime = time.time()
    time.sleep(8)

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
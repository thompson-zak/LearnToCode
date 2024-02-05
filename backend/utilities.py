from pydantic_settings import BaseSettings
from fastapi import HTTPException
import json
import re
import traceback

def validateAuthHeader(auth_header: str, settings: BaseSettings):
    if(settings.api_auth_enabled and auth_header != settings.frontend_api_auth):
        raise HTTPException(status_code=400, detail="You are not authorized to call this endpoint.")


def validateCode(code: str, auth_header: str, settings: BaseSettings):
    validateAuthHeader(auth_header, settings)
    
    print("I am currently validating user provided code.")

    try:
        codeObject = compile(code, "User supplied code", "exec")
    except Exception as e:
        eType = type(e).__name__
        userErrorString = ""
        if eType == 'SyntaxError':
            traceStrList = traceback.format_exception(e)
            strLen = len(traceStrList)
            if strLen >= 3:
                userErrorString = traceStrList[strLen-3] + traceStrList[strLen-2] + traceStrList[strLen-1]

        errorObject = {
            "errorType": eType,
            "errorMessage": userErrorString
        }

        print("I have caught an error during compilation!")

        raise HTTPException(status_code=400, detail=errorObject)

    return None


def validateAndParsePrompts(requestedSection: str, id: int, auth_header: str,  prompts: any, settings: BaseSettings):
    validateAuthHeader(auth_header, settings)
            
    section = prompts.get(requestedSection, None)
    if(section == None): 
        raise HTTPException(status_code=400, detail="Invalid section provided.")
    
    requestedPrompts = []
    
    if(id != -1):
        exercisePrompt = section.get(id, None)
        if(exercisePrompt == None):
            raise HTTPException(status_code=400, detail="Exercise ID provided is invalid for given section")
        
        requestedPrompts.append((id, exercisePrompt))
    else:
        # Empty dictionaries evaluate to false
        if(not section):
            raise HTTPException(status_code=400, detail="Section provided is empty")
        
        for key in section:
            requestedPrompts.append((key, section.get(key)))
        
    return requestedPrompts


def formatCompletions(completionsWithKeys):
    formattedCompletions = {}
    for completionWithKey in completionsWithKeys:

        completion = completionWithKey["completion"]
        if not isinstance(completion, dict):
            completion = vars(completion)

        print("------------Completion------------")
        print(completion)
        print("----------------------------------")

        choices = completion.get("choices", None)
        if choices == None or len(choices) == 0:
            raise HTTPException("OpenAI response does not contain choices object or choices object is empty")
        
        firstChoice = choices[0]
        if not isinstance(firstChoice, dict):
            firstChoice = vars(firstChoice)
        if firstChoice == None or len(firstChoice) == 0:
            raise HTTPException("OpenAI response first choice is empty.")
        
        message = firstChoice.get("message", None)
        if not isinstance(message, dict):
            message = vars(message)
        if message == None or len(message) == 0:
            raise HTTPException("OpenAI first choice does not contain message or message object is empty")
        
        content = message.get("content", None)
        if content == None or len(content) == 0:
            raise HTTPException("OpenAI message does not contain content or content string is empty")
        
        # TODO - change the rely on the <b> and <hr> tags that I ask GPT to insert to mark sections and keywords

        contentLowercase = content.lower()
        endBoldTagKeyword = "</b>"
        
        promptStartIndex = contentLowercase.index(endBoldTagKeyword)
        promptEndIndex = findSectionEndIndex(contentLowercase, promptStartIndex)
        promptContent = content[ promptStartIndex + len(endBoldTagKeyword) : promptEndIndex ].strip()

        outlineStartIndex = contentLowercase.index(endBoldTagKeyword, promptEndIndex)
        outlineEndIndex = findSectionEndIndex(contentLowercase, outlineStartIndex)
        outlineContent = content[ outlineStartIndex + len(endBoldTagKeyword) : outlineEndIndex ].strip()
        trailingWordIndex = outlineContent.rindex(".")
        # Prepending a newline character will give all list numberings a common format
        outlineContent = "\n" + outlineContent[0 : trailingWordIndex + 1]
        outlineSteps = re.split(r'\n[0-9]+\.', outlineContent)
        # After splitting the steps into an array, double check for empty values and remove
        for outlineStep in outlineSteps:
            if outlineStep == "":
                outlineSteps.remove(outlineStep)

        codeStartIndex = contentLowercase.index(endBoldTagKeyword, outlineEndIndex)
        codeEndIndex = findSectionEndIndex(contentLowercase, codeStartIndex)
        codeContent = content[ codeStartIndex + len(endBoldTagKeyword) : codeEndIndex ].strip()

        explanationStartIndex = contentLowercase.index(endBoldTagKeyword, codeEndIndex)
        explanationEndIndex = findSectionEndIndex(contentLowercase, explanationStartIndex)
        # If end index is -1, then <hr> and <b> tag was not found from the beginning of the last block to end of text. Therefore, take end of string as final index.
        if explanationEndIndex == -1:
            explanationEndIndex = len(contentLowercase)
        explanationContent = content[ explanationStartIndex + len(endBoldTagKeyword) : explanationEndIndex ].strip()

        formattedCompletions[completionWithKey["key"]] = {
            "prompt": promptContent,
            "outline": outlineSteps,
            "code": codeContent,
            "explanation": explanationContent
        }

    print("----- Formatted OpenAI Response Object -----")
    print(json.dumps(formattedCompletions, indent=4))
    print("--------------------------------------------")

    return formattedCompletions

def findSectionEndIndex(contentLowercase : str, startIndex : int):
    hrTagKeyword = "<hr>"
    boldTagKeyword = "<b>"

    try:
        hrEndIndex = contentLowercase.index(hrTagKeyword, startIndex)
        return hrEndIndex
    except:
        print("Could not find hr html tag while searching section with start index of " + str(startIndex))
        try:
            boldEndIndex = contentLowercase.index(boldTagKeyword, startIndex)
            return boldEndIndex
        except:
            print("Could not find b html tag while searching section with start index of " + str(startIndex))
            return -1
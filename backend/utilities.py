from pydantic_settings import BaseSettings
from fastapi import HTTPException
import json

def validateAndParsePrompts(requestedSection: str, id: int, auth_header: str,  prompts: any, settings: BaseSettings):
    if(settings.api_auth_enabled and auth_header != settings.frontend_api_auth):
        raise HTTPException(status_code=400, detail="You are not authorized to call this endpoint.")
            
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
        # Key sections to parse - may need to add flexibility if ChatGPT ever starts to switch up ordering of sections
        promptKeyword = "Prompt:".lower()
        outlineKeyword = "Code outline:".lower()
        codeKeyword = "Code:".lower()
        explanationKeyword = "Explanation:".lower()
        codeCommentKeyword = "```".lower()

        completion = completionWithKey["completion"]

        completions = completion.get("completions", None)
        if completions == None or len(completions) == 0:
            raise HTTPException("OpenAI response does not contain at least 1 completion or the completion is empty.")

        item = completions.get("1", None)
        if item == None or len(item) == 0:
            raise HTTPException("OpenAI response does not contain at least 1 item or first item is empty.")

        choices = item.get("choices", None)
        if choices == None or len(choices) == 0:
            raise HTTPException("OpenAI response does not contain choices object or choices object is empty")
        
        firstChoice = choices[0]
        if firstChoice == None or len(firstChoice) == 0:
            raise HTTPException("OpenAI response first choice is empty.")
        
        message = firstChoice.get("message", None)
        if message == None or len(message) == 0:
            raise HTTPException("OpenAI first choice does not contain message or message object is empty")
        
        content = message.get("content", None)
        if content == None or len(content) == 0:
            raise HTTPException("OpenAI message does not contain content or content string is empty")
        
        contentLowercase = content.lower()
        promptIndex = contentLowercase.index(promptKeyword)
        outlineIndex = contentLowercase.index(outlineKeyword)
        codeIndex = contentLowercase.index(codeKeyword)

        # Sometimes the word "Explanation" will not show up, so we will need to index on the triple backticks at the end of the code
        explanationIndex = -1
        explanationKeywordLen = -1
        try:
            explanationIndex = contentLowercase.index(explanationKeyword)
            explanationKeywordLen = len(explanationKeyword)
        except:
            print("'Explanation:' was not found - instead indexing on ```")
            startIndex = contentLowercase.index(codeCommentKeyword)
            explanationIndex = contentLowercase.index(codeCommentKeyword, startIndex + len(codeCommentKeyword))
            explanationKeywordLen = len(codeCommentKeyword)
        
        promptContent = content[promptIndex + len(promptKeyword) : outlineIndex].strip()
        outlineContent = content[outlineIndex + len(outlineKeyword) : codeIndex].strip()

        # Here we need special behavior to account for the possible differences in what the explanation section index may be
        # We are particularly concerned with inadvertently excluding the end of the code block denoted by triple backticks
        if explanationKeywordLen == 3:
            codeContentEndingIndex = explanationIndex + 3
        else:
            codeContentEndingIndex = explanationIndex
        codeContent = content[codeIndex + len(codeKeyword) : codeContentEndingIndex].strip()

        explanationContent= content[explanationIndex + explanationKeywordLen : len(content)].strip()

        formattedCompletions[completionWithKey["key"]] = {
            "prompt": promptContent,
            "outline": outlineContent,
            "code": codeContent,
            "explanation": explanationContent
        }

    print("----- Formatted OpenAI Response Object -----")
    print(json.dumps(formattedCompletions, indent=4))
    print("--------------------------------------------")

    return formattedCompletions
from pydantic_settings import BaseSettings
from fastapi import HTTPException
import time

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
    for completion in completionsWithKeys:
        # TODO - parse actual completion into tokens (prompt, code outline, etc) for easier use on frontend
        
        # Key sections to parse
        # "Prompt:"
        # "Code Outline:"
        # "Code:"
        # "Explanation:"
        
        formattedCompletions[completion["key"]] = completion["completion"]
    return formattedCompletions
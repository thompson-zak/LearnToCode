from pydantic_settings import BaseSettings
from fastapi import HTTPException
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import traceback
import uuid
import datetime
from prompts import getPrompts


def getMongoConnectionUri(settings: BaseSettings):
    mongo_conn_start = "mongodb+srv://"
    mongo_conn_end = "@learntocodecluster0.pvsvjov.mongodb.net/?retryWrites=true&w=majority"
    return mongo_conn_start + settings.mongo_db_user + ":" + settings.mongo_db_pass + mongo_conn_end


def createAndStoreUserToken(settings: BaseSettings, tokenCache: dict):
    uri = getMongoConnectionUri(settings)
    client = MongoClient(uri, server_api=ServerApi('1'), uuidRepresentation='standard', tz_aware=True)

    try:
        db = client.learntocodedb
        sessions = db.sessions

        newToken = uuid.uuid4()
        currentTime = datetime.datetime.now(tz=datetime.timezone.utc)
        tokenLife = datetime.timedelta(weeks=1)
        expirationDate = currentTime + tokenLife
        newSession = {
            "token": newToken,
            "expirationDate": expirationDate
        }
        sessions.insert_one(newSession)

        insertTokenIntoCache(newToken, expirationDate, tokenCache)

        return newToken
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="There was an issue authenticating your session.")


def validateAuthHeader(auth_header: str, settings: BaseSettings, tokenCache: dict):

    if(settings.api_auth_enabled and not tokenIsPresentInCache(uuid.UUID(auth_header), tokenCache)):
        uri = getMongoConnectionUri(settings)
        client = MongoClient(uri, server_api=ServerApi('1'), uuidRepresentation='standard', tz_aware=True)
        # Need to check MongoDB instance for token existence and validity (not expired)
        try:
            db = client.learntocodedb
            sessions = db.sessions

            queryParameters = {
                "token": uuid.UUID(auth_header),
                "expirationDate": { "$gt": datetime.datetime.now(tz=datetime.timezone.utc) }
            }

            session = sessions.find_one(queryParameters)

            if session == None:
                raise HTTPException(status_code=401, detail="You are not authorized to call this endpoint. Please log in again.")
            else:
                insertTokenIntoCache(uuid.UUID(auth_header), session.get('expirationDate'), tokenCache)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="There was an issue authenticating your session.")
    
    return True


def validateCode(code: str, auth_header: str, settings: BaseSettings, tokenCache: dict):
    validateAuthHeader(auth_header, settings, tokenCache)

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

        raise HTTPException(status_code=400, detail=errorObject)

    return None


def validateAndParsePrompts(requestedSection: str, id: int, auth_header: str, settings: BaseSettings, tokenCache: dict):
    validateAuthHeader(auth_header, settings, tokenCache)
            
    prompts = getPrompts()
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


def tokenIsPresentInCache(token: uuid, tokenCache: dict):
    expirationDate = tokenCache.get(token)
    if(expirationDate is None):
        return False

    if(datetime.datetime.now(tz=datetime.timezone.utc) > expirationDate):
        tokenCache.pop(token)
        return False
    else:
        return True


def insertTokenIntoCache(token: uuid, expirationDate: datetime, tokenCache: dict):
    tokenCache[token] = expirationDate
import json
import re
from io import StringIO
from html.parser import HTMLParser
from fastapi import HTTPException

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()


def extractOpenAiContent(completion):
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

    return content


def formatCompletions(completionsWithKeys):
    formattedCompletions = {}
    for completionWithKey in completionsWithKeys:

        completion = completionWithKey["completion"]
        if not isinstance(completion, dict):
            completion = vars(completion)

        print("------------Completion------------")
        print(completion)
        print("----------------------------------")

        content = extractOpenAiContent(completion)
        
        # TODO - change the rely on the <b> and <hr> tags that I ask GPT to insert to mark sections and keywords

        contentLowercase = content.lower()
        endBoldTagKeyword = "</b>"
        
        promptStartIndex = contentLowercase.index(endBoldTagKeyword)
        promptEndIndex = findSectionEndIndex(contentLowercase, promptStartIndex)
        promptContent = stripTags(content[ promptStartIndex + len(endBoldTagKeyword) : promptEndIndex ]).strip()

        outlineStartIndex = contentLowercase.index(endBoldTagKeyword, promptEndIndex)
        outlineEndIndex = findSectionEndIndex(contentLowercase, outlineStartIndex)
        outlineContent = stripTags(content[ outlineStartIndex + len(endBoldTagKeyword) : outlineEndIndex ]).strip()
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
        codeContent = stripTags(content[ codeStartIndex + len(endBoldTagKeyword) : codeEndIndex ]).strip()

        explanationStartIndex = contentLowercase.index(endBoldTagKeyword, codeEndIndex)
        explanationEndIndex = findSectionEndIndex(contentLowercase, explanationStartIndex)
        # If end index is -1, then <hr> and <b> tag was not found from the beginning of the last block to end of text. Therefore, take end of string as final index.
        if explanationEndIndex == -1:
            explanationContent = content[ explanationStartIndex + len(endBoldTagKeyword) : ]
        else:
            explanationContent = content[ explanationStartIndex + len(endBoldTagKeyword) : explanationEndIndex ]
        explanationContent = stripTags(explanationContent).strip()

        formattedCompletions[completionWithKey["key"]] = {
            "prompt": promptContent,
            "outline": outlineSteps,
            "code": codeContent,
            "explanation": explanationContent,
            "rawContent": content
        }

    print("----- Formatted OpenAI Response Object -----")
    print(json.dumps(formattedCompletions, indent=4))
    print("--------------------------------------------")

    return formattedCompletions


def formatValidityCompletion(completion):
    print("------------Completion------------")
    print(completion)
    print("----------------------------------")

    content = extractOpenAiContent(completion)
    contentLowercase = content.lower()
    return {
        "isValid": contentLowercase.contains("yes")
    }


def findSectionEndIndex(contentLowercase : str, startIndex : int):
    hrTagKeyword = "<hr>"
    boldTagKeyword = "<b>"

    try:
        boldEndIndex = contentLowercase.index(boldTagKeyword, startIndex)
        return boldEndIndex
    except:
        print("Could not find b html tag while searching section with start index of " + str(startIndex))
        return -1
    

def stripTags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
RESPONSE_STRUCTURE = " Your response should contain a prompt, an outline of steps to be completed, a code sample, and an explanation with each section titled in <b> html tags as I just listed and followed by an <hr> html tag."
NO_INPUT_ONLY_PRINT = " This code should not contain any input statements and should rely only a print statements for displaying output."

PROMPT_INSTRUCTIONS = RESPONSE_STRUCTURE + NO_INPUT_ONLY_PRINT

prompts = {
    "Variables": {
        1: "Please provide a very basic problem to help a student who has never coded before learn python syntax and variables." + PROMPT_INSTRUCTIONS,
        2: "Please provide a prompt and code outline for a problem to help a student who has never coded before learn python syntax and variables." + PROMPT_INSTRUCTIONS
    },
    "Data": {},
    "Conditionals": {},
    "OOP": {}
}

def getPrompts():
    return prompts
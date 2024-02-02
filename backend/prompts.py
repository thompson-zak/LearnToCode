RESPONSE_SECTIONS = " Your response should contain a prompt, an outline of steps to be completed, a code sample, and an explanation."
SECTION_STRUCTURE = " Each section should be titled in <b> html tags and followed by an <hr> html tag. Each step in the outline of steps should end with a period."
NO_INPUT_ONLY_PRINT = " This code should not contain any input statements and should rely only a print statements for displaying output."

PROMPT_INSTRUCTIONS = RESPONSE_SECTIONS + SECTION_STRUCTURE + NO_INPUT_ONLY_PRINT

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
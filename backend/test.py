from main import formatCompletions
import json
import traceback
import sys


# Sample Completion 1 updated to better reflect new OpenAI response with nested objects rather than JSON
def testVariablesFormatCompletions1():
    file = open('./test_resources/variables/sample_completion_1.json')
    completion = json.load(file)
    print("Loaded completion from file 1...")
    completionWithKey = [{
        "key": 1,
        "completion": completion
    }]
    formattedCompletions = formatCompletions(completionWithKey)
    print("----------------------------------")
    return formattedCompletions


# Sample Completion 2 updated to better reflect new OpenAI response with nested objects rather than JSON
def testVariablesformatCompletions2():
    file = open('./test_resources/variables/sample_completion_2.json')
    completion = json.load(file)
    print("Loaded completion from file 2...")
    completionWithKey = [{
        "key": 1,
        "completion": completion
    }]
    formattedCompletions = formatCompletions(completionWithKey)
    print("----------------------------------")
    return formattedCompletions


def testCompileBehavior():
    codeBlock = "This is not python code!"
    codeObject = compile(codeBlock, "userCode", "exec")


def testDataFormatCompletions1():
    file = open('./test_resources/data/sample_completion_1.json')
    completion = json.load(file)
    print("Loaded completion from file 1...")
    completionWithKey = [{
        "key": 1,
        "completion": completion
    }]
    formattedCompletions = formatCompletions(completionWithKey)
    print("----------------------------------")
    return formattedCompletions
            
# Dummy change 6 - test cloud run trigger
if __name__ == "__main__":
    #testVariablesFormatCompletions1()
    #testVariablesFormatCompletions2()
    #testCompileBehavior()
    testDataFormatCompletions1()
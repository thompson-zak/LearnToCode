from main import formatCompletions
import json


def testformatCompletions():
    file = open('./test_resources/sample_completion.json')
    completion = json.load(file)
    completionWithKey = {
        1: completion
    }
    formattedCompletions = formatCompletions(completionWithKey)
    formattedPrint(formattedCompletions)


def formattedPrint(message: str, testName: str):
    print(testName)
    print("-----------------------------------")
    print(message)
    print("--------Test Complete---------")


if __name__ == "__main__":
    testformatCompletions()
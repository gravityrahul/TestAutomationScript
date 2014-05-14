import os
import json

def  parseTestFiletoDict(filename):
    json_data = open(filename)
    testCaseObject = json.load(json_data)
    return testCaseObject


if __name__ == "__main__":
    parseTestFiletoDict("/home/rahul/QATEST/integration/test_definition.tdf")

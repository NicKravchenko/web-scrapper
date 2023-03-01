import json


def readFile(route):
    fileObject = open(route, "r")
    jsonContent = fileObject.read()
    readed = json.loads(jsonContent)
    fileObject.close()
    return readed


def writeFile(route, content):
    jsonString = json.dumps(content)

    jsonFile = open(route, "w")
    jsonFile.write(jsonString)

    jsonFile.close()


from numpy import *
import numpy.ma as ma

class Population:

    #########################

    def __init__(self, populationSize, parentModel):

        self.populationSize = populationSize
        self.timeStepMem = 2
        self.attributes = {'state': None}
        self.updateCode = []
        self.currentstates = []
        self.model = parentModel

    #########################

    def setglobal(self, attributeName, value):
        self.model.globals[attributeName] = value

    #########################

    def getglobal(self, attributeName):
        return self.model.globals[attributeName]

    #########################

    def getfrom(self, populationName, attributeName, t):
        readIndex = t
        return self.model.populations[populationName].attributes[attributeName][readIndex]

    #########################

    def get(self, attributeName, t):
        readIndex = t
        while readIndex >= self.timeStepMem:
            readIndex -= self.timeStepMem
        return self.attributes[attributeName][readIndex]

    #########################

    def getstates(self, populationName):
        return self.currentstates

    #########################

    def calculateNewArray(self, oldValues, newValues, trueFalseMask):
        resultArray = oldValues
        for index, value in enumerate(newValues):
            print trueFalseMask
            if trueFalseMask[index] == True:
                resultArray[index] = newValues[index]
            #else:
            #    resultArray.append(oldValues[index])

        return resultArray

    #########################

    def update(self, attributeName, newValues, trueFalseMask, t):
        writeIndex = t + 1
        oldValues = self.get(attributeName, t)
        while writeIndex >= self.timeStepMem:
            writeIndex -= self.timeStepMem
        maskedArray = ma.array(newValues, mask=trueFalseMask)

        result = self.calculateNewArray(oldValues, newValues, trueFalseMask)

        print "old " + attributeName + ": " + str(oldValues)
        print "new " + attributeName + ": " + str(newValues)
        print "mask " + attributeName + ": " + str(maskedArray)
        print "result " + attributeName + ": " + str(result)

        self.attributes[attributeName][writeIndex] = result

    #########################

    def declareAttribute(self, attributeName):
        self.attributes[attributeName] = None

    #########################

    def addState(self, stateName):
        self.currentstates.append(stateName)

    #########################

    def addUpdateCode(self, codeString):
        self.updateCode.append(codeString)

    #########################

    def updateAttributes(self, attributes, t):

        setglobal = lambda attributeName, value : self.setglobal(attributeName, value)
        update = lambda attributeName, value, mask : self.update(attributeName, value, mask, t)
        get = lambda attributeName : self.get(attributeName, t)
        getglobal = lambda attributeName : self.getglobal(attributeName)
        getfrom = lambda populationName, attributeName : self.getfrom(populationName, attributeName, t)
        getstates = lambda populationName : self.getstates(populationName)

        for codeblock in self.updateCode:
            code = compile(codeblock, "<string>", "exec")
            exec code in globals(), locals()

        # for stateKey, data in self.stateData.items():
        #     for codeblock in data["updateCode"]:
        #         code = compile(codeblock, "<string>", "exec")
        #         exec code in globals(), locals()

    #########################



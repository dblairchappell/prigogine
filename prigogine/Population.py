
import numpy as np
class Population:

    #########################

    def __init__(self, parentModel):

        self.popsize = 0
        self.updateCode = []
        self.model = parentModel
        self.t = 0
        self.variables = []

    #########################

    def create(self, popsize):
        self.popsize = popsize
        for varName in self.variables:
            exec "self.%(variable)s = np.zeros((2,popsize))" % \
                 {"variable" : varName}

    #########################

    def init(self, varName, expression):

        exec "self.%s = np.zeros((2,self.popsize))" % varName

        code = "self.%(varName)s[0] = %(expression)s" % \
             {"varName" : varName, "expression" : expression}
        exec code in globals(), locals()

        code = "self.%(varName)s[1] = %(expression)s" % \
               {"varName" : varName, "expression" : expression}
        exec code in globals(), locals()

    #########################

    def evalUpdateCode(self):
        update = lambda variableName, value, conditionalCheck, t: self.update(variableName, value, conditionalCheck, self.model.t)
        updateMap = lambda variableName, value, conditionalCheck, t: self.updateMap(variableName, value, conditionalCheck, self.model.t)
        for code in self.updateCode:
            exec code in globals(), locals()

    #########################

    @staticmethod
    def calculateNewArray(oldVals, newVals, trueFalse):
        resultArray = oldVals
        for index in np.where(trueFalse):
            resultArray[index] = newVals[index]
        return resultArray

    #########################

    def update(self, variableName, newValues, conditionalCheck, t):
        readIndex = self.model.readIndex
        writeIndex = self.model.writeIndex
        t = readIndex
        oldVals = eval("self.%s[readIndex]" % variableName)
        newVals = eval(newValues)
        trueFalse = eval(conditionalCheck)
        result = self.calculateNewArray(oldVals, newVals, trueFalse)
        codeblock = "self.%(variableName)s[%(writeIndex)d] = result" % \
             {"variableName" : variableName, "result" : result, "writeIndex" : writeIndex}
        code = compile(codeblock, "<string>", "exec")
        exec code in locals(), globals()

    #########################

    def updateMap(self, variableName, newValue, conditionalCheck, t):
        readIndex = self.model.readIndex
        writeIndex = self.model.writeIndex
        t = readIndex
        oldVals = eval("self.%s[readIndex]" % variableName)
        newVals = eval("self.%s[readIndex].copy()" % variableName)
        newVals.fill(eval(newValue))
        trueFalse = eval(conditionalCheck)
        result = self.calculateNewArray(oldVals, newVals, trueFalse)

        codeblock = "self.%(variableName)s[%(writeIndex)d] = result" % \
             {"variableName" : variableName, "result" : result, "writeIndex" : writeIndex}
        code = compile(codeblock, "<string>", "exec")
        exec code in locals(), globals()

    #########################

    # class init:
    #
    #     def __init__(self, varName):
    #         self.variable = varName
    #
    #     def getvarname(self):
    #         return self.variable
    #
    #     def choice(self, choiceArray, probabilityArray):
    #         print self.variable
    #
    #     def randint(self, range):
    #         print
    #
    #     def constant(self, value):
    #         print "testing"


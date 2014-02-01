#Imports modules
import random
import sys

class cTestTool():
    """Provides tools for unittesting functions/objects and for mocking their
    "Requirements, such as input, print and the random module.

    If you want to use this class, just subclass it
      and put in a test method for each function or method
      you want to unittest in your code.
      (ps. the test methods name needs to start with mTest)

    To mock input use the mSetInput method,
      to mock the random module use the SetRandom method"""
    def __init__(self, bQuiet=False):
        "Collects all test method in it's subclasses."
        self.bQuiet = bQuiet
        self.lsPrintOutput = []

        #Collect all names to the methods in this class that starts with mTest
        self.lsTestMethods = [s for s in dir(self) if s.startswith("mTest")]

    def __call__(self, bQuitAfter=False):
        "Runs all class methods starting with mTest"
        #prints start message
        self.mPrint("STARTING UNITTESTS")

        #Turn on mocking for the print function
        sys.stdout = self

        #Turn on mocking for the input function
        sys.stdin = self

        #Turn on mocking for the random module, and backups the original
        Randombackup = random
        globals()["random"] = self

        #Declare a variable to count the number of tests
        iTests = 0

        #Run all methods that starts with mTest in this class
        for sTestMethod in self.lsTestMethods:
            #Resets counter for number of tests in this method
            self.iMethodTests = 0

            #Print message
            self.mPrint("Running tests in method: %s" % sTestMethod, end="")

            #Run testmethod
            eval("self." + sTestMethod + "()")

            #Print rest of message
            self.mPrint("#n>%s tests completed.#n" % self.iMethodTests)

            #Inrease testnumber with the number of tests in this method
            iTests += self.iMethodTests

        #Turn off mocking for the print function
        sys.stdout = sys.__stdout__

        #Turn on mocking for the input function
        sys.stdin = sys.__stdin__

        #Turn on mocking for the random module
        globals()["random"] = Randombackup

        #prints end message
        self.mPrint("UNITTESTS COMPLETED, %s TESTS COMPLETED" % iTests)

        #Exits the program after testing if self.bQuitAfterwards is True
        if bQuitAfter:
            exit(0)

        #Returns True in case this object has been called by an assert
        return(True)

    def mPrint(self, *lxArgs, **dKeywords):
        "A print method that works similar as the python3's print function"

        #Sends a string representation to the proper stdout.write method
        sys.__stdout__.write(self.msFormat(*lxArgs, **dKeywords))

    def mCheck(self, xTest, xExpected=True):
        """Tests sTestString against xExpected.
        xTest can either be an object or an executable string,
          if it's an executable string mCheck will execute it
          and store the result or any exception it raises into xResult.

        mCheck will then compare xResult and xExpected
          to see if it's a successfull test or not and print the results.
        """
        #Increases the test count
        self.iMethodTests += 1

        #Resets self.llsPrintOutput
        self.lsPrintOutput = []

        #Tries to run xTest while storing the result in xResult
        try:
            xResult = eval(str(xTest), globals(), globals())

        #If it can't run xTest
        except Exception as e:
            #Store the exception in xResult
            xResult = e.__class__

        #If xExpected is xResult or xTest
        if xExpected in (xResult, xTest):
            if not self.bQuiet:
                self.mPrint("#n  Successful test: '%s'"
                            % str(xTest)[:40], end="")
        else:
            self.mPrint("#nFAILED TEST: '%s'" % str(xTest)[:80])
            self.mPrint("   EXPECTED: '%s'" % str(xExpected)[:80])
            self.mPrint("   RECEIVED: '%s'" % str(xResult)[:80], end="")

    #Contains tools for mocking the input function
    def readline(self, sDummy=""):
        "Returns the string supplied by mSetInput instead of an actual input"
        if len(self.lsInputs) == 0:
            self.mPrint("FAILED TEST, SUPPLY MORE INPUTS!")
            return("")
        else:
            return(self.lsInputs.pop())

    def mSetInput(self, lxInputs):
        "Reverses lxInputs and converts all values inside to strings."
        self.lsInputs = [str(x) for x in reversed(lxInputs)]

    #Contains tools for mocking the print function
    def write(self, sString):
        "Copies all sent prints into a variable."
        self.lsPrintOutput.append(sString)

    def msFormat(self, *lxArgs, **dKeywords):
        "Formats arguments almost like the print function in python3 does."

        #Creates a list of strings from lxArgs
        lsStrings = [str(s) for s in lxArgs]

        #Replaces all newlines with the text "\n"
        lsStrings = [s.replace("\n", "\\n") for s in lsStrings]

        #Replaces all horisontal tabs with the text "\t"
        lsStrings = [s.replace("\t", "\\t") for s in lsStrings]

        #Replaces all #n with \n (newlines) (so we have access to newlines)
        lsStrings = [s.replace("#n", "\n") for s in lsStrings]

        #Replaces all #t with \t (newlines) (so we have access to tabs)
        lsStrings = [s.replace("#t", "\t") for s in lsStrings]


        #Collects the correct keywords sep and end
        sSep = dKeywords.get("sep", ", ")
        sEnd = dKeywords.get("end", "\n")

        #Joins the list together
        sOutput = sSep.join(lsStrings) + sEnd
        return(sOutput)

    def msPrintOutput(self):
        return("".join(self.lsPrintOutput))

    #Contains tools for mocking the random module
    def seed(self, xDummy):
        "Dummy function made for mocking the seed function in the random module"
        return(False)

    def randrange(self, *Dummyargs):
        """Returns the number supplied by mSetRandom
         instead of an actual random number"""
        if len(self.liNumbers) == 0:
            self.mPrint("FAILED TEST, SUPPLY MORE RANDOM NUMBERS!")
            return("")
        else:
            return(self.liNumbers.pop())

    def choice(self, lx, *args):
        if len(self.liNumbers) == 0:
            self.mPrint("FAILED TEST, SUPPLY MORE RANDOM NUMBERS!")
            return("")
        else:
            return(lx[self.liNumbers.pop()])

    def mSetRandom(self, liNumbers):
        liNumbers.reverse()
        self.liNumbers = liNumbers

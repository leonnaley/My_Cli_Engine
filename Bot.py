from pdb import set_trace as t
import random


class cChar():
    """A class that will declare itself a character, allow itself to be called
    and append itself to a given list."""

    #Handles creation
    def __init__(self, loList, sChar=None):
        """Declares self.sChar, which is used when representing
        itself, and appends itself to the given loList."""

        #Declares object variables
        self.loList = loList

        #Places the bot into the given list
        self.loList.append(self)

        #Sets self.sChar
        self.sChar = self.msFindChar(sChar)

    def mAct(self):
        """This method will run when this object is called.
        Subclass this method for your convinience."""

    def msFindChar(self, sChar=None):
        "Returns a random char if None is given, else return sChar."
        #if sChar is not given
        if sChar is None:
            #Return a random character
            return(chr(random.randrange(33, 127)))

        #if sChar is given
        else:
            return(sChar)

    #Python internal methods
    def __add__(self, xOther):
        "Handles how to add this bot together with other objects."
        return(self.sChar + str(xOther))

    def __call__(self):
        "Takes one step with this bot."
        self.mAct()

    def __del__(self):
        "Removed itself from self.loList."
        self.loList.remove(self)

    def __radd__(self, xOther):
        "Handles how to add this bot together with other objects."
        return(str(xOther) + self.sChar)

    def __repr__(self):
        "Handles how this bot represent itself when called."
        return(self.sChar)


class cBot(cChar):
    """A subclass of the cChar class, this class will place itself into a
    given layer object, and allow movement within it."""

    #Handles creation
    def __init__(self, oMatrix, loList, sChar=None, tiPosition=None):
        """Declares object variables and places itself into oMatrix."""
        #Initialises its parent class
        cChar.__init__(self, loList, sChar)

        #Declares object variables
        self.oMatrix = oMatrix

        #Sets self.tiPosition
        self.tiPosition = self.mtiFindPosition(tiPosition)

        #Forcibly place the bot into self.oMatrix
        self.oMatrix[self.tiPosition] = self

    def mtiFindPosition(self, tiPosition=None):
        """Returns a random empty position if tiPosition is not given."""
        #if tiPosition is not given
        if tiPosition is None:
            #Set tiPosition to an empty position
            for _i in range(self.oMatrix.iWidth*self.oMatrix.iHeight):
                #Creates a new random position
                iX = random.randrange(0, self.oMatrix.iWidth)
                iY = random.randrange(0, self.oMatrix.iHeight)

                #If the random position is empty
                if self.oMatrix[iY, iX] is None:

                    #Return the empty position
                    tiPosition = (iY, iX)
                    break

            #If you fail to find an empty position
            else:
                #stop the program by raising an exception
                raise Exception("No empty space found!")

        #Return tiPosition
        return(tiPosition)

    def mbMove(self, sDirection):
        "Moves itself in a given direction. Returns True if successful."
        #Calculates the new position
        tiNewPosition = self.mtiCalcPosition(sDirection)

        #if the cell we are moving to is empty
        if self.oMatrix[tiNewPosition] is None:

            #Place ourself in the new position
            self.oMatrix[tiNewPosition] = self

            #Place an empty cell in the old position
            self.oMatrix[self.tiPosition] = None

            #Change our position
            self.tiPosition = tiNewPosition

            #Return True as the move was a success
            return(True)

        #If the cell we are moving to is not empty
        else:
            #Return False as the move was a failure
            return(False)

    def mtiCalcPosition(self, sDirection):
        "Calculates and returns a new position taking edges into account."
        iY, iX = self.tiPosition

        #Handles left and right
        if sDirection.endswith("left"):
            iX -= 1
        elif sDirection.endswith("right"):
            iX += 1
        #Handles up and down
        if sDirection.startswith("up"):
            iY -= 1
        elif sDirection.startswith("down"):
            iY += 1

        #Takes the horisontal edge into consideration
        if iX < 0:
            iX = self.oMatrix.iWidth-1
        elif iX > self.oMatrix.iWidth-1:
            iX = 0
        #Takes the vertical edge into consideration
        if iY < 0:
            iY = self.oMatrix.iHeight-1
        elif iY > self.oMatrix.iHeight-1:
            iY = 0

        #Returns the calculated position
        return(iY, iX)

    #Python internal methods
    def __del__(self):
        "Deletes this bot from self.oMatrix and self.loList."

        #Deletes itself from self.oMatrix
        del self.oMatrix[self.tiPosition]

        #Removes itself from self.loList
        if self in self.loList:
            self.loList.remove(self)


class cLivingBot(cBot):
    """A subclass of the cBot class, this class will add iMoves, sDirection
    and iHealth."""
    def __init__(self, oMatrix, loList, sChar=None, tiPosition=None,
                 sDirection=None, iHealth=100):
        "Declares iMoves, iHealth and sDirection in addition to calling cBot."
        self.mInitialize()
        cBot.__init__(self, oMatrix, loList, sChar, tiPosition)
        self.iMoves = 0
        self.iHealth = iHealth
        self.lsDirections = ["upleft", "up", "upright",
                             "left", "right",
                             "downleft", "down", "downright"]

        self.sDirection = self.msFindDirection(sDirection)

    def mInitialize(self):
        """Dummy method to be replaced by subclasses, this method will be run
        whenever self.__init__ is run."""

    def msFindDirection(self, sDirection=None):
        """Returns a random direction if sDirection is not given."""
        #if sDirection is not given
        if sDirection is None:
            #Find a random empty position in self.oMatrix
            sDirection = random.choice(self.lsDirections)

        #Return tiPosition
        return(sDirection)

    def mtiFindNearbyEmptySpace(self):
        "Returns a random nearby empty space, None if none found"
        #Copies self.lsDirections
        lsDirections = list(self.lsDirections)

        #Randomly shuffles lsDirections
        random.shuffle(lsDirections)

        #Loops through all directions
        for sDirection in lsDirections:

            #Calculate possible position, based on direction
            tiPosition = self.oMatrix.mtiCalcPosition(self.tiPosition,
                                                      sDirection)

            #If that position is empty
            if self.oMatrix.mbEmptyPosition(tiPosition):

                #Return that position
                return(tiPosition)

        #No positions have been found, return None
        return(None)

    def moTarget(self, sDirection):
        "Returns a target in a given direction"
        tiTargetPosition = self.mtiCalcPosition(sDirection)
        return(self.oMatrix[tiTargetPosition])

    #Python internal methods
    def __call__(self):
        "Takes one step with this bot."
        self.iMoves += 1

        if self.iHealth <= 0:
            self.__del__()
            return

        self.mAct()

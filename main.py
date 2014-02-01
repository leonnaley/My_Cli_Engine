#Imports modules
from pdb import set_trace as t
import Bot
import Game
import Map
import random
import time

class cUpBot(Bot.cLivingBot):
    def mAct(self):
        self.mbMove("up")
    def msFindChar(self, sDummy):
        return("^")

class cDownBot(Bot.cLivingBot):
    def mAct(self):
        self.mbMove("down")
    def msFindChar(self, sDummy):
        return("v")

class cLeftBot(Bot.cLivingBot):
    def mAct(self):
        self.mbMove("left")
    def msFindChar(self, sDummy):
        return("<")

class cRightBot(Bot.cLivingBot):
    def mAct(self):
        self.mbMove("right")
    def msFindChar(self, sDummy):
        return(">")

class cRandomDirectionBot(Bot.cLivingBot):
    def mAct(self):
        self.mbMove(self.sDirection)
        if random.randrange(5) == 0:
            self.sDirection = random.choice(self.lsDirections)
    def msFindChar(self, sDummy):
        return("x")

class cGameOfLifeBot(Bot.cLivingBot):
    def __init__(self, oMatrix, loBots, tiPosition):
        sChar = random.choice(["O", " "])
        Bot.cLivingBot.__init__(self, oMatrix, loBots, sChar, tiPosition)
        self.bCount = True

    def mAct(self):
        if self.bCount:
            self.mCount()
        else:
            self.mDisplay()
        self.bCount = (not self.bCount)

    def mCount(self):
        iCount = self.miCount()
        if (iCount == 2) and (self.sChar == "O"):
            self.bActive = True
        elif iCount == 3:
            self.bActive = True
        else:
            self.bActive = False

    def mDisplay(self):
        if self.bActive:
            self.sChar = "O"
        else:
            self.sChar = " "

    def miCount(self):
        "Returns the number of bots nearby"
        iCount = 0
        for sDirection in self.lsDirections:
            oTarget = self.moTarget(sDirection)
            if oTarget.sChar == "O":
                iCount += 1

        return(iCount)

class cGameOfLife(Game.cWorld):
    def mloCreateBots(self, iLayers, tiBots, tcBotClasses):
        loBots = []
        for iY in range(self.loLayers[0].iHeight):
            for iX in range(self.loLayers[0].iWidth):
                cGameOfLifeBot(self.loLayers[0], loBots, tiPosition=(iY, iX))

        return(loBots)

class cKnightBot(Bot.cLivingBot):
    def mInitialize(self):
        self.iVariant = random.randrange(1, 20)

    def msFindChar(self, sDummy):
        return(chr(65+self.iVariant))

    def mAct(self):
        self.iHealth -= 1
        if random.randrange(self.iVariant) == 0:
            self.sDirection = random.choice(self.lsDirections)
        if not self.mbMove(self.sDirection):
            if self.moTarget(self.sDirection).__class__ == self.__class__:
                self.moTarget(self.sDirection).iHealth = 0
                self.iHealth += 50
            else:
                self.sDirection = random.choice(self.lsDirections)


#Creates the game with layers and bots
oGame1 = Game.cWorld(iLayers=5,
                   tiBots=(50, 50, 50, 50, 50),
                   tcLayerClasses=(Map.cTextureLayer, Map.cTextureLayer, Map.cTextureLayer, Map.cTextureLayer, Map.cTextureLayer),
                   tcBotClasses=(cUpBot, cDownBot, cLeftBot, cRightBot, cRandomDirectionBot))

oGame2 = cGameOfLife(iLayers=1,
                   tiBots=(50,),
                   tcLayerClasses=(Map.cTextureLayer,),
                   tcBotClasses=(cGameOfLifeBot,))

oGame3 = Game.cWorld(iLayers=1,
                   tiBots=(550,),
                   tcLayerClasses=(Map.cTextureLayer,),
                   tcBotClasses=(cKnightBot,))


while True:
    #Runs one round of the game
    oGame2(bGuiMode = False)
    #sleeps
    time.sleep(0.16)

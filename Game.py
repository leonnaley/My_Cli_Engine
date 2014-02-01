#Imports modules
from __future__ import print_function
from pdb import set_trace as t
import Gui

#Creates a gui object
#oWindow = Gui.cWindow(iRows=151, iColoumns=41)

#Defines classes
class cWorld():
    "Creates a world with several layers and bots to inhabit it."
    def __init__(self, iLayers, tcLayerClasses, tiBots, tcBotClasses):
        #Creates layers
        self.loLayers = self.mloCreateLayers(iLayers, tcLayerClasses)

        #Modify layers
        self.loLayers = self.mloModifyLayers(self.loLayers)

        #Creates bots
        self.loBots = self.mloCreateBots(iLayers, tiBots, tcBotClasses)

    def mloCreateBots(self, iLayers, tiBots, tcBotClasses):
        loBots = []
        for iLayer in range(iLayers):
            for _iBots in range(tiBots[iLayer]):
                tcBotClasses[iLayer](self.loLayers[iLayer], loBots)
        return(loBots)

    def mloCreateLayers(self, iLayers, tcLayerClasses):
        loLayers = []
        for iLayer in range(iLayers):
            cLayerClass = tcLayerClasses[iLayer]
            loLayers.append(cLayerClass())
        return(loLayers)

    def mloModifyLayers(self, loLayers):
        "Dummy Function, to be replaced by subclasses."
        return(loLayers)

    def __call__(self, bDecreaseSpace=False, bGuiMode=False):
        #Loops through all bots, and take it's turn
        for oBot in self.loBots[::-1]:
            oBot()

        if bDecreaseSpace:
            for oLayer in self.loLayers:
                oLayer.mDecreaseSpace()

        if bGuiMode:
            oWindow.mDisplay(self)
        else:
            #prints out the layers to the terminal
            print(self)
            print(len(self.loBots))

    def __repr__(self):
        s = str(self.loLayers[0])
        for oLayer in self.loLayers[1:]:
            s = oLayer + s
        return(s)


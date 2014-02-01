#Imports modules
import random
import Unittesting


#Defines classes
class cLayer():
    """A container class that represents a two dimensional list."""
    def __init__(self, iHeight=41, iWidth=151, xValue=None):
        "Declares its width and height, then creates its 2 dimensional list."
        #Declares object constants
        self.iWidth = iWidth
        self.iHeight = iHeight

        #Creates its two dimensional list
        self.llo = [[xValue for _iX in range(iWidth)] for _iY in range(iHeight)]

    #Python internal methods
    def __add__(self, xSecond, xFirst=None):
        "Adds itself together with another cLayer object, returns a string."
        if xFirst is None:
            xFirst = self
        llsFirst = str(xFirst).split("\n")
        llsSecond = str(xSecond).split("\n")

        sOut = ""
        for iY in range(self.iHeight):
            for iX in range(self.iWidth):
                if llsSecond[iY][iX] == " ":
                    sOut += llsFirst[iY][iX]
                else:
                    sOut += llsSecond[iY][iX]
            sOut += "\n" if (iY != len(llsFirst)-1) else ""

        return(sOut)

    def __delitem__(self, tiPosition):
        iY, iX = tiPosition
        self.llo[iY][iX] = None

    def __getitem__(self, tiPosition):
        "Handles any calls to indexing this object"
        assert(tiPosition.__class__ == tuple().__class__)

        iY, iX = tiPosition
        return(self.llo[iY][iX])

    def __len__(self):
        return(self.iWidth)

    def __radd__(self, xSecond):
        return(self.__add__(self, xSecond))

    def __repr__(self):
        "Returns the contents of this layer as a string"
        sOut = ""
        for lX in self.llo:
            for x in lX:
                sOut += x if (x is not None) else " "
            sOut += "\n"
        return(sOut[:-1])

    def __setitem__(self, tiPosition, oNewItem):
        iY, iX = tiPosition
        self.llo[iY][iX] = oNewItem


class cTextureLayer(cLayer):
    "A subclass of cLayer which provides methods for terrain and lines."

    def mCreateBorder(self, sCharacter="#"):
        "Creates a border at every edge."
        #Creates the left vertical line
        self.mbCreateVerticalLine(0, sCharacter)
        #Creates the right vertical line
        self.mbCreateVerticalLine(self.iWidth-1, sCharacter)

        #Create the top horisontal line
        self.mbCreateHorisontalLine(0, sCharacter)
        #Creates the bottom horisontal line
        self.mbCreateHorisontalLine(self.iHeight-1, sCharacter)

    def mDecreaseSpace(self, sCharacter="#"):
        "Creates walls from each side closing in on non-empty spaces."
        #Creates walls starting on the left
        for iX in range(0, self.iWidth):
            if not self.mbCreateVerticalLine(iX, sCharacter):
                break

        #Creates walls starting on the right
        for iX in range(0, self.iWidth)[::-1]:
            if not self.mbCreateVerticalLine(iX, sCharacter):
                break

        #Creates walls starting on the top
        for iY in range(0, self.iHeight):
            if not self.mbCreateHorisontalLine(iY, sCharacter):
                break

        #Creates walls starting on the bottom
        for iY in range(0, self.iHeight)[::-1]:
            if not self.mbCreateHorisontalLine(iY, sCharacter):
                break

    def mbCreateHorisontalLine(self, iY, sCharacter="#"):
        """Creates a horisontal line at iY consisting of sCharacter
        if all the spaces are empty or contain sCharacter."""

        #Loop through all horisontal at the iX Axis
        for iX in range(self.iWidth):
            #If the cell is not empty
            if self[iY, iX] not in (sCharacter, None):
                #Return False
                return(False)

        #Loop through all cells at the iX Axis
        for iX in range(self.iWidth):
            #Forcibly place a wall character
            self[iY, iX] = sCharacter

        #Return True
        return(True)

    def mbCreateVerticalLine(self, iX, sCharacter="#"):
        """Creates a vertical line at iX consisting of sCharacter
        if all the spaces are empty."""

        #Loop through all cells at the iY Axis
        for iY in range(self.iHeight):
            #If the cell is not empty
            if self[iY, iX] not in (sCharacter, None):
                #Return False
                return(False)

        #Loop through all cells at the iY Axis
        for iY in range(self.iHeight):
            #Forcibly place a wall character
            self[iY, iX] = sCharacter

        #Return True
        return(True)

    def mCreateTerrain(self, dTerrain):
        "Creates terrain in the form of characters."
        #Generates a list of characters
        #The more times the characters are in the list
        #the higher likelyhood it will be placed
        lsTextures = []
        for sTexture in list(dTerrain.keys()):
            for _i in range(dTerrain[sTexture]):
                lsTextures.append(sTexture)

        #Inserts the terrain of characters into the layer
        self._mInsertTerrain(lsTextures)

    def _mInsertTerrain(self, lsTextures):
        for iY in range(self.iHeight):
            for iX in range(self.iWidth):
                if self[iY, iX] is None:
                    self[iY, iX] = random.choice(lsTextures)


class cUnittests(Unittesting.cTestTool):
    #Tests the cLayer class
    def mTest_cLayer__init(self):
        oTest = cLayer(10, 5, "a")
        llsExpected = [["a" for iX in range(5)] for iY in range(10)]
        self.mCheck(oTest.llo, llsExpected)
        self.mCheck(oTest.iWidth, 5)
        self.mCheck(oTest.iHeight, 10)

        oTest = cLayer()
        llsExpected = [[None for iX in range(151)] for iY in range(41)]
        self.mCheck(oTest.llo, llsExpected)

    def mTest_cLayer_add(self):
        #Tests that any content in oTest2 overwrites any content i oTest
        oTest = cLayer(2, 2, "a")
        oTest2 = cLayer(2, 2, "b")
        self.mCheck(oTest.__add__(oTest2), "bb\nbb")
        #Checks that missing content in oTest2 makes oTest1 come out
        oTest = cLayer(2, 2, "a")
        oTest2 = cLayer(2, 2)
        self.mCheck(oTest.__add__(oTest2), "aa\naa")

    def mTest_cLayer_delitem(self):
        oTest = cLayer(2, 2, "a")
        del oTest[1, 1]
        self.mCheck(oTest.llo, [["a", "a"], ["a", None]])

    def mTest_cLayer_getitem(self):
        oTest = cLayer(2, 2, "a")
        oTest.llo[1][1] = "b"
        self.mCheck(oTest[0, 0], "a")
        self.mCheck(oTest[1, 1], "b")

    def mTest_cLayer_len(self):
        oTest = cLayer(2, 2)
        self.mCheck(len(oTest), 2)

    def mTest_cLayer_radd(self):
        #Tests that any content in oTest2 overwrites any content i oTest
        oTest = cLayer(2, 2, "a")
        oTest2 = cLayer(2, 2, "b")
        self.mCheck(oTest.__radd__(oTest2), "aa\naa")
        #Checks that missing content in oTest2 makes oTest1 come out
        oTest = cLayer(2, 2, "a")
        oTest2 = cLayer(2, 2)
        self.mCheck(oTest.__radd__(oTest2), "aa\naa")

    def mTest_cLayer_repr(self):
        oTest = cLayer(3, 3, "a")
        self.mCheck(oTest.__repr__(), "aaa\naaa\naaa")

    def mTest_cLayer_setitem(self):
        oTest = cLayer(2, 2)
        oTest[1, 1] = "a"
        self.mCheck(oTest.llo, [[None, None], [None, "a"]])

    #Tests the cTextureLayer class
    def mTest_cTextureLayer_mbCreateHorisontalLine(self):
        oTest = cTextureLayer(2, 2)
        oTest.mbCreateHorisontalLine(1, "a")
        lloExpected = [[None, None], ["a", "a"]]
        self.mCheck(oTest.llo, lloExpected)

        oTest = cTextureLayer(2, 2, "a")
        self.mCheck(oTest.mbCreateHorisontalLine(0), False)

    def mTest_cTextureLayer_mbCreateVerticalLine(self):
        oTest = cTextureLayer(2, 2)
        oTest.mbCreateVerticalLine(1, "a")
        lloExpected = [[None, "a"], [None, "a"]]
        self.mCheck(oTest.llo, lloExpected)

        oTest = cTextureLayer(2, 2, "a")
        self.mCheck(oTest.mbCreateVerticalLine(0), False)

    def mTest_cTextureLayer_mCreateBorder(self):
        oTest = cTextureLayer(4, 3)
        oTest.mCreateBorder()
        lloExpected = [["#", "#", "#"], ["#", None, "#"],
                       ["#", None, "#"], ["#", "#", "#"]]
        self.mCheck(oTest.llo,  lloExpected)

        oTest = cTextureLayer(1, 1)
        oTest.mCreateBorder("a")
        self.mCheck(oTest.llo, [["a"]])

    def mTest_cTextureLayer_mDecreaseSpace(self):
        oTest = cTextureLayer(3, 3)
        oTest.llo[1][1] = "b"
        oTest.mDecreaseSpace("a")
        self.mCheck(oTest.llo, [["a", "a", "a"], ["a", "b", "a"],
                                ["a", "a", "a"]])
        pass  # this method is not fully tested

    def mTest_cTextureLayer_mCreateTerrain(self):
        oTest = cTextureLayer(3, 3)
        oTest.mCreateTerrain({"a": 1})
        self.mCheck(oTest.llo, [["a", "a", "a"], ["a", "a", "a"],
                                ["a", "a", "a"]])
        pass  # this method is not fully tested


oTests = cUnittests(bQuiet=True)
assert(oTests())

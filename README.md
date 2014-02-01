#My Cli Engine

##What you can do with it:
Create simple worlds with bots moving about and interacting with each other.

##Map.py
A module that contains two classes (plus a unittest class)
###cLayer class
A container class that represents a two dimensional list.
###cTexture layer class
A subclass of cLayer which provides methods for terrain and lines.

##Bot.py
A module that contains three classes
###cChar class
A class that will declare itself a character, allow itself to be called and append itself to a given list.
###cBot class
A subclass of the cChar class, this class will place itself into a given layer object, and allow movement within it.
###cLivingBot class
A subclass of the cBot class, this class will add iMoves, sDirection and iHealth.

##Game.py

##cGame class
"Creates a world with several layers and bots to inhabit it."

##main.py
Creates some games and run them, for testing purposes and demonstration.

##Unittesting.py
Holds a class which supports unittesting and mocking of modules.
This class should be subclassed and your tests put in methods.
These methods should have names starting with mTest_ so they get automatically
run when the object is run.
# Semantic-Parsing-of-picture-descriptions
This project is part of the Softwareproject "Language, Action and Perception".

General research question:  Can we implement a model that learns a natural language from scratch through interaction?

Focused research question:  Can we teach a computer a mapping from natural language picture descriptions to a logical representation?

# SHAPELURN: An Interactive Language Learning Game

## Demo of the Prototype

To play the Prototype of our language learning game you only have to clone the repository and run the gui_simple.py script. 
You will be asked to enter a name for your session and the programm will then create a new folder with your chosen name in the source code directory. 
In this folder the result data from your game  will be stored. (If your are testing the game for us in order to collect data for our evaluation of the system, this folder contains all the data we need from you.)

**Requirements**<br>
Python 3 <br>
tkinter <br>
PIL <br>
PySimpleGUI <br>

## (Draft for) Instructions 

Welcome to SHAPELURN!<br>
In this interactive language learning game, you will teach the computer a language of your choice (see below for restrictions for the current Prototype version).
You will see pictures displaying simple geometric forms of different colours and shapes. Your task is to describe a part of the picture and the computer has to guess which of the objects of the picture you describe. However, at the beginning the computer doesn't know any words of your language (or any language at all). Therefore, you have to teach it your language by providing feedback such that the computer can learn from you. <br>
Your goal for this game is that the computer becomes better and better in guessing the correct answer during the progress of the game. 

For the detailed instructions please refer to the [Wiki](https://github.com/itsLuisa/Semantic-Parsing-of-picture-descriptions/wiki)


## Files 
* folder marked_pictures: pictures with guessed blocks for the test sentences
* folder pictures: example pictures as created by PictureLevel.py

* BlockPictureGenerator.py: automatically creates and saves the pictures 
* CalculCoordinates.py: used to calculate the coordinates for the picture generation in BlockPictureGenerator.py
* PictureLevel.py: generates a picture for a specified level by calling BlockPictureGenerator.py with corresponding parameters
* grammar.py:
* gui_simple: working GUI
* learning.py: the Stochastic Gradient Descent learn algorithm
* semdata.py: training and test sentences

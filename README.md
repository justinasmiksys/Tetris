DEMO: https://www.youtube.com/watch?v=Rzyx9OdU6yc

simple tetris game with small user interface

CONTENTS:

- checkbox.py: chckbox class which is used by the menu.py in order to (de)select options (backrgound color and available shapes) in the menu window

- game.py: game object which carries all of the game data and runs the game loop and is responsible for general game settings

- gameplay.py: gameplay object, which is responsible for the gameplay of tetris after clicking "play".
it draws/updates the game and is responsible for the controlls as well as in-game logic.

- menu.py: this file contains all of the menu views: Main, Start, Options, Rankings, GameOver, Exit.

- ranks.py: object which establishes the connection to the database file rankings.db (has to be created by the user) and
gets the data from the database to be displayed in the highscores section and writes new highscores into the database

- text_input.py: input box class, which is used by the game.py in order to type the name after the game and save it in the highscores

- main.py: main file, which imports the game object and runs the game loop


REQUIRED LIBRARIES:

- pygame
- random
- copy
- sqlite3
- os

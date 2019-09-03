# Scrabble-AI

This is my Scrabble AI project I'm doing for fun. 

To play against the bot, run game_gui.py on your system.

How to play:

Click on a tile and then click on a space on the board to place it. 

Click play to play the word, or swap to exchange all tiles currently on tbe board

Clear returns all tiles to hand

Cheat shows what the AI would do, but does not force you to make that play. 


The goal I have is to create a bruteforce bot which just picks the highest-scoring word every turn, then to create another agent which can beat that.

To see two greedy bots play against each other, with ASCII graphics, run greedymirror.py

Blank spaces aren't implemented, and also the bots can only makes horizontal moves atm. Working on fixing that. Also, the bots get stuck in some circumstances.

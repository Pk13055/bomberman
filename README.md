# Python Terminal Bomberman

## Introduction

This game has been written using _almost_ Vanilla Python. It uses the `numpy` library to keep track of the grid.
Dependencies are only numpy. Important to note that the game has been tested on **ONLY** Linux-based OSs, and _may not_ work on Windows.

## Structure

The application demonstrates inheritance, encapsulation, polymorphism as well as overloading.
- Each "object" is a derived class of the `Object` class.
- Each player/enemy is a derived class of the `Person` class.
- The `board` has its own class and and captures all objects placed on it.

## Running the program

- First, install all the requirements:
	- `pip install -r requirements.txt`
- Now, simply replace the first line of `main.py` with the location of your python installation
	- `#!/usr/bin/env python`
- Running the program is easy
	- `./main.py`

## Controls

- Controls follow traditional classic titles (W,S,A,D)
- To drop a bomb press `b`
- To quit, press `q`

## File Structure

.
 * [__init__.py](./__init__.py)
 * [people.py](./people.py)
 * [config.py](./config.py)
 * [objects.py](./objects.py)
 * [board.py](./board.py)
 * [main.py](./main.py)
 * [requirements.txt](./requirements.txt)
 * [README.md](./README.md)
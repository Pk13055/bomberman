#!/home/pratik/anaconda3/bin/python3.6

import board
import people
import objects
from config import getch
import sys

def spawn_enemies()

def main():
	# make the board and player
	bd = board.Board(42, 84)
	player = people.Bomber(36, 22)
	
	try:
		level = int(input("Choose level [1/2/3] : "))
		if level not in [0, 1, 2, 3]:
			raise Exception
	except:
		level = 1
	
	enemies = [0, 2, 3, 4]
	bricks 	= [0, 5, 7, 9]

	spawn_enemies(enemies[level], bd)

if __name__ == '__main__':
	main()
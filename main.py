#!/home/pratik/anaconda3/bin/python3.6

import board
import people
import objects
import sys
from config import getch, get_input, QUIT
from sys import argv as rd

# this attaches the enemies at random locations
def spawn_enemies(no_enemies, board):
	pass

# this attaches the bricks at random locations
def spawn_bricks(no_bricks, board):
	pass

def main():
	try:
		height, width = tuple(map(int, rd[1:3]))
	except:
		height, width = (34, 76)

	# make the board and player
	bd = board.Board(height, width)
	player = people.Bomber(5, 3) # always spawns at top left
	# spawning the player on the board
	bd.spawn(player)

	try:
		level = int(input("Choose level [[1], 2, 3] :"))
		if level not in [0, 1, 2, 3]:
			raise Exception
	except:
		level = 1
	
	enemies = [0, 2, 3, 4]
	bricks 	= [0, 5, 7, 9]

	spawn_enemies(enemies[level], bd)
	spawn_bricks(bricks[level], bd)
	bd.render()

	p_input = None
	# main loop which renders the game
	
	while True:
		print("'q' to quit | 'b' to drop bomb | WASD control |", p_input)
		p_input = get_input(getch())
		
		# don't render new frame unless valid input
		if p_input is None:
			continue
		elif p_input == QUIT:
			break

		bd.process_input(p_input)

		# print(bd)
		bd.render()

if __name__ == '__main__':
	main()
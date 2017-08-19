#!/home/pratik/anaconda3/bin/python3.6

import board
import people
import objects
import random
import config
from sys import argv as rd


# this attaches the enemies at random locations
def spawn(typ, total, board):
	for _ in range(total):
		x, y = (1, 1)
		if typ == config._enemy:
			e = people.Enemy(x, y)
		elif typ == config._bricks:
			e = objects.Bricks(x, y)
		else:
			return False
		run_count = 0
		while True:
			print(run_count)
			new_x, new_y = random.choice(board.init_points)
			if e.update_location(board, new_x, new_y, True):
				break
			run_count += 1
		board.add_storage(e)

	return True

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
	
	print("Initializing enemies, bricks ...")
	if spawn(config._enemy, config.enemies[level], bd) and \
		spawn(config._bricks, config.enemies[level], bd):
		print("Object Spawn Error")

	bd.render()

	p_input = -1
	# main loop which renders the game
	
	while True:
		print("'q' to quit | 'b' to drop bomb | WASD control | %d" % p_input)
		p_input = config.get_input(config.getch())
		
		# don't render new frame unless valid input
		if p_input == -1:
			continue
		elif p_input == config.QUIT:
			break

		bd.process_input(p_input)

		# print(bd)
		bd.render()

if __name__ == '__main__':
	main()
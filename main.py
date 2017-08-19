#!/home/pratik/anaconda3/bin/python3.6

import config, board
import people, objects
import random
import sys, signal
from sys import argv as rd
from time import sleep

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


	try:
		level = int(input("Choose level [[1], 2, 3] :"))
		if level not in [0, 1, 2, 3]:
			raise Exception
	except:
		level = 1
	
	# make the board and player
	bd = board.Board(height, width, level)
	
	player = people.Bomber(5, 3, config.lives[level], \
		config.bombs[level]) # always spawns at top left
	# spawning the player on the board
	bd.spawn(player)

	print("Initializing enemies, bricks ...")
	if not (spawn(config._enemy, config.enemies[level], bd) and \
			spawn(config._bricks, config.bricks[level], bd)):
		print("Object Spawn Error")
		return False
	
	print("Objects spawned successfully", "Rendering board", sep = "\n")
	sleep(1)

	bd.render()

	p_input = -1
	# main loop which renders the game
	while True:
		print("'q' : quit | 'b' : drop bomb || Lives %d | Bombs %d | F%d " \
			% (player.lives, player.bombs, bd.frame_counter))
		
		if bd.is_over():
			print("Congratulations, all enemies killed!")
			break

		if not player.lives:
			print("0 LIVES LEFT!! GAME OVER!")
			break

		p_input = config.get_input(config.getch())

		if p_input == config.QUIT:
			break

		bd.process_input(player, p_input)
		bd.update_frame()
		bd.render()

	bd.clear_storage()

if __name__ == '__main__':
	main()
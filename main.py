#!/home/pratik/anaconda3/bin/python3.6

import random
from sys import argv as rd
from os import system
from time import sleep
import datetime
import config
import board
import people
import objects


def spawn(typ, total, board):
    '''# this attaches the enemies at random locations'''
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
    except BaseException:
        height, width = (34, 76)

    a = 'r'

    while a == 'r':

        try:
            level = int(input("Choose level [[1], 2, 3] :"))
            if level not in [0, 1, 2, 3]:
                raise Exception
        except BaseException:
            level = 1

        # make the board and player
        bd = board.Board(height, width, level)

        player = people.Bomber(
            5,
            3,
            config.lives[level],
            config.bombs[level])  # always spawns at top left
        # spawning the player on the board
        bd.spawn(player)

        print("Initializing enemies, bricks ...")
        if not (spawn(config._enemy, config.enemies[level], bd) and
                spawn(config._bricks, config.bricks[level], bd)):
            print("Object Spawn Error")
            return False

        print("Objects spawned successfully", "Rendering board", sep="\n")
        sleep(1)

        bd.render()

        is_clean = False
        p_input = -1
        # main loop which renders the game
        st_time = datetime.datetime.now()
        prev_round = datetime.datetime.now()
        while (datetime.datetime.now() - st_time) <= \
                datetime.timedelta(seconds=config.timelimit[level]):

            print(config.printcc("'q' : quit | 'b' : drop bomb || Lives ", 'Gray') +
                  config.printcc('%s' % (player.lives * '♥ '), 'Red') +
                  config.printcc('| Bombs ', 'Gray') +
                  config.printcc('%s' % (player.bombs * '💣 '), 'Dark Gray') +
                  config.printcc("| T : %d " % (config.timelimit[level] - (datetime.datetime.now() -
                                                                           st_time).seconds), 'Gray'))

            try:
                bd.is_over(player)
            except Exception as exc:
                print(config.printcc(exc.args[0], 'Gray'))
                is_clean = True
                break

            p_input = config.get_key(config.get_input())

            if p_input == config.QUIT:
                break

            cur_round = datetime.datetime.now()
            bd.process_input(player, p_input)
            if (cur_round - prev_round) >= datetime.timedelta(seconds=1):
                bd.update_frame()
                prev_round = cur_round

            bd.render()

        if not is_clean:
            print(config.printcc("TIME UP!", 'Gray'))

        bd.clear_storage()
        for c, player in enumerate(bd.players):
            print(
                config.printcc(
                    "Player %d score : %d" %
                    (c, player.score), 'White'))

        sleep(3)
        print(
            config.printcc(
                "Press ANY KEY to exit | Press 'r' to restart",
                'Gray'))
        a = config._getch()
        system('reset')


if __name__ == '__main__':
    main()

'''
    Contains the board class along with the methods and other features
'''

import sys
import random
from os import system
from objects import Wall, Bomb
from config import x_fac, y_fac
import numpy as np
import config


class Board:

    '''# main board class that houses all board functions'''

    def __init__(self, m, n, level):
        '''# preferred size = (34, 76)'''

        assert isinstance(n, int) == True
        assert isinstance(m, int) == True

        self.width = n
        self.height = m
        self.dimen = (n, m)
        self._b = np.chararray((m, n))
        self._b[:, :] = config._empty
        self.frame_counter = 0
        self.init_points = []
        self.level = level

        self.init_board()

        # this stores all the bombs bricks and enemies that spawn
        self._storage = {
            config.types[config._bomb]: [],
            config.types[config._bricks]: [],
            config.types[config._enemy]: []
        }

        # this stores the player(s)
        self.players = []

    def init_board(self, reset=False):
        '''# initialize and setup the frame of the board'''
        if reset:
            self.frame_counter = 0
        # scaling the wall piece
        w = Wall(self.width / 20, self.height / 20)
        w_height, w_width = w.get_size()

        # creating the rows
        full_row, full_row[:, :] = \
            np.chararray((w_height, self.width)), config._wall
        emp_row, emp_row[:, :] = \
            np.chararray((w_height, self.width)), config._empty
        emp_row[:, :w_width] = emp_row[:, -w_width:] = w.structure

        alt_row, alt_row[:, :] = \
            np.chararray((w_height, self.width)), config._empty
        for c in range(1, int(self.width / w_width) + 1):
            if c % 2:
                alt_row[:, (c - 1) * w_width: (c * w_width)] = w.structure

        # assigning top and bottom
        self._b[:w_height, :] = self._b[-w_height:, :] = full_row
        # assigning other rows
        for r in range(2, int(self.height / w_height)):
            # alt row
            if r % 2:
                cur_row = alt_row
            else:
                cur_row = emp_row

            self._b[(r - 1) * w_height: (r * w_height), :] = cur_row

        # create the inital points for spawning objects
        # subtracting two edge blocks for each top bottom
        # and dividing by two for range of motion
        fp = (5, 3)
        # each object is 4 px wide
        total_block_x = int((self.width / config.x_fac - 2) / 2 + 1)
        # each object is 2px tall
        total_block_y = int((self.height / config.y_fac - 2) / 2 + 1)
        for r in range(total_block_x):
            for c in range(total_block_y):
                self.init_points.append((fp[0] + r * (2 * config.x_fac),
                                         fp[-1] + c * (2 * config.y_fac)))
        self.init_points = list(set(self.init_points))

    def reset_board(self):
        '''# reset the borad at the end of a life'''
        reset = True
        self.init_board(reset)
        self.clear_storage()

    def update_frame(self):
        '''# main function to check updates at every frame'''

        # clean up debris of the previous bombs
        for bomb in self._storage[config.types[config._bomb]]:
            if not bomb.active:
                bomb.structure[:, :] = config._empty
                x, y = bomb.get_coords()
                height, width = bomb.get_size()

                # removing the bomb as well
                bomb.blast_radius.insert(0, bomb.get_coords())

                for x_i, y_i in bomb.blast_radius:
                    self._b[y_i - 1: y_i - 1 + height, x_i -
                            1: x_i - 1 + width] = config._empty

                self._storage[config.types[config._bomb]].remove(bomb)

        # check if any bomb needs to detonate
        for bomb in self._storage[config.types[config._bomb]]:
            if (not bomb.timer) and bomb.active:

                bomb.structure[:, :] = config._expl
                x, y = bomb.get_coords()
                height, width = bomb.get_size()

                for x_i, y_i in bomb.blast_radius:
                    # if a wall blocks the way remove the blast coords
                    try:
                        if np.any(self._b[y_i -
                                          1: y_i -
                                          1 +
                                          height, x_i -
                                          1: x_i -
                                          1 +
                                          width] == Wall(0, 0).structure):
                            raise IndexError
                    except BaseException:
                        if x - x_i == 1 * x_fac:
                            bomb.blast_radius.remove((x + 2 * x_fac, y))
                        elif x - x_i == -1 * x_fac:
                            bomb.blast_radius.remove((x - 2 * x_fac, y))
                        elif y - y_i == 1 * y_fac:
                            bomb.blast_radius.remove((x, y - 2 * y_fac))
                        elif y - y_i == -1 * y_fac:
                            bomb.blast_radius.remove((x, y + 2 * y_fac))

                        bomb.blast_radius.remove((x_i, y_i))
                        continue

                    # kill all enemies in trajectory
                    for en in self._storage[config.types[config._enemy]]:
                        if en.get_coords() == (x_i, y_i) and en.is_killable:
                            self.clear_storage(en)
                            bomb.owner.score += config.scores[config._enemy]
                    # kill all players in trajectory
                    for pl in self.players:
                        if pl.get_coords() == (x_i, y_i) and pl.is_killable:
                            pl.lives = 0
                    # destory all bricks in trajectory
                    for brick in self._storage[config.types[config._bricks]]:
                        if brick.get_coords() == (x_i, y_i):
                            self.clear_storage(brick)
                            bomb.owner.score += config.scores[config._bricks]
                    # detonate other bombs by chain
                    for bmb in self._storage[config.types[config._bomb]]:
                        if bmb.active and bmb != bomb and bmb.get_coords() in bomb.blast_radius:
                            bmb.timer = 0

                # rendering the "explosion"
                for x_i, y_i in bomb.blast_radius:
                    self._b[y_i - 1: y_i - 1 + height, x_i -
                            1: x_i - 1 + width] = config._expl

                bomb.active = False

        # countdown everybomb
        for bomb in self._storage[config.types[config._bomb]]:
            bomb.countdown()
            self.refresh_obj(bomb)

        # move the enemies randomly
        for _ in self._storage[config.types[config._enemy]]:
            _dir = random.choice(config.DIR)
            self.process_input(_, _dir)

        self.frame_counter += 1

    def add_storage(self, obj):
        '''# add to storage'''
        try:
            if obj not in self._storage[obj.get_type()]:
                self._storage[obj.get_type()].append(obj)
                return True
            else:
                return None
        except KeyError:
            return False

    def clear_storage(self, obj=None):
        '''# clear the objects on the board at every instance'''
        if obj is None:
            for object_type in self._storage:
                for object_ in self._storage[object_type]:
                    del object_
                self._storage[object_type] = []
            return True
        else:
            typ = obj.get_type()
            try:
                self._storage[typ].remove(obj)
                return True
            except BaseException:
                return False

    def path_check(self, obj):
        '''# check if new binding space is occupied else if occupied'''

        height, width = obj.get_size()
        x_pos, y_pos = obj.get_coords()

        emp_comp = np.chararray(obj.get_size())
        emp_comp[:, :] = config._empty

        # bomb can overwrite enemies
        if obj.get_type() == config.types[config._bomb]:
            for enemy in self._storage[config.types[config._enemy]]:
                if enemy.get_coords() == obj.get_coords():
                    self.clear_storage(enemy)
            return True

        # enemies can walk into players and kill
        if obj.get_type() == config.types[config._enemy]:
            for player in self.players:
                if player.get_coords() == obj.get_coords():
                    player.lives -= 1
                    return True

        # players can walk into enemies
        elif obj in self.players:
            for enemy in self._storage[config.types[config._enemy]]:
                if obj.get_coords() == enemy.get_coords():
                    obj.lives -= 1
                    return True

        return np.all(self._b[y_pos - 1: y_pos - 1 + height, x_pos - 1:
                              x_pos - 1 + width] == emp_comp)

    def refresh_obj(self, obj):
        '''# refreshes the object on the board (meant to be used only with bombs)'''
        if obj.get_type() == config.types[config._bomb]:
            x, y = obj.get_coords()
            height, width = obj.get_size()
            self._b[y - 1: y - 1 + height,
                    x - 1: x - 1 + width] = obj.structure
            return True
        return False

    def draw_obj(self, obj):
        '''# draws the object on the board'''
        if self.path_check(obj):
            height, width = obj.get_size()
            x, y = obj.get_coords()
            self._b[y - 1: y - 1 + height,
                    x - 1: x - 1 + width] = obj.structure
            return True

        return False

    def clear_obj(self, obj):
        '''# clears the object from the board by an object'''
        if obj.get_type() != config.types[config._wall]:
            height, width = obj.get_size()
            x, y = obj.get_coords()

            # add exception for clearing the bomb
            if np.all(self._b[y - 1: y - 1 + height, x - 1: x - 1 + width] ==
                      Bomb(0, 0).structure):
                return True

            self._b[y - 1: y - 1 + height,
                    x - 1: x - 1 + width] = config._empty
            return True

        return False

    def attach_object(self, obj):
        '''# size being a (height, width) tuple'''
        if self.draw_obj(obj):
            self.add_storage(obj)
            return True
        return False

    def spawn(self, obj):
        '''# method to spawn the main player'''
        if obj.get_type() == config.types[config._bomb_man]:
            height, width = obj.get_size()
            x, y = obj.get_coords()
            x, y = x - 1, y - 1
            self._b[y: y + height, x: x + width] = obj.structure
            self.players.append(obj)
            return True
        else:
            print("Cannot spawn non-player object")
            return False

    def process_input(self, player, key_press):
        '''# to process the key press and take according action'''
        res = False
        if key_press in config.DIR:
            x, y = player.get_coords()

            # inverted up down calc because of top left origin
            if key_press == config.UP:
                y -= config.y_fac
            elif key_press == config.DOWN:
                y += config.y_fac
            elif key_press == config.LEFT:
                x -= config.x_fac
            elif key_press == config.RIGHT:
                x += config.x_fac

            res = player.update_location(self, x, y)

        # place the bomb at the given location
        elif player in self.players and key_press == config.BOMB:
            x, y = player.get_coords()
            if player.bombs:
                bomb = Bomb(x, y)
                bomb.owner = player
                self.attach_object(bomb)
                bomb.detonate(random.choice(config.timers[self.level]))
                player.bombs -= 1
            return True

        return res

    def is_over(self, player):
        '''# check to see if all the enemies have been killed'''
        if self.level:
            if len(self._storage[config.types[config._enemy]]) == 0:
                raise Exception("Congratulations, all enemies killed!")
            elif player.bombs == 0 and \
                    len(self._storage[config.types[config._bomb]]) == 0:
                raise Exception("It's a tie!")
            elif player.lives == 0:
                raise Exception("No lives left! GAME OVER!")
        return True

    def render(self):
        '''# displaying the board at every frame'''
        sys.stdout.flush()
        # print("\x1b[{};{}H".format(0,0))
        try:
            system('clear')
        except BaseException:
            system('cls')

        temp_board = np.matrix(self._b)
        for row in range(self.height):
            for col in range(self.width):
                try:
                    sys.stdout.write(config.
                                     getcc(temp_board[row, col].decode()))
                except BaseException:
                    sys.stdout.write(config.
                                     getcc(temp_board[row, col]))
            sys.stdout.write("\n")
        del temp_board

    def __repr__(self):
        '''# printing the board for debugging purposes'''
        temp_board = np.matrix(self._b)
        for row in range(self.height):
            for col in range(self.width):
                try:
                    print(temp_board[row, col].decode(), end="")
                except BaseException:
                    print(temp_board[row, col], end="")
            print()
        del temp_board
        return ""

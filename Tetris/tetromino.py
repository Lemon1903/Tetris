import random, time
import numpy as np
import pygame as pg
from settings import *


class Tetromino:
    def __init__(self, grid, first_drop=True):
        # main attributes
        self.x = 5
        self.y = 0
        self.ghost_y = 0
        self.grid = grid
        self.main_blocks = []
        self.ghost_blocks = []
        self.previous_blocks = []
        self.have_landed = False
        self.shape = random.choice(TETROMINOES)
        self.color = BLOCK_COLORS[TETROMINOES.index(self.shape)]
        
        # key input
        self.key = None
        self.key_delay = 0.1
        self.do_hard_drop = False

        # tetromino time attributes
        self.drop_delay = 0.3
        self.time_passed = 0
        self.first_drop = first_drop
        self.previous_time = time.perf_counter()

    def update_position(self, x, y, current_blocks):
        # store the previous positions of blocks
        self.previous_blocks = current_blocks.copy()

        # update the new position of the blocks
        current_blocks.clear()
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] == 1:    
                    row = y + i
                    col = x + j - len(self.shape[j])//2
                    current_blocks.append((row, col))

    def update_blocks(self):
        if self.do_hard_drop:
            self.hard_drop()
            HARDDROP_SOUND.play()

        # updates the blocks position first
        self.update_position(self.x, self.y, self.main_blocks)
        
        # check if the current position is inside and no overlapping cells
        if self.is_outside(self.main_blocks) or self.is_not_empty(self.main_blocks):
            # revert blocks position to its previous position
            self.revert_blocks(self.main_blocks)

            # check for game over status
            if self.y <= 0 and (self.key in ["down", "space"] or self.move_down):
                pg.event.post(pg.event.Event(GAMEOVER))
        else:
            # for the appropriate sound effects
            if self.key in ["down", "left", "right"]:
                MOVE_SOUND.play()
            elif self.key == "up":
                ROTATE_SOUND.play()

    def update_ghost_blocks(self):
        self.ghost_y = self.y
        while True:
            self.update_position(self.x, self.ghost_y, self.ghost_blocks)
            if self.is_outside(self.ghost_blocks) or self.is_not_empty(self.ghost_blocks):
                self.ghost_y -= 1
                self.revert_blocks(self.ghost_blocks)
                break
            self.ghost_y += 1

    def hard_drop(self):
        self.y = self.ghost_y
        self.have_landed = True
        self.main_blocks = self.ghost_blocks

    def soft_drop(self):
        # drop after (x) seconds
        self.move_down = False
        current_time = time.perf_counter()
        if current_time - self.previous_time >= self.drop_delay:
            # there's an issue about dropping the first
            # and second tetromino and this fixed it
            if self.first_drop:
                self.first_drop = False
            else:
                self.y += 1
                self.move_down = True
            self.previous_time = current_time

    def check_input(self, delta_time):
        keys = pg.key.get_pressed()
        self.time_passed += delta_time

        if self.key == "space":  # hard drop
            self.do_hard_drop = True
        elif self.key == "up":   # rotation
            self.shape = np.rot90(self.shape, 3)
        elif keys[pg.K_DOWN] and self.time_passed >= self.key_delay:    # drop faster
            self.y += 1
            self.key = "down"
            self.time_passed = 0
        elif keys[pg.K_LEFT] and self.time_passed >= self.key_delay:   # move left
            self.x -= 1
            self.key = "left"
            self.time_passed = 0
        elif keys[pg.K_RIGHT] and self.time_passed >= self.key_delay:  # move right
            self.x += 1
            self.key = "right"
            self.time_passed = 0

    def is_outside(self, current_blocks):
        for block in current_blocks:
            row, col = block[0], block[1]
            if col < 0 or col >= COLUMNS or row >= ROWS or row < 0:
                return True
        return False

    def is_not_empty(self, current_blocks):
        for block in current_blocks:
            row, col = block[0], block[1]
            if self.grid[row][col] is not None:
                return True
        return False

    def revert_blocks(self, current_blocks):
        if current_blocks == self.main_blocks:
            if self.key == "left":
                self.x += 1
                MOVE_FAIL_SOUND.play()
            elif self.key == "right":
                self.x -= 1
                MOVE_FAIL_SOUND.play()
            elif self.key == "up":  # -90 degrees
                self.shape = np.rot90(self.shape)
                ROTATE_FAIL_SOUND.play()
            elif self.key in ["down", "space"] or self.move_down:
                self.y -= 1
                self.have_landed = True
        current_blocks[:] = self.previous_blocks

    def reset(self):
        self.x = 5
        self.y = 0
        self.ghost_y = 0
        self.main_blocks = []
        self.ghost_blocks = []
        self.previous_blocks = []
        self.shape = TETROMINOES[BLOCK_COLORS.index(self.color)]
    
    def update(self, delta_time):
        self.soft_drop()
        self.check_input(delta_time)
        self.update_ghost_blocks()
        self.update_blocks()
        self.key = None
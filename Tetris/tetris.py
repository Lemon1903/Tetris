import pygame as pg
from settings import *
from tetromino import Tetromino
from ui_manager import UIManager
from game_manager import GameManager


class Tetris:
    def __init__(self):
        # display surfaces
        self.grid_surf = UIManager.get_instance().surfaces["grid"]
        self.hold_surf = UIManager.get_instance().surfaces["hold"]
        self.next_surf = UIManager.get_instance().surfaces["next"]
        self.next3_surf = UIManager.get_instance().surfaces["next3"]

        # tetris matrix
        self.grid = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]

        # tetromino
        self.hold_key = 0
        self.on_hold_tetromino = None
        self.current_tetromino = Tetromino(self.grid, False)
        self.next_tetromino = Tetromino(self.grid)
        self.next_tetrominoes = [Tetromino(self.grid) for _ in range(3)]
        self.score_system = {1: 40, 2: 100, 3: 300, 4: 1200}

    def spawn_tetromino(self):
        return Tetromino(self.grid)

    def draw_on_hold_tetromino(self):
        self.hold_surf.fill(DARK_GRAY)
        if self.on_hold_tetromino and GameManager.get_instance().state in ["game", "pause", "gameover"]:
            # displaying hold tetromino in hold surface
            tetromino_img = pg.image.load(f"assets/tetrominoes/{self.on_hold_tetromino.color}_tetromino.png").convert_alpha()
            self.hold_surf.blit(tetromino_img, (0, 0))
                
    def draw_next_tetromino(self):
        # displaying next tetromino in next surface
        self.next_surf.fill(DARK_GRAY)
        if self.next_tetromino and GameManager.get_instance().state in ["game", "pause", "gameover"]:
            tetromino_img = pg.image.load(f"assets/tetrominoes/{self.next_tetromino.color}_tetromino.png").convert_alpha()
            self.next_surf.blit(tetromino_img, (0, 0))

    def draw_next_tetrominoes(self):
        # displaying the next tetrominoes in next3 surface
        for i in range(3):
            self.next3_surf[i].fill(DARK_GRAY)
            if self.next_tetrominoes[i] and GameManager.get_instance().state in ["game", "pause", "gameover"]:
                tetromino_img = pg.image.load(f"assets/tetrominoes/{self.next_tetrominoes[i].color}_tetromino.png").convert_alpha()
                self.next3_surf[i].blit(tetromino_img, (0, 0))

    def draw_blocks(self):
        self.grid_surf.fill(BLACK)
        for i, row in enumerate(self.grid[1:]):
            for j, col in enumerate(row):
                x, y = j * BLOCKSIZE, i * BLOCKSIZE
                if col is not None:
                    if col == "ghost":
                        block = TETROMINO_BLOCKS["ghost"]
                    else:
                        block = TETROMINO_BLOCKS[col]
                else:
                    if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0):
                        block = TETROMINO_BLOCKS["dark"]
                    else:
                        block = TETROMINO_BLOCKS["light"]

                self.grid_surf.blit(block, (x,y))

    def update_cells(self, color, ghost_color):
        for b_pos, g_pos in zip(self.current_tetromino.main_blocks, self.current_tetromino.ghost_blocks):
            b_row, b_col = b_pos[0], b_pos[1]
            g_row, g_col = g_pos[0], g_pos[1]
            self.grid[g_row][g_col] = ghost_color
            self.grid[b_row][b_col] = color

    def check_rows(self):
        lines = 0
        have_played = False

        for row_ind, row in enumerate(self.grid):
            if None not in row:
                lines += 1
                self.move_down(row_ind)
                if not have_played:
                    CLEARLINE_SOUND.play()
                    have_played = True
        
        GameManager.get_instance().lines += lines
        GameManager.get_instance().score += self.score_system.get(lines, 0)
        GameManager.get_instance().best = max(GameManager.get_instance().score, GameManager.get_instance().best)

    def move_down(self, row):
        for i in range(row, 0, -1):
            self.grid[i] = self.grid[i-1]
        self.grid[0] = [None] * COLUMNS

    def hold_tetromino(self):
        # update tetromino
        self.update_cells(None, None)
        self.current_tetromino.reset()

        if self.on_hold_tetromino:
            temp = self.current_tetromino
            self.current_tetromino = self.on_hold_tetromino
            self.on_hold_tetromino = temp
        else:
            self.on_hold_tetromino = self.current_tetromino
            self.current_tetromino = self.next_tetromino
            self.next_tetromino = self.next_tetrominoes.pop(0)
            self.next_tetrominoes.append(self.spawn_tetromino())

    def update(self, delta_time):
        # drawing the game elements
        self.draw_blocks()
        self.draw_on_hold_tetromino()
        self.draw_next_tetromino()
        self.draw_next_tetrominoes()
        
        # state handling
        if GameManager.get_instance().state == "gameover":
            UIManager.get_instance().draw_game_over()
        
        elif GameManager.get_instance().state == "game":
            UIManager.get_instance().reset_game_over_elements()
            if self.hold_key == 1:
                self.hold_key = -1 
                self.hold_tetromino()
                HOLD_SOUND.play()
            if self.current_tetromino.have_landed:
                self.check_rows()
                self.hold_key = 0
                self.current_tetromino = self.next_tetromino
                self.next_tetromino = self.next_tetrominoes.pop(0)
                self.next_tetrominoes.append(self.spawn_tetromino())
            else:
                self.update_cells(None, None)  # clears previous cells
                self.current_tetromino.update(delta_time)
                self.update_cells(self.current_tetromino.color, "ghost")  # update new cells
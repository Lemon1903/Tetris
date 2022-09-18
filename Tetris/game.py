import sys, pygame as pg
from tetris import Tetris
from settings import *
from ui_manager import UIManager
from game_manager import GameManager


class Game:
    def __init__(self):
        # blitting surfaces
        self.display_surf = pg.display.get_surface()
        self.grid_surf = pg.Surface((GRID_W, GRID_H))
        self.hold_surf = pg.Surface((MA_FRAME_W, MA_FRAME_W))
        self.next_surf = pg.Surface((MA_FRAME_W, MA_FRAME_W))
        self.next3_surf = [pg.Surface((MA_FRAME_W, MA_FRAME_H)) for _ in range(3)]
        self.background = pg.transform.scale(pg.image.load("assets/others/background1.jpg"), (SCREEN_W, SCREEN_H)).convert()
        
        # game setup
        self.ui_manager = UIManager(self.grid_surf, self.hold_surf, self.next_surf, self.next3_surf)
        self.tetris = Tetris()
        self.delta_time = 0
        self.clock = pg.time.Clock()

    def draw_window(self):
        self.display_surf.blit(self.background, (0, 0))
        self.ui_manager.draw()
        self.tetris.update(self.delta_time)
        pg.display.update()

    def run(self):
        while True:
            self.delta_time = self.clock.tick(60)/1000

            # event handling
            for event in pg.event.get():
                # exit game
                if event.type in [pg.QUIT, EXIT_GAME]:
                    pg.quit()
                    sys.exit()
                # game over animation is done
                if event.type == GAMEOVER_DONE:
                    pg.time.delay(3000)
                    self.tetris = Tetris()
                    GameManager.get_instance().score = 0
                    GameManager.get_instance().lines = 0
                    GameManager.get_instance().state = "menu"
                # start button pressed
                if event.type == START_GAME:
                    GameManager.get_instance().state = "game"
                    pg.mixer.music.play(-1)
                # pause button pressed
                if event.type == PAUSE_GAME:
                    GameManager.get_instance().state = "pause"
                    pg.mixer.music.pause()
                # resume button pressed
                if event.type == RESUME_GAME:
                    GameManager.get_instance().state = "game"
                    pg.mixer.music.unpause()
                # help button pressed
                if event.type == HELP:
                    GameManager.get_instance().show_help = True
                # close button pressed
                if event.type == CLOSE:
                    GameManager.get_instance().show_help = False
                # game over state
                if event.type == GAMEOVER:
                    GameManager.get_instance().state = "gameover"
                    pg.mixer.music.stop()
                    GAMEOVER_SOUND.play()
                # input key for tetromino movement
                if event.type == pg.KEYDOWN:
                    if GameManager.get_instance().state == "game":
                        # for tetromino hold
                        if event.key == pg.K_c:
                            if not self.tetris.hold_key:
                                self.tetris.hold_key = 1
                            else:
                                HOLD_FAIL_SOUND.play()

                        # for tetromino movement
                        if event.key == pg.K_SPACE:
                            self.tetris.current_tetromino.key = "space"
                        elif event.key == pg.K_UP:
                            self.tetris.current_tetromino.key = "up"

            self.draw_window()


if __name__ == "__main__":
    pg.init()
    pg.display.set_caption("Tetris")
    game = Game()
    game.run()
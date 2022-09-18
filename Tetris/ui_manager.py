import pygame as pg
from game_manager import GameManager
from settings import *


class UIManager:
    __instance = None

    @staticmethod
    def get_instance():
        return UIManager.__instance

    def __init__(self, grid_surf, hold_surf, next_surf, next3_surf):
        # exception handling
        self.check_instance()

        # blitting surfaces
        self.display_surf = pg.display.get_surface()
        self.tetris_word = pg.transform.scale(pg.image.load("assets/others/tetris_word.png"), (240, 64)).convert()
        self.surfaces = {
            "grid": grid_surf,
            "hold": hold_surf,
            "next": next_surf,
            "next3": next3_surf
        }

        # blitting background surfaces
        self.blit_bg = {
            "grid": pg.image.load("assets/others/border.png").convert_alpha(),
            "frame": pg.image.load("assets/others/frame.png").convert_alpha(),
            "hold": pg.image.load("assets/others/frame_bg.png").convert_alpha(),
            "next": pg.image.load("assets/others/frame_bg2.png").convert_alpha(),
            "text": pg.image.load("assets/others/text_bg.png").convert_alpha()
        }

        # text image surfaces
        self.texts = {
            "hold": pg.image.load("assets/others/hold.png").convert_alpha(),
            "next": pg.image.load("assets/others/next.png").convert_alpha(),
            "best": pg.image.load("assets/others/best.png").convert_alpha(),
            "score": pg.image.load("assets/others/score.png").convert_alpha(),
            "lines": pg.image.load("assets/others/lines.png").convert_alpha(),
            "level": pg.image.load("assets/others/level.png").convert_alpha(),
            "gameover": pg.image.load("assets/others/gameover.png").convert_alpha()
        }

        # text image background surfaces
        self.text_bg = {
            "best": pg.image.load("assets/others/text_bg.png").convert_alpha(),
            "score": pg.image.load("assets/others/text_bg.png").convert_alpha(),
            "lines": pg.image.load("assets/others/text_bg.png").convert_alpha(),
            "level": pg.image.load("assets/others/text_bg.png").convert_alpha()
        }

        # game over attributes
        self.dynamic_text_surf = self.texts["gameover"]
        self.transparent_surf = self.surfaces["grid"].convert_alpha()
        self.orig_pos = (
            self.display_surf.get_width()/2, 
            self.display_surf.get_height()/2 - self.texts["gameover"].get_height()/2)
        self.target_size = self.texts["gameover"].get_size()
        self.enlarge_size = (self.target_size[0] + 34, self.target_size[1] + 4)
        self.reset_game_over_elements()

        # help ui 
        self.help_ui = pg.image.load("assets/others/help_ui.png").convert_alpha()
        self.help_ui_rect = self.help_ui.get_rect(center=(SCREEN_W/2, SCREEN_H/2))

        # buttons
        start_button = Button("start", (SCREEN_W/2, SCREEN_H/2 - 80), "assets/others/green_button.png")
        help_button = Button("help", (SCREEN_W/2, SCREEN_H/2), "assets/others/blue_button.png")
        quit_button = Button("quit", (SCREEN_W/2, SCREEN_H/2 + 80), "assets/others/red_button.png")
        pause_button = Button("pause", (SCREEN_W - 110, SCREEN_H - 130), "assets/others/pause.png")
        resume_button = Button("resume", (SCREEN_W/2, SCREEN_H/2 - 80), "assets/others/green_button.png")
        close_button = Button("close", (self.help_ui_rect.right - 95, 117), "assets/others/close_button.png")
        self.main_menu_buttons = ButtonGroup([start_button, help_button, quit_button])
        self.pause_menu_buttons = ButtonGroup([resume_button, help_button, quit_button])
        self.game_buttons = ButtonGroup([pause_button])
        self.help_buttons = ButtonGroup([close_button])

    def check_instance(self):
        if UIManager.__instance is not None:
            raise Exception("This is a singleton class. Cannot be instantiated.")
        else:
            UIManager.__instance = self

    def load_image(self):
        pass

    # ===== all state =====
    def draw_grid_elements(self):
        self.display_surf.blit(self.blit_bg["grid"], (
            SCREEN_W/2 - self.blit_bg["grid"].get_width()/2, SCREEN_H/2 - self.blit_bg["grid"].get_height()/2 + 15))
        self.display_surf.blit(self.surfaces["grid"], (SCREEN_W/2 - GRID_W/2, SCREEN_H/2 - GRID_H/2 + 15))

    def draw_hold_elements(self):
        self.display_surf.blit(self.blit_bg["hold"], (27, 107))
        self.display_surf.blit(self.surfaces["hold"], (47, 127))
        self.display_surf.blit(self.texts["hold"], (95 - self.texts["hold"].get_width()/2, 58))

    def draw_next_elements(self):
        # background behind all next elements
        self.display_surf.blit(self.blit_bg["next"], (537, 107))

        # background behind the next tetromino
        x = 537 + (self.blit_bg["next"].get_width()/2 - self.blit_bg["frame"].get_width()/2)
        self.display_surf.blit(self.blit_bg["frame"], (x, 120)) 
        self.display_surf.blit(self.surfaces["next"], (557, 127))
        self.display_surf.blit(self.texts["next"], (605 - self.texts["next"].get_width()/2, 58))
        
        # background behind the next 3 tetrominoes
        for i, surf in enumerate(self.surfaces["next3"]):
            y = 255 + i*5 + i*BG_FRAME_H
            self.display_surf.blit(self.blit_bg["frame"], (x, y))
            self.display_surf.blit(surf, (557, y + 5))

    def draw_text_elements(self):
        best = SCORE_FONT.render(str(GameManager.get_instance().best), 1, WHITE)
        self.display_surf.blit(self.texts["best"], (95 - self.texts["best"].get_width()/2, 278))
        self.display_surf.blit(self.text_bg["best"], (27, 328))
        self.display_surf.blit(best, (
            27 + self.text_bg["best"].get_width()/2 - best.get_width()/2, 
            328 + self.text_bg["best"].get_height()/2 - best.get_height()/2
        ))

        score = SCORE_FONT.render(str(GameManager.get_instance().score), 1, WHITE)
        self.display_surf.blit(self.texts["score"], (95 - self.texts["score"].get_width()/2, 378))
        self.display_surf.blit(self.text_bg["score"], (27, 428))
        self.display_surf.blit(score, (
            27 + self.text_bg["score"].get_width()/2 - score.get_width()/2, 
            428 + self.text_bg["score"].get_height()/2 - score.get_height()/2
        ))

        lines = SCORE_FONT.render(str(GameManager.get_instance().lines), 1,  WHITE)
        self.display_surf.blit(self.texts["lines"], (95 - self.texts["lines"].get_width()/2, 478))
        self.display_surf.blit(self.text_bg["lines"], (27, 528))
        self.display_surf.blit(lines, (
            27 + self.text_bg["lines"].get_width()/2 - lines.get_width()/2, 
            528 + self.text_bg["lines"].get_height()/2 - lines.get_height()/2
        ))

    # ===== game over state =====
    def draw_game_over(self):
        self.expand()
        self.transparent_surf.fill((0, 0, 0, 150))
        self.surfaces["grid"].blit(self.transparent_surf, (0, 0))
        self.display_surf.blit(self.dynamic_text_surf, self.dynamic_text_rect)

    def expand(self):
        if self.start_size[0] <= self.enlarge_size[0] and not self.is_enlarge:
            self.start_size[0] += 40
            self.start_size[1] += 5
        else:
            self.is_enlarge = True
            if self.start_size[0] >= self.target_size[0] and not self.is_done:
                self.start_size[0] -= 32
                self.start_size[1] -= 4
            else:
                self.is_done = True
                pygame.event.post(pygame.event.Event(GAMEOVER_DONE))
        
        self.dynamic_text_surf = pg.transform.scale(self.texts["gameover"], self.start_size)
        self.dynamic_text_rect = self.dynamic_text_surf.get_rect(topleft=(self.orig_pos[0] - self.start_size[0]/2, self.orig_pos[1]))

    def reset_game_over_elements(self):
        self.is_enlarge = False
        self.is_done = False
        self.start_size = [56, 31]

    # ===== main menu state =====
    def draw_main_menu(self):
        self.main_menu_buttons.draw()
        self.main_menu_buttons.update()

    # ===== game state =====
    def draw_game_buttons(self):
        self.game_buttons.draw()
        self.game_buttons.update()

    # ===== pause menu state =====
    def draw_pause_menu(self):
        self.pause_menu_buttons.draw()
        self.pause_menu_buttons.update()

    # ===== help state =====
    def draw_help_ui(self):
        self.display_surf.blit(self.help_ui, self.help_ui_rect)
        self.help_buttons.draw()
        self.help_buttons.update()

    # ===== drawing UI =====
    def draw(self):
        # elements drawn in all state
        self.draw_grid_elements()
        self.draw_hold_elements()
        self.draw_next_elements()
        self.draw_text_elements()
        self.display_surf.blit(self.tetris_word, (SCREEN_W/2 - self.tetris_word.get_width()/2, 15))

        # draw elements in specific state only
        if GameManager.get_instance().show_help:
            self.draw_help_ui()
        elif GameManager.get_instance().state == "menu":
            self.draw_main_menu()
        elif GameManager.get_instance().state == "game":
            self.draw_game_buttons()
        elif GameManager.get_instance().state == "pause":
            self.draw_pause_menu()


# ===== buttons classes =====
class ButtonGroup:
    def __init__(self, buttons):
        self.buttons = buttons

    def draw(self):
        for button in self.buttons:
            button.draw()

    def update(self):
        for button in self.buttons:
            button.update()

class Button:
    def __init__(self, button_type, pos, path):
        self.type = button_type
        self.display_surf = pg.display.get_surface()

        if button_type in ["start", "resume", "help", "quit"]:
            # button image surface
            self.image = pg.transform.scale(pg.image.load(path), (250, 64)).convert_alpha()
            self.rect = self.image.get_rect(topleft=(pos[0] - self.image.get_width()/2, pos[1] - self.image.get_height()/2))
            
            # text surface
            self.text_surf = MENU_FONT.render(button_type, 1, "white")
            self.text_rect = self.text_surf.get_rect(center=self.rect.center)
            
        if button_type in ["pause", "close"]:
            self.image = pg.image.load(path).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)

        # main attributes
        self.is_pressed = False
        self.is_played = False
        self.brightness = (0, 0, 0)

    def draw(self):
        self.dynamic_image = self.image.copy()
        self.dynamic_image.fill(self.brightness, None, pg.BLEND_RGB_ADD)
        self.display_surf.blit(self.dynamic_image, self.rect)

        if self.type not in ["pause", "close"]:
            self.display_surf.blit(self.text_surf, self.text_rect)

    def activate(self):
        if self.type == "start":
            pg.event.post(pg.event.Event(START_GAME))
        elif self.type == "help":
            pg.event.post(pg.event.Event(HELP))
        elif self.type == "pause":
            pg.event.post(pg.event.Event(PAUSE_GAME))
        elif self.type == "resume":
            pg.event.post(pg.event.Event(RESUME_GAME))
        elif self.type == "close":
            pg.event.post(pg.event.Event(CLOSE))
        else:
            pg.event.post(pg.event.Event(EXIT_GAME))

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.brightness = (15, 15, 15)
            if not self.is_played:
                self.is_played = True
                HOVER_SOUND.play()

            if pg.mouse.get_pressed()[0]:
                self.is_pressed = True
            elif self.is_pressed:
                self.activate()
                self.is_played = False
                self.is_pressed = False
                CONFIRM_SOUND.play()
        else:
            self.is_played = False
            self.is_pressed = False
            self.brightness = (0, 0, 0)
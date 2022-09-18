import pygame

# ===== game attributes ============================================================================================================#
pygame.init()
SCREEN_W, SCREEN_H = 700, 800
GRID_W, GRID_H = 320, 640
BG_FRAME_W, BG_FRAME_H = 110, 110
MA_FRAME_W, MA_FRAME_H = 96, 96
ROWS, COLUMNS = 21, 10
DISPLAY_SURFACE = pygame.display.set_mode((SCREEN_W, SCREEN_H))

# ===== colors =====================================================================================================================#
WHITE = (245, 245, 245)
BLACK = (0, 0, 0)
DARK_GRAY = (66, 65, 62)

# ===== user events ================================================================================================================#
GAMEOVER_DONE = pygame.USEREVENT + 1
START_GAME = pygame.USEREVENT + 2
EXIT_GAME = pygame.USEREVENT + 3
PAUSE_GAME = pygame.USEREVENT + 4
RESUME_GAME = pygame.USEREVENT + 5
HELP = pygame.USEREVENT + 6
CLOSE = pygame.USEREVENT + 7
GAMEOVER = pygame.USEREVENT + 8

# ===== fonts ======================================================================================================================#
MENU_FONT = pygame.font.Font("assets/font/tetris_font.ttf", 30)
SCORE_FONT = pygame.font.Font("assets/font/tetris_font.ttf", 20)

# ===== sounds =====================================================================================================================#
MOVE_SOUND = pygame.mixer.Sound("assets/sounds/move.wav")
MOVE_FAIL_SOUND = pygame.mixer.Sound("assets/sounds/movefail.wav")
HOLD_SOUND = pygame.mixer.Sound("assets/sounds/hold.wav")
HOLD_FAIL_SOUND = pygame.mixer.Sound("assets/sounds/holdfail.wav")
ROTATE_SOUND = pygame.mixer.Sound("assets/sounds/rotate.wav")
ROTATE_FAIL_SOUND = pygame.mixer.Sound("assets/sounds/rotfail.wav")
HARDDROP_SOUND = pygame.mixer.Sound("assets/sounds/harddrop.wav")
GAMEOVER_SOUND = pygame.mixer.Sound("assets/sounds/gameover.wav")
CONFIRM_SOUND = pygame.mixer.Sound("assets/sounds/menuconfirm.wav")
HOVER_SOUND = pygame.mixer.Sound("assets/sounds/menuhover.wav")
CLEARLINE_SOUND = pygame.mixer.Sound("assets/sounds/clearline.mp3")
pygame.mixer.music.load("assets/sounds/Tetris Friends - Ultra Music.mp3")

# ===== tetris attributes ==========================================================================================================#
BLOCKSIZE = 32
BLOCK_COLORS = ("cyan", "blue", "orange", "yellow", "red", "green", "purple")
TETROMINOES = [
    [   # I tetromino
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],

    [   # J tetromino
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
    ],

    [   # L tetromino
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0],
    ],

    [   # O tetromino
        [1, 1],
        [1, 1]
    ],

    [   # Z tetromino
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0],
    ],

    [   # S tetromino
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0],
    ],

    [   # T tetromino
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0]
    ]
]

# ===== tetromino blocks ===========================================================================================================#
TETROMINO_BLOCKS = {
    "cyan": pygame.transform.scale(pygame.image.load(f"assets/blocks/cyan_block.png"), (BLOCKSIZE, BLOCKSIZE)).convert(),
    "blue": pygame.transform.scale(pygame.image.load(f"assets/blocks/blue_block.png"), (BLOCKSIZE, BLOCKSIZE)).convert(),
    "orange": pygame.transform.scale(pygame.image.load(f"assets/blocks/orange_block.png"), (BLOCKSIZE, BLOCKSIZE)).convert(),
    "yellow": pygame.transform.scale(pygame.image.load(f"assets/blocks/yellow_block.png"), (BLOCKSIZE, BLOCKSIZE)).convert(),
    "red": pygame.transform.scale(pygame.image.load(f"assets/blocks/red_block.png"), (BLOCKSIZE, BLOCKSIZE)).convert(),
    "green": pygame.transform.scale(pygame.image.load(f"assets/blocks/green_block.png"), (BLOCKSIZE, BLOCKSIZE)).convert(),
    "purple": pygame.transform.scale(pygame.image.load(f"assets/blocks/purple_block.png"), (BLOCKSIZE, BLOCKSIZE)).convert(),
    "ghost": pygame.transform.scale(pygame.image.load(f"assets/blocks/ghost_block.png"), (BLOCKSIZE, BLOCKSIZE)).convert(),
    "light": pygame.transform.scale(pygame.image.load(f"assets/blocks/light_block.png"), (BLOCKSIZE, BLOCKSIZE)).convert(),
    "dark": pygame.transform.scale(pygame.image.load(f"assets/blocks/dark_block.png"), (BLOCKSIZE, BLOCKSIZE)).convert()
}

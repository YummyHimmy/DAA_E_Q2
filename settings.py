#settings.py
import os

GRID = 8
TILE_SIZE = 64
WIDTH = GRID * TILE_SIZE
HEIGHT = GRID * TILE_SIZE
TOTAL_TILES = GRID * GRID
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")  
TOP_BAR_HEIGHT = 40
SIDEBAR_WIDTH = 260
GAME_OFFSET_X = 0
GAME_OFFSET_Y = TOP_BAR_HEIGHT
MAX_STEPS = 6
GHOST_MAX_STEPS = 5
AVATAR_MOVE_DELAY = 650 #  ms
GHOST_STEP_DELAY = 120  #  ms

FLOOR = 0
WALL = 1
SEALED_FLOOR = 2
MANUSCRIPT = 3
WALL_SEALED = 4
MANUSCRIPT_SEALED = 5

PLAYER_PLANNING = 0
PLAYER_MOVING   = 1
GHOST_MOVING    = 2
GAME_OVER = 3
WIN_SCREEN = 4
turn_state = PLAYER_PLANNING

DIFFICULTY_SETTINGS = {
    "EASY": {
        "wall_ratio": (0.15, 0.20),     
        "sealed_ratio": 0.10,           
        "wall_chance": 0.5,             
        "spawn_dist": max(4, GRID // 2) 
    },
    "MEDIUM": {
        "wall_ratio": (0.25, 0.30),
        "sealed_ratio": 0.06,
        "wall_chance": 0.7,
        "spawn_dist": max(3, GRID // 3)
    },
    "HARD": {
        "wall_ratio": (0.35, 0.40),
        "sealed_ratio": 0.03,
        "wall_chance": 0.9,             
        "spawn_dist": max(3, GRID // 3)
    }
}

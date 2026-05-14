#game_state.py
import time
import map
from settings import *
from home_screen import HomeScreen

class GameState:
    def __init__(self):
        self.ghost_path = []
        self.ghost_step_index = 0
        self.ghost_last_move_time = 0
        
        self.current_difficulty = None
        
        self.grid = None
        self.player_pos = None
        self.ghost_pos = None        
        
        self.manuscripts_left = 0
        
        self.turn_state = PLAYER_PLANNING
        
        self.start_time = time.time()
        self.total_time = 0
        
        self.end_screen_start = None
        self.end_screen_delay = 2
        
        self.running = True
        
    def start_new_game(self, screen, movement):
        home_screen = HomeScreen(
            WIDTH + SIDEBAR_WIDTH,
            HEIGHT + TOP_BAR_HEIGHT
        )

        selected_difficulty = home_screen.run(screen)

        if not selected_difficulty:
            return False

        self.current_difficulty = selected_difficulty
        self.grid, self.player_pos, self.ghost_pos = map.generate_map(self.current_difficulty)

        self.manuscripts_left = sum(
            1
            for r in range(GRID)
            for c in range(GRID)
            if self.grid[r][c] in [MANUSCRIPT, MANUSCRIPT_SEALED]
        )

        self.turn_state = PLAYER_PLANNING
        self.running = True

        self.start_time = time.time()
        self.total_time = 0

        self.end_screen_start = None

        self.ghost_path = []
        self.ghost_step_index = 0
        self.ghost_last_move_time = 0

        movement.reset_path()
        movement.is_moving = False
        movement.animation = 0
        movement.direction = "DOWN"

        movement.pixel_x = self.player_pos[1] * TILE_SIZE
        movement.pixel_y = self.player_pos[0] * TILE_SIZE

        return True


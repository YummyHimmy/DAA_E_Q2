# movement.py
import pygame
from settings import *

class Controller:
    def __init__(self):
        self.path = []
        self.is_moving = False
        self.move_index = 0
        self.last_move_time = 0
        self.direction = "DOWN"
        self.animation = 0
        self.pixel_x = None
        self.pixel_y = None
        self.target_x = None
        self.target_y = None
        self.move_start_time = 0
        self.move_duration = AVATAR_MOVE_DELAY

    def is_adjacent(self, a, b):
        ar, ac = a
        br, bc = b
        return max(abs(ar - br), abs(ac - bc)) == 1  # diagonal allowed

    def is_walkable(self, grid, r, c):
        return grid[r][c] in [
            FLOOR, SEALED_FLOOR,
            MANUSCRIPT, MANUSCRIPT_SEALED
        ]

    def handle_mouse_click(self, pos, grid, player_pos):
        if self.is_moving: # block input when move
            return

        mx, my = pos # coordinate in pixel unit
        r = my // TILE_SIZE # coordinat in tile unit
        c = mx // TILE_SIZE

        if not (0 <= r < GRID and 0 <= c < GRID): # Prevent out of bond click
            return

        if not self.is_walkable(grid, r, c): # Prevent click on wall
            return

        if len(self.path) == 0:
            if self.is_adjacent(player_pos, (r, c)): # Dot must be adjacent to player
                self.path.append((r, c))
        else:
            if len(self.path) < MAX_STEPS and self.is_adjacent(self.path[-1], (r, c)): 
            # Dot must be adjacent to other dot
                self.path.append((r, c))

    def confirm_move(self):
        if self.path:
            self.is_moving = True
            self.move_index = 0
            self.last_move_time = pygame.time.get_ticks()

    def update(self, player_pos):
        if not self.is_moving:
            return player_pos

        now = pygame.time.get_ticks()
        
        if self.pixel_x is None:
            r, c = player_pos
            self.pixel_x = c * TILE_SIZE
            self.pixel_y = r * TILE_SIZE

        if self.is_moving:
            if self.target_x is None:
                nr, nc = self.path[self.move_index] 
                # Target coordinate for next step

                cr, cc = player_pos # Curr avatar coordinate
                dr = nr - cr
                dc = nc - cc

                if dr == -1 and dc == 0:
                    self.direction = "UP"
                elif dr == 1 and dc == 0:
                    self.direction = "DOWN"
                elif dr == 0 and dc == -1:
                    self.direction = "LEFT"
                elif dr == 0 and dc == 1:
                    self.direction = "RIGHT"
                elif dr == -1 and dc == -1:
                    self.direction = "UP_LEFT"
                elif dr == -1 and dc == 1:
                    self.direction = "UP_RIGHT"
                elif dr == 1 and dc == -1:
                    self.direction = "DOWN_LEFT"
                elif dr == 1 and dc == 1:
                    self.direction = "DOWN_RIGHT"

                # target pixel
                self.target_x = nc * TILE_SIZE
                self.target_y = nr * TILE_SIZE
                self.move_start_time = now

            # anims interpolation
            t = min((now - self.move_start_time) / self.move_duration, 1)
            self.pixel_x += (self.target_x - self.pixel_x) * t
            self.pixel_y += (self.target_y - self.pixel_y) * t

            if t >= 1: # Reset the traget pixel coordinate when arrive at each dot
                player_pos = self.path[self.move_index]
                self.move_index += 1 # Increment step taken
                self.target_x = None
                self.target_y = None

                if self.move_index >= len(self.path): # when avatar has reached last dot
                    self.path.clear()
                    self.is_moving = False
                    self.animation = 0
                    self.direction = "DOWN"
            
        return player_pos

    def reset_path(self):
        if not self.is_moving:
            self.path.clear()

    def draw_path(self, screen, offset_x=0, offset_y=0):    
        if self.is_moving: # Remove dot when moving
            return
        
        for r, c in self.path:
            pygame.draw.circle(
                screen, (228, 245, 245),
                (c * TILE_SIZE + TILE_SIZE // 2 + offset_x,
                r * TILE_SIZE + TILE_SIZE // 2 + offset_y)
                , 7 # radius
            )

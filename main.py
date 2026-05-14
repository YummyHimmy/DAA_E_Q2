#main.py
import pygame
import sys
import time

from settings import *
from movement import Controller
from game_state import GameState
from asset_load import load_all_assets
from renderer import draw, draw_game_over, draw_win_screen
from ghost_movements import find_path, is_player_in_kill_range

pygame.init()
screen = pygame.display.set_mode((
    WIDTH + SIDEBAR_WIDTH,
    HEIGHT + TOP_BAR_HEIGHT
))

state = GameState()
movement = Controller()
assets = load_all_assets()

pygame.display.set_caption("Quiz 2")
clock = pygame.time.Clock()

if not state.start_new_game(screen, movement):
    pygame.quit()
    sys.exit()

while state.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state.running = False
            
        if (event.type == pygame.MOUSEBUTTONDOWN 
        and event.button == 1 and state.turn_state == PLAYER_PLANNING):
            mx, my = pygame.mouse.get_pos()
            movement.handle_mouse_click(
                (mx, my - TOP_BAR_HEIGHT),
                state.grid,
                state.player_pos
            )

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and state.turn_state == PLAYER_PLANNING: 
                movement.confirm_move()
                if movement.path:
                    state.turn_state = PLAYER_MOVING
                    
            if event.key == pygame.K_z: # Reset path w/ 'z'
                movement.reset_path()
            
            if event.key == pygame.K_m:  # Backto menu dg 'm'
                state.start_new_game(screen, movement)

            if event.key == pygame.K_ESCAPE: # quit game 'ESC'
                state.running = False
                
    player_done = movement.is_moving
    state.player_pos = movement.update(state.player_pos)

    pr, pc = state.player_pos # pr = player row; pc = player column

    if state.grid[pr][pc] == MANUSCRIPT:
        state.grid[pr][pc] =FLOOR
        state.manuscripts_left -= 1

    elif state.grid[pr][pc] == MANUSCRIPT_SEALED:
        state.grid[pr][pc] = SEALED_FLOOR
        state.manuscripts_left -= 1

    if state.manuscripts_left <= 0 and state.turn_state not in (WIN_SCREEN, GAME_OVER):
        state.end_screen_start = time.time()
        state.total_time = time.time() - state.start_time
        state.turn_state = WIN_SCREEN

    if player_done and not movement.is_moving and state.turn_state != WIN_SCREEN:
        state.turn_state = GHOST_MOVING
        
        full_path = find_path(state.grid, state.ghost_pos, state.player_pos)
        if full_path:
            state.ghost_path = full_path[:GHOST_MAX_STEPS]
        else:
            state.ghost_path = []

        state.ghost_step_index = 0
        state.ghost_last_move_time = pygame.time.get_ticks()

    if state.turn_state == GHOST_MOVING:
        now = pygame.time.get_ticks()

        if state.ghost_step_index < len(state.ghost_path):
            if now - state.ghost_last_move_time >= GHOST_STEP_DELAY:
                next_pos = state.ghost_path[state.ghost_step_index]
                rr, cc = next_pos
                
                if state.grid[rr][cc] == SEALED_FLOOR:
                    state.ghost_path = []
                else:
                    state.ghost_pos = next_pos
                    state.ghost_step_index += 1
                    state.ghost_last_move_time = now

                if is_player_in_kill_range(
                    state.grid,
                    state.ghost_pos,
                    state.player_pos
                ):
                    if state.end_screen_start is None:
                        state.end_screen_start = time.time()

                    state.turn_state = GAME_OVER
    
        else:
            state.turn_state = PLAYER_PLANNING
            state.ghost_path = []
        
    screen.fill((0,0,0))
    draw(screen, movement, state, assets)
    movement.draw_path(screen, GAME_OFFSET_X, GAME_OFFSET_Y)

    if state.turn_state == GAME_OVER:
        draw_game_over(screen)
    elif state.turn_state == WIN_SCREEN:
        draw_win_screen(screen, state.total_time)

    pygame.display.flip()
    clock.tick(30)
    
    if (state.turn_state in (GAME_OVER, WIN_SCREEN) and state.end_screen_start is not None):
        if time.time() - state.end_screen_start >= state.end_screen_delay:
            if not state.start_new_game(screen, movement):
                state.running = False

pygame.quit()
sys.exit()

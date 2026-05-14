#main.py
import pygame
import sys
import time

from settings import *
from movement import Controller
from game_state import GameState
from asset_load import load_all_assets
from renderer import draw, draw_game_over, draw_win_screen

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
        #TODO: bikin path buat ghost

    if state.turn_state == GHOST_MOVING:
        #TODO: bikin pergerakan ghost
        state.turn_state = PLAYER_PLANNING
        
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

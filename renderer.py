#renderer.py
import pygame
import math
import time
from settings import *
from asset_load import *

def draw(screen, movement, state, assets):
    for r in range(GRID):
        for c in range(GRID):
            x = c * TILE_SIZE
            y = r * TILE_SIZE
            t = state.grid[r][c]
            
            if t == FLOOR:
                screen.blit(assets["floor_regular"], (x + GAME_OFFSET_X, y + GAME_OFFSET_Y))
            elif t == WALL:
                screen.blit(assets["wall_regular"], (x + GAME_OFFSET_X, y + GAME_OFFSET_Y))
            elif t == WALL_SEALED:
                screen.blit(assets["wall_sealed"], (x + GAME_OFFSET_X, y + GAME_OFFSET_Y))
            elif t == SEALED_FLOOR:
                screen.blit(assets["floor_sealed"], (x + GAME_OFFSET_X, y + GAME_OFFSET_Y))
            elif t == MANUSCRIPT:
                screen.blit(assets["floor_regular"], (x + GAME_OFFSET_X, y + GAME_OFFSET_Y))
                screen.blit(assets["manuscript_img"], (x + GAME_OFFSET_X, y + GAME_OFFSET_Y))
            elif t == MANUSCRIPT_SEALED:
                screen.blit(assets["floor_sealed"], (x + GAME_OFFSET_X, y + GAME_OFFSET_Y))
                screen.blit(assets["manuscript_img"], (x + GAME_OFFSET_X, y + GAME_OFFSET_Y))

    player_img = assets["player_sprites"].get(movement.direction, assets["player_sprites"]["DOWN"])
    y_offset = int(2 * math.sin(movement.animation)) if movement.is_moving else 0
    screen.blit(player_img, (
        int(movement.pixel_x) + GAME_OFFSET_X,
        int(movement.pixel_y) + GAME_OFFSET_Y + y_offset
    ))

    gr, gc = state.ghost_pos
    screen.blit(assets["ghost_img"], (
        gc * TILE_SIZE + GAME_OFFSET_X,
        gr * TILE_SIZE + GAME_OFFSET_Y
    ))

    bar_rect = pygame.Rect(0, 0, WIDTH + SIDEBAR_WIDTH, TOP_BAR_HEIGHT)
    pygame.draw.rect(screen, (20, 20, 20), bar_rect)

    font = pygame.font.SysFont("LucidaConsole", 18)

    left_text = f"Difficulty: {state.current_difficulty} | Manuscripts: {state.manuscripts_left}"
    screen.blit(font.render(left_text, True, (230, 230, 230)), (WIDTH - 145, 10))

    if state.turn_state == PLAYER_PLANNING:
        state_text = "Plan your moves carefully"
        state_color = (80, 200, 120)
    elif state.turn_state == PLAYER_MOVING:
        state_text = "Make it count"
        state_color = (200, 160, 80)
    elif state.turn_state == GAME_OVER:
        state_text = "GAME OVER"
        state_color = (200, 80, 80)

    else: #GHOST_MOVING
        dots = "." * ((pygame.time.get_ticks() // 500) % 4)
        state_text = "The soul pursue" + dots
        state_color = (200, 80, 80)

    screen.blit(font.render(state_text, True, state_color), (12, 10))

    sidebar_x = WIDTH
    sidebar_rect = pygame.Rect(sidebar_x, TOP_BAR_HEIGHT, SIDEBAR_WIDTH, HEIGHT)

    pygame.draw.rect(screen, (25, 25, 35), sidebar_rect)

    font_title = pygame.font.SysFont("LucidaConsole", 18, bold=True)
    font_text  = pygame.font.SysFont("LucidaConsole", 14)

    screen.blit(
        font_title.render("CONTROLS", True, (240, 220, 180)),
        (sidebar_x + 16, TOP_BAR_HEIGHT + 16)
    )

    controls = [
        "Click  : Place movement dot",
        "ENTER  : Confirm move",
        "Z      : Reset path",
        "ESC    : Quit game",
        "M      : Main Menu"
    ]

    y = TOP_BAR_HEIGHT + 52
    if state.start_time is not None:
        if state.turn_state in (WIN_SCREEN, GAME_OVER):
            timer = state.total_time
        else:
            timer = time.time() - state.start_time

        total_int = int(timer)
        minutes = total_int // 60
        seconds = total_int % 60
        timer_str = f"{minutes:02d}:{seconds:02d}"
        timer_font = pygame.font.SysFont("LucidaConsole", 33, bold=True)
        screen.blit(
            timer_font.render(f"Time: {timer_str}", True, (200, 200, 200)),
            (sidebar_x + 28, y + 410))

    for c in controls:
        screen.blit(font_text.render(c, True, (210, 210, 210)), (sidebar_x + 16, y))
        y += 22

def draw_game_over(screen):
    popup_width, popup_height = WIDTH // 2, HEIGHT // 4
    popup = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup.fill((40, 10, 10, 230))

    font_big = pygame.font.SysFont("LucidaConsole", 42, bold=True)
    text = font_big.render("GAME OVER", True, (240, 100, 100))
    popup.blit(text, text.get_rect(center=(popup_width//2, popup_height//2)))
    screen.blit(popup, ((WIDTH - popup_width)//2, (HEIGHT - popup_height)//2))

def draw_win_screen(screen, total_time):
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)
    time_str = f"{minutes}m {seconds}s"
    
    popup_width, popup_height = WIDTH // 2, HEIGHT // 3
    popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup_surface.fill((30, 30, 40, 230))
    win_font = pygame.font.SysFont("LucidaConsole", 36, bold=True)
    win_text = win_font.render("You Win!", True, (220, 180, 240))
    time_font = pygame.font.SysFont("LucidaConsole", 24, bold=True)
    time_text = time_font.render(f"Time spent: {time_str}", True, (200, 200, 200))
    hint_font = pygame.font.SysFont("LucidaConsole", 20)
    hint = hint_font.render("Thank you", True, (220, 200, 200))

    # pop up
    popup_surface.blit(win_text, win_text.get_rect(center=(popup_width//2, popup_height//3)))
    popup_surface.blit(time_text, time_text.get_rect(center=(popup_width//2, popup_height//2)))
    popup_surface.blit(hint, hint.get_rect(center=(popup_width//2, 2 * popup_height//3)))
    
    screen.blit(popup_surface, ((WIDTH - popup_width)//2, (HEIGHT - popup_height)//2))

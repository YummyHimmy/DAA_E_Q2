#asset_load.py
import os
import pygame
from settings import *

def load_asset(name):
    path = os.path.join(ASSET_DIR, name)

    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    except Exception as e:
        print("FAILED:", path)
        print(e)
        return None


def solid_surface(color):
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    s.fill(color)
    return s


def load_all_assets():
    assets = {}

    assets["player_sprites"] = {
        "UP": load_asset("Avatar\Avatar_Up.png"),
        "DOWN": load_asset("Avatar\Avatar_Down.png"),
        "LEFT": load_asset("Avatar\Avatar_Left.png"),
        "RIGHT": load_asset("Avatar\Avatar_Right.png"),
        
        "UP_RIGHT": load_asset("Avatar\Avatar_Up_Right.png"),
        "DOWN_RIGHT": load_asset("Avatar\Avatar_Down_Right.png"),
        "UP_LEFT": load_asset("Avatar\Avatar_Up_Left.png"),
        "DOWN_LEFT": load_asset("Avatar\Avatar_Down_Left.png"),
    }

    assets["ghost_img"] = load_asset("Ghost_Left.png")
    assets["manuscript_img"] = load_asset("Manuscript.png")
    
    assets["wall_regular"] = load_asset("Wall_Regular.png")
    assets["wall_sealed"] = load_asset("Wall_Sealed.png")
    assets["floor_regular"] = load_asset("Floor_Regular.png")
    assets["floor_sealed"] = load_asset("Floor_Sealed.png")

    return assets


# # Fallback: jika asset hilang/korup
# if floor_regular is None:
#     floor_regular = solid_surface((180, 160, 120))
# if floor_sealed is None:
#     floor_sealed = solid_surface((140, 120, 200))
# if wall_regular is None:
#     wall_regular = solid_surface((80, 80, 80))
# if wall_sealed is None:
#     wall_sealed = solid_surface((100, 60, 60))
# if manuscript_img is None:
#     manuscript_img = solid_surface((255, 230, 140))
# if ghost_img is None:
#     ghost_img = solid_surface((200, 60, 140))
# for k, v in player_sprites.items():
#     if v is None:
#         player_sprites[k] = solid_surface((60, 140, 220))
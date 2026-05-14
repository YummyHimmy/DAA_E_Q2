import random
from settings import *

def generate_map(difficulty="EASY"):
    config = DIFFICULTY_SETTINGS[difficulty]

    wall_min = int(TOTAL_TILES * config["wall_ratio"][0])
    wall_max = int(TOTAL_TILES * config["wall_ratio"][1])
    
    sealed_floors_count = int(TOTAL_TILES * config["sealed_ratio"])
    wall_chance = config["wall_chance"]
    spawn_dist = config["spawn_dist"]

    target_final_walls = random.randint(wall_min, wall_max)

    grid = [[WALL for _ in range(GRID)] for _ in range(GRID)]
    
    start_r, start_c = random.randint(0, GRID-1), random.randint(0, GRID-1)
    grid[start_r][start_c] = FLOOR

    stack = [(start_r, start_c)]

    while stack:
        current_r, current_c = stack[-1] 

        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(directions)

        found_path = False
        for dr, dc in directions:
            nr, nc = current_r + dr, current_c + dc

            if 0 <= nr < GRID and 0 <= nc < GRID and grid[nr][nc] == WALL:
                
                wall_between_r = current_r + (dr // 2)
                wall_between_c = current_c + (dc // 2)
                grid[wall_between_r][wall_between_c] = FLOOR
                
                grid[nr][nc] = FLOOR

                stack.append((nr, nc))
                found_path = True
                break 
        
        if not found_path:
            stack.pop() 


    current_wall_count = sum(row.count(WALL) for row in grid)

    walls_coords = []
    for r in range(GRID):
        for c in range(GRID):
            if grid[r][c] == WALL:
                walls_coords.append((r,c))
    random.shuffle(walls_coords)

    while current_wall_count > target_final_walls and walls_coords:
        r, c = walls_coords.pop()
        grid[r][c] = FLOOR
        current_wall_count -= 1

    for r in range(GRID):
        for c in range(GRID):
            if grid[r][c] == WALL:
                if random.random() > wall_chance:
                    grid[r][c] = WALL_SEALED
    
    placed_sealed = 0
    attempts = 0
    while placed_sealed < sealed_floors_count and attempts < 200:
        attempts += 1
        r, c = random.randint(0, GRID-1), random.randint(0, GRID-1)
        if grid[r][c] == FLOOR:
            grid[r][c] = SEALED_FLOOR
            placed_sealed += 1

    placed_manuscripts = 0
    attempts = 0
    while placed_manuscripts < 3 and attempts < 500:
        attempts += 1
        r, c = random.randint(0, GRID-1), random.randint(0, GRID-1)
        if grid[r][c] == FLOOR:
            grid[r][c] = MANUSCRIPT
            placed_manuscripts += 1
        elif grid[r][c] == SEALED_FLOOR:
            grid[r][c] = MANUSCRIPT_SEALED
            placed_manuscripts += 1

    safe_spots = [(r, c) for r in range(GRID) for c in range(GRID) if grid[r][c] == FLOOR]
    
    if len(safe_spots) < 2:
        return generate_map("EASY") 

    player_pos = random.choice(safe_spots)
    safe_spots.remove(player_pos)
    random.shuffle(safe_spots)
    
    ghost_pos = None
    current_req_dist = spawn_dist
    
    for _ in range(5): 
        for spot in safe_spots:
            gr, gc = spot
            pr, pc = player_pos
            dist = abs(gr - pr) + abs(gc - pc)
            
            if dist >= current_req_dist:
                ghost_pos = spot
                break
        
        if ghost_pos: break
        current_req_dist = max(2, current_req_dist - 1) 
        
    if not ghost_pos:
        ghost_pos = safe_spots[0] 

    return grid, player_pos, ghost_pos
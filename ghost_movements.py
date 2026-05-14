from settings import GRID, WALL_SEALED, SEALED_FLOOR
from collections import deque

def get_neighbors(pos, grid):
    """Tile yang bisa dimasuki ghost: semua kecuali WALL_SEALED dan SEALED_FLOOR"""
    r, c = pos
    neighbors = []
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < GRID and 0 <= nc < GRID:
            tile = grid[nr][nc]
            if tile not in (WALL_SEALED, SEALED_FLOOR):
                neighbors.append((nr, nc))
    return neighbors

def bfs_to_target(grid, start, goal):
    queue = deque([start])
    came_from = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for nb in get_neighbors(current, grid):
            if nb not in came_from:
                came_from[nb] = current
                queue.append(nb)
    if goal not in came_from:
        return []
    path = []
    cur = goal
    while cur != start:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path

def find_path(grid, ghost_pos, player_pos):
    pr, pc = player_pos
    player_tile = grid[pr][pc]
    
    if player_tile != SEALED_FLOOR:
        return bfs_to_target(grid, ghost_pos, player_pos)
    
    possible_targets = []
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nr, nc = pr + dr, pc + dc
        if 0 <= nr < GRID and 0 <= nc < GRID:
            tile = grid[nr][nc]
            if tile not in (WALL_SEALED, SEALED_FLOOR):
                possible_targets.append((nr, nc))
    
    if not possible_targets:
        return []
    
    best_path = None
    for target in possible_targets:
        path = bfs_to_target(grid, ghost_pos, target)
        if path:
            if best_path is None or len(path) < len(best_path):
                best_path = path
    return best_path if best_path else []
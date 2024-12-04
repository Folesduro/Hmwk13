import pygame
import random

# Constants
TILE_SIZE = 32
GRID_WIDTH = 20  # Number of tiles horizontally
GRID_HEIGHT = 15  # Number of tiles vertically
FPS = 1  # Updates per second

# Rules
def count_neighbors(matrix, x, y):
    neighbors = 0
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                if matrix[ny][nx] > 0:
                    neighbors += 1
    return neighbors

def apply_rules(matrix):
    new_matrix = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            neighbors = count_neighbors(matrix, x, y)
            current = matrix[y][x]
            if neighbors == 2 or neighbors in (6, 7, 8):
                new_matrix[y][x] = current + 1 if current > 0 else 0
            elif neighbors == 3 and current == 0:
                new_matrix[y][x] = 1
            else:
                new_matrix[y][x] = current

            # Reset to 0 if it exceeds the max stage
            if new_matrix[y][x] >= num_stages:
                new_matrix[y][x] = 0
    return new_matrix

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE))
pygame.display.set_caption("Cellular Automata - Tree Life")
clock = pygame.time.Clock()

# Load tileset
tileset = pygame.image.load(r"C:\Users\foles\PycharmProjects\Hmwk13\features_trees.png")
num_stages = tileset.get_width() // TILE_SIZE

# Initialize matrix
matrix = [[random.randint(0, num_stages - 1) if random.random() < 0.3 else 0
           for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Apply rules and update matrix
    matrix = apply_rules(matrix)

    # Draw the grid
    screen.fill((0, 0, 0))
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            value = matrix[y][x]
            if value > 0:
                tile_rect = pygame.Rect((value - 1) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
                screen.blit(tileset, (x * TILE_SIZE, y * TILE_SIZE), tile_rect)

    # Refresh the screen
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

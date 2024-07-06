# Main.py

import pygame
import sys
from collections import defaultdict
import math
from Tile import Tile

pygame.init()

# Constants
MAX_GRID_WIDTH, MIN_GRID_WITH = 6, 3
TILE_SIZE = 100
WIDTH, HEIGHT = 1000, 800
BG_COLOR = (255, 255, 255)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Settlers of Catan Board")

def generate_grid_pattern(max_grid_width, min_grid_width):
    grid_pattern = []
    for i in range(min_grid_width, max_grid_width + 1):
        grid_pattern.append(i)
    for i in range(max_grid_width - 1, min_grid_width - 1, -1):
        grid_pattern.append(i)
    return grid_pattern

def calculate_hex_points(x, y, size):
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        points.append((x + size * math.cos(angle_rad), y + size * math.sin(angle_rad)))
    return points

def main():
    clock = pygame.time.Clock()
    running = True

    grid_pattern = generate_grid_pattern(MAX_GRID_WIDTH, MIN_GRID_WITH)
    tiles = [[Tile() for _ in range(row)] for row in grid_pattern]

    # Correct calculation for x_offset to center the grid on the x-axis
    hex_width = TILE_SIZE * math.sqrt(3)
    widest_row_width = hex_width + (hex_width * 3/4 * (MAX_GRID_WIDTH - 1))
    x_offset = (WIDTH - widest_row_width) / 2

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        # Draw the hexagonal grid pattern centered within the window
        y = (HEIGHT - sum([TILE_SIZE * math.sqrt(3) / 2 for _ in range(len(tiles))])) / 2
        for row in tiles:
            x = x_offset + TILE_SIZE * 1.5 * ((max(grid_pattern) - len(row)) / 2)
            for tile in row:
                points = calculate_hex_points(x, y, TILE_SIZE / 2)
                pygame.draw.polygon(screen, tile.color, points)
                pygame.draw.polygon(screen, (0, 0, 0), points, 1)
                # Draw the resource type and number on the tile
                font = pygame.font.Font(None, 20)
                text = font.render(f"{tile.resource_type[0]}{tile.number}", True, (0, 0, 0))
                text_rect = text.get_rect(center=(x + TILE_SIZE / 4, y + TILE_SIZE * math.sqrt(3) / 6))
                screen.blit(text, text_rect)
                x += TILE_SIZE * 1.5
            y += TILE_SIZE * math.sqrt(3) / 2

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
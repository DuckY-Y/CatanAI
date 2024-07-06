# Main.py

import pygame
import sys
import math
from collections import defaultdict
from Tile import Tile

pygame.init()

# Constants
LAYER = 3
TILE_SIZE = 100
WIDTH, HEIGHT = 1000, 800
BG_COLOR = (255, 255, 255)
SPACING_FACTOR = 0.95

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Settlers of Catan Board")

def calculate_hex_points(x, y, size):
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        points.append((x + size * math.cos(angle_rad), y + size * math.sin(angle_rad)))
    return points

def generate_hex_grid(layers):
    grid = []
    center = (0, 0)
    grid.append(center)
    
    for layer in range(1, layers + 1):
        for i in range(6):
            for j in range(layer):
                dx = layer * math.cos(math.pi / 3 * i)
                dy = layer * math.sin(math.pi / 3 * i)
                if j > 0:
                    dx -= (layer - j) * math.cos(math.pi / 3 * (i + 1))
                    dy -= (layer - j) * math.sin(math.pi / 3 * (i + 1))
                grid.append((dx, dy))
    return grid

def main():
    clock = pygame.time.Clock()
    running = True

    # Calculate the number of tiles needed
    num_tiles = 1 + 3 * LAYER * (LAYER + 1)
    tiles = [Tile() for _ in range(num_tiles)]
    hex_grid = generate_hex_grid(LAYER)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        # Calculate the center of the screen
        center_x = WIDTH / 2
        center_y = HEIGHT / 2

        for i, (dx, dy) in enumerate(hex_grid):
            x = center_x + dx * TILE_SIZE * SPACING_FACTOR
            y = center_y + dy * TILE_SIZE * SPACING_FACTOR
            points = calculate_hex_points(x, y, TILE_SIZE / 2)
            pygame.draw.polygon(screen, tiles[i].color, points)
            pygame.draw.polygon(screen, (0, 0, 0), points, 1)
            # Draw the resource type and number on the tile
            font = pygame.font.Font(None, 20)
            text = font.render(f"{tiles[i].resource_type[0]}{tiles[i].number}", True, (0, 0, 0))
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
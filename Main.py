# Main.py

import pygame
import sys
import math
from collections import defaultdict
from Tile import Tile

pygame.init()

# Constants
MAX_LAYER = 3
TILE_SIZE = 50
WIDTH, HEIGHT = 1200, 800
BG_COLOR = (255, 255, 255)
SPACING_FACTOR = 0.9

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Settlers of Catan Board")

def hex_to_pixel(q, r, size):
    x = size * (math.sqrt(3) * q + math.sqrt(3) / 2 * r) + WIDTH / 2
    y = size * (3 / 2 * r) + HEIGHT / 2
    return x, y

def draw_hexagon(surface, q, r, size, spacing_factor, color=(0, 0, 0), width=2):
    x, y = hex_to_pixel(q, r, size)
    scaled_size = size * spacing_factor
    corners = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        corners.append((x + scaled_size * math.cos(angle_rad), y + scaled_size * math.sin(angle_rad)))
    pygame.draw.polygon(surface, color, corners, width)
    return corners

def generate_hex_map(max_layer, size):
    hex_map = []
    for layer in range(max_layer + 1):
        for q in range(-layer, layer + 1):
            for r in range(-layer, layer + 1):
                if abs(q + r) <= layer:
                    hex_map.append((q, r))
    return hex_map

def get_edge_id(node1, node2):
    return tuple(sorted([node1, node2]))

def main():
    clock = pygame.time.Clock()
    running = True
    hex_map = generate_hex_map(MAX_LAYER, TILE_SIZE)
    tiles = {hex_pos: Tile() for hex_pos in hex_map}
    node_points = defaultdict(list)
    node_data = {}
    edge_data = {}

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)
        for (q, r), tile in tiles.items():
            # Calculate original corners without scaling
            x, y = hex_to_pixel(q, r, TILE_SIZE)
            original_corners = []
            for i in range(6):
                angle_deg = 60 * i - 30
                angle_rad = math.pi / 180 * angle_deg
                original_corners.append((x + TILE_SIZE * math.cos(angle_rad), y + TILE_SIZE * math.sin(angle_rad)))
            node_points[(q, r)] = original_corners

            # Draw hexagon with tile color
            draw_hexagon(screen, q, r, TILE_SIZE, SPACING_FACTOR, tile.color, 0)

            # Draw hexagon border
            draw_hexagon(screen, q, r, TILE_SIZE, SPACING_FACTOR, (0, 0, 0), 2)

            # Draw the tile number in the center
            font = pygame.font.Font(None, 36)
            text = font.render(str(tile.number), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)

            for i, corner in enumerate(original_corners):
                node_id = (q, r, i)
                if node_id not in node_data:
                    node_data[node_id] = {
                        'position': corner,
                        'hexagons': [(q, r)],
                        'ownership': None,  # No player owns the node initially
                        'building': None    # No building on the node initially
                    }
                else:
                    node_data[node_id]['hexagons'].append((q, r))

                # Calculate edges between corners
                next_i = (i + 1) % 6
                next_node_id = (q, r, next_i)
                edge_id = get_edge_id(node_id, next_node_id)
                if edge_id not in edge_data:
                    edge_data[edge_id] = {
                        'nodes': (node_id, next_node_id),
                        'ownership': None,  # No player owns the edge initially
                        'building': None    # No building on the edge initially
                    }

        # Draw nodes
        for node_id, data in node_data.items():
            pygame.draw.circle(screen, (255, 0, 0), (int(data['position'][0]), int(data['position'][1])), 3)
            if data['building']:
                building_color = (0, 0, 255) if data['building'] == 'settlement' else (0, 255, 0)
                pygame.draw.circle(screen, building_color, (int(data['position'][0]), int(data['position'][1])), 10)

        # Draw edges
        for edge_id, data in edge_data.items():
            node1_pos = node_data[data['nodes'][0]]['position']
            node2_pos = node_data[data['nodes'][1]]['position']
            pygame.draw.line(screen, (0, 0, 0), node1_pos, node2_pos, 2)
            if data['building']:
                building_color = (255, 140, 0)  # Orange color for roads
                midpoint = ((node1_pos[0] + node2_pos[0]) / 2, (node1_pos[1] + node2_pos[1]) / 2)
                pygame.draw.circle(screen, building_color, (int(midpoint[0]), int(midpoint[1])), 5)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

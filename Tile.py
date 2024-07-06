# Tile.py

import random

class Tile:
    RESOURCE_TYPES = ['Wood', 'Brick', 'Sheep', 'Wheat', 'Ore']
    RESOURCE_COLORS = {
        'Wood': (139, 69, 19),  # SaddleBrown
        'Brick': (178, 34, 34),  # FireBrick
        'Sheep': (124, 252, 0),  # LawnGreen
        'Wheat': (255, 215, 0),  # Gold
        'Ore': (112, 128, 144)   # SlateGray
    }
    RESOURCE_DISTRIBUTION = [3, 2, 3, 3, 1]  # Ratios for resource types
    NUMBER_ASSIGNMENTS = list(range(2, 13)) * 2  # Each number from 2 to 12 can be used twice

    def __init__(self):
        self.resource_type = self.assign_resource_type()
        self.number = self.assign_number()
        self.color = self.RESOURCE_COLORS[self.resource_type]

    def assign_resource_type(self):
        # Normalize the distribution to use as weights
        total = sum(self.RESOURCE_DISTRIBUTION)
        weights = [count / total for count in self.RESOURCE_DISTRIBUTION]
        resource_index = random.choices(range(len(self.RESOURCE_TYPES)), weights=weights)[0]
        return self.RESOURCE_TYPES[resource_index]

    def assign_number(self):
        if not self.NUMBER_ASSIGNMENTS:
            self.NUMBER_ASSIGNMENTS = list(range(2, 13)) * 2  # Reset the number assignments
        number = random.choice(self.NUMBER_ASSIGNMENTS)
        self.NUMBER_ASSIGNMENTS.remove(number)
        return number

    def __repr__(self):
        return f"Tile({self.resource_type}, {self.number})"
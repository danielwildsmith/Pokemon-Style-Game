import pygame
from csv import reader
from os import walk


# File reading method taken from ClearCode's Zelda Game Tutorial
def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


# File reading method taken from ClearCode's Zelda Game Tutorial
def import_folder(path):
    surface_list = []
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list


WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 12 * 4
FONT = '../graphics/font/joystix.ttf'
FONT_SIZE = 18

entity_data = {
    'slime': {'health': 20, 'damage': 5, 'moveset': ['Tackle', 'Heal', 'Thunderbolt'],
              'image': '../graphics/entities/slime/back.png'},
    'snake': {'health': 15, 'damage': 5, 'moveset': ['Bite', 'Hiss'],
              'image': '../graphics/entities/snake/face.png'},
    'reptile': {'health': 15, 'damage': 5, 'moveset': ['Quick Attack', 'Focus'],
                'image': '../graphics/entities/reptile/face.png'}
}

env_colors = {
    'GRASS_BG_COLOR': pygame.color.Color(180, 217, 190),
    'GRASS_PLATFORM_COLOR': pygame.color.Color(126, 194, 97),
    'GRASS_PLATFORM_BORDER_COLOR': pygame.color.Color(90, 158, 62),
    'WATER_BG_COLOR': pygame.color.Color(159, 237, 233),
    'WATER_PLATFORM_COLOR': pygame.color.Color(103, 181, 177),
    'WATER_PLATFORM_BORDER_COLOR': pygame.color.Color(62, 117, 114),
}
DEFAULT_BORDER_COLOR = pygame.color.Color(75, 75, 75)
SELECTED_BORDER_COLOR = pygame.color.Color('gold')
DIALOGUE_BG_COLOR = pygame.color.Color(77, 129, 138)
DIALOGUE_BORDER_COLOR = pygame.color.Color(184, 91, 81)
DIALOGUE_TEXT_COLOR = pygame.color.Color(230, 234, 235)

MOVESET_BG_COLOR = pygame.color.Color(186, 188, 191)
MOVESET_TEXT_COLOR = pygame.color.Color(43, 45, 46)

ENTITY_UI_BG_COLOR = pygame.color.Color(230, 241, 242)
ENTITY_UI_BORDER_COLOR = pygame.color.Color(75, 75, 75)
ENTITY_HEALTH_BAR_COLOR = pygame.color.Color(96, 219, 88)

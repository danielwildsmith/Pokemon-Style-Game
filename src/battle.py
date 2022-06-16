import pygame.sprite

from settings import *
from entity import Entity


class Battle:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, FONT_SIZE)
        self.battle_state = True

        self.entity_group = pygame.sprite.Group()
        self.player_entity = Entity(player.entities[0], (275, HEIGHT - 250), self.entity_group)
        self.enemy_entity = Entity('snake', (WIDTH - 325, 190), self.entity_group)

        self.dialogue = f'A wild {self.enemy_entity.name} appeared!'
        self.items = self.create_items(self.dialogue)

        self.selection_index = 0

        self.message_display_time = None
        self.can_display_new_message = True
        self.message_display_cooldown = 1500
        self.player_turn = True
        self.additional_cooldown_run = 0

    def input(self):
        keys = pygame.key.get_pressed()

        if self.selection_index == 0:
            if keys[pygame.K_DOWN]:
                self.selection_index = 2
            elif keys[pygame.K_RIGHT]:
                self.selection_index = 1
        elif self.selection_index == 1:
            if keys[pygame.K_LEFT]:
                self.selection_index = 0
            elif keys[pygame.K_DOWN]:
                self.selection_index = 3
        elif self.selection_index == 2:
            if keys[pygame.K_UP]:
                self.selection_index = 0
            elif keys[pygame.K_RIGHT]:
                self.selection_index = 3
        elif self.selection_index == 3:
            if keys[pygame.K_LEFT]:
                self.selection_index = 2
            elif keys[pygame.K_UP]:
                self.selection_index = 1

        if keys[pygame.K_SPACE] and self.can_display_new_message and self.player_turn:
            self.player_turn = False

            if 0 <= self.selection_index <= 2:
                self.update_dialogue(self.player_entity.attack(self.enemy_entity, self.selection_index))
            if self.selection_index == 3:
                self.update_dialogue(f'{self.player_entity.name} ran away!')
                self.battle_state = False

                # TODO: Enemy entity timer
                # self.dialogue = self.enemy_entity.attack()
                # self.items['dialogue'].text = self.dialogue

    def create_items(self, text):
        items = {
            'dialogue': BattleUI(0, HEIGHT - 150, WIDTH / 2, 150, self.font, DIALOGUE_BG_COLOR, DIALOGUE_BORDER_COLOR,
                                 text_color=DIALOGUE_TEXT_COLOR, text=text, type='dialogue'),
            'player_entity': BattleUI(WIDTH / 2 + 45, HEIGHT - 350, 550, 135, self.font, ENTITY_UI_BG_COLOR,
                                      text=self.player_entity.name, text_color=MOVESET_TEXT_COLOR, type='entity'),
            'enemy_entity': BattleUI(65, 75, 525, 100, self.font, ENTITY_UI_BG_COLOR, text=self.enemy_entity.name,
                                     text_color=MOVESET_TEXT_COLOR, type='entity'),
            'player_health_bar': BattleUI(WIDTH / 2 + 145, HEIGHT - 290, 430, 20, self.font, ENTITY_HEALTH_BAR_COLOR,
                                          text_color=DIALOGUE_BORDER_COLOR, type='player_health_bar'),
            'enemy_health_bar': BattleUI(65 + 100, 75 + 65, 405, 20, self.font, ENTITY_HEALTH_BAR_COLOR,
                                         text_color=DIALOGUE_BORDER_COLOR, type='enemy_health_bar'),
            'option_0': BattleUI(WIDTH / 2 + 15, HEIGHT - 150, WIDTH / 4 - 30, 65, self.font, MOVESET_BG_COLOR,
                                 text=self.player_entity.moveset[0], text_color=MOVESET_TEXT_COLOR, index=0),
            'option_1': BattleUI(WIDTH * 0.75 + 15, HEIGHT - 150, WIDTH / 4 - 30, 65, self.font, MOVESET_BG_COLOR,
                                 text=self.player_entity.moveset[1], text_color=MOVESET_TEXT_COLOR, index=1),
            'option_2': BattleUI(WIDTH / 2 + 15, HEIGHT - 75, WIDTH / 4 - 30, 65, self.font, MOVESET_BG_COLOR,
                                 text=self.player_entity.moveset[2], text_color=MOVESET_TEXT_COLOR, index=2),
            'option_3': BattleUI(WIDTH * 0.75 + 15, HEIGHT - 75, WIDTH / 4 - 30, 65, self.font, MOVESET_BG_COLOR,
                                 text='Run', text_color=MOVESET_TEXT_COLOR, index=3)
        }

        return items

    def create_scene(self):
        self.display_surface.fill(GRASS_BG_COLOR)
        platform_one = pygame.Rect(-100, HEIGHT - 250, 700, 200)
        pygame.draw.ellipse(self.display_surface, GRASS_PLATFORM_COLOR, platform_one)
        pygame.draw.ellipse(self.display_surface, GRASS_PLATFORM_BORDER_COLOR, platform_one, 8)

        platform_two = pygame.Rect(WIDTH / 2 + 50, 150, 550, 165)
        pygame.draw.ellipse(self.display_surface, GRASS_PLATFORM_COLOR, platform_two)
        pygame.draw.ellipse(self.display_surface, GRASS_PLATFORM_BORDER_COLOR, platform_two, 8)

    def cooldowns(self, game_over_cooldown=False):
        current_time = pygame.time.get_ticks()

        if game_over_cooldown:
            if current_time - self.message_display_time >= self.message_display_cooldown:
                print('WHU')
                return False

        if not self.can_display_new_message and self.battle_state:
            if current_time - self.message_display_time >= self.message_display_cooldown:
                self.can_display_new_message = True
                if not self.player_turn:
                    self.update_dialogue(self.enemy_entity.attack(self.player_entity))
                    self.player_turn = True
        return True

    def check_battle_over(self):
        if self.enemy_entity.health <= 0:
            self.update_dialogue(f'{self.player_entity.name} defeated {self.enemy_entity.name}!')
            self.battle_state = False
        elif self.player_entity.health <= 0:
            self.update_dialogue(f'{self.enemy_entity.name} defeated {self.player_entity.name}!')
            self.battle_state = False

    def update_dialogue(self, text):
        self.message_display_time = pygame.time.get_ticks()
        if self.can_display_new_message:
            self.items['dialogue'].text = text
            self.can_display_new_message = False

    def display(self):
        self.create_scene()
        for item in self.items.values():
            if item.type and 'health_bar' in item.type:
                current_health = int(self.player_entity.health if 'player' in item.type else self.enemy_entity.health)
                max_health = entity_data[self.player_entity.name]['health'] if 'player' in item.type else entity_data[self.enemy_entity.name]['health']
                item.display_health_bar(self.display_surface, current_health, max_health)
            else:
                item.display_rect(self.display_surface, self.selection_index)

        self.entity_group.draw(self.display_surface)

    def update(self):
        self.display()
        if not self.battle_state:
            return self.cooldowns(True)
        else:
            self.input()
            self.cooldowns()
            self.check_battle_over()
        return True


class BattleUI:
    def __init__(self, left, top, width, height, font, color, border_color=None, text=None, text_color=None, type=None, index=None):
        self.rect = pygame.Rect(left, top, width, height)
        self.font = font
        self.text = text if text else None
        self.text_color = text_color if text_color else None
        self.color = color
        self.border_color = border_color if border_color else None
        self.type = type if type else None
        self.index = index

    def display_rect(self, surface, selection_num):
        pygame.draw.rect(surface, self.color, self.rect)
        if self.border_color:
            pygame.draw.rect(surface, self.border_color, self.rect, 4)
        else:
            if self.index == selection_num:
                pygame.draw.rect(surface, SELECTED_BORDER_COLOR, self.rect, 4)
            else:
                pygame.draw.rect(surface, DEFAULT_BORDER_COLOR, self.rect, 4)

        if self.text:
            text_surf = self.font.render(self.text, False, self.text_color)
            if self.type == 'dialogue' or self.type == 'entity':
                text_rect = text_surf.get_rect(topleft=self.rect.topleft + pygame.math.Vector2(15, 15))
            else:
                text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def display_health_bar(self, surface, current_health, max_health):
        pygame.draw.rect(surface, ENTITY_UI_BG_COLOR, self.rect)
        ratio = current_health / max_health
        current_health_rect_width = self.rect.width * ratio
        current_health_rect = self.rect.copy()
        current_health_rect.width = current_health_rect_width

        pygame.draw.rect(surface, ENTITY_HEALTH_BAR_COLOR, current_health_rect)
        pygame.draw.rect(surface, ENTITY_UI_BORDER_COLOR, self.rect, 4)

        hp_surf = self.font.render('HP', False, self.text_color)
        hp_rect = hp_surf.get_rect(midright=self.rect.midleft)
        pygame.draw.rect(surface, ENTITY_UI_BORDER_COLOR, hp_rect)
        surface.blit(hp_surf, hp_rect)

        if self.type and 'player' in self.type:
            text_surf = self.font.render(f'{current_health} / {max_health}', False, MOVESET_TEXT_COLOR)
            text_rect = text_surf.get_rect(topright=self.rect.bottomright + pygame.math.Vector2(0, 10))
            surface.blit(text_surf, text_rect)

import pygame
from pygame.sprite import Sprite
from settings import Settings
import random

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen, sprite_sheet):
        """Initialize the alien, and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.sprite_sheet = sprite_sheet

        # Load the alien image, and set its rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = pygame.Rect(sprite_sheet.cell_list[0])

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

        # Ship Sprite Index Locations
        self.Ship_Sprite_Index = [5, 8, 11, 14, 17, 20]
        self.Explosion_Index = [16, 17, 19, 20]

        #Get num of frame_animations
        self.total_num_of_alien_Sprites = 3
        self.num_of_base_frames = len(self.Ship_Sprite_Index) / self.total_num_of_alien_Sprites
        self.frame_counter = 0
        self.frame_start = random.randint(0, 2) * 2

        #points given depending on alien
        if self.frame_start == 0:
            self.points = 10
        elif self.frame_start == 2:
            self.points = 20
        elif self.frame_start == 4:
            self.points = 30

        self.frame_counti = self.frame_start

        #bullet count tracker
        self.bullet_count_tracker = 0

        
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
    def update(self):
        """Move the alien right or left."""
        self.x += (self.ai_settings.alien_speed_factor *
                        self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        self.frame_counter += 1

        if self.frame_counter % Settings.fps / 2 == 0:
            self.frame_counti += 1

            if self.frame_counti >= self.frame_start + 2:
                self.frame_counti = self.frame_start

            """Draw the alien at its current location."""
        self.screen.blit(self.sprite_sheet.sheet, self.rect,
                         self.sprite_sheet.cell_list[self.Ship_Sprite_Index[self.frame_counti]])



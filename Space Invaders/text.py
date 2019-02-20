import pygame
from pygame.locals import *


class Text:

    def __init__(self, screen, text, font_color, background_color,
                 rect_position_x, rect_position_y, font_size):
        self.screen = screen
        self.screen_area = screen.get_rect()
        self.font_color = font_color
        self.background_color = background_color
        self.font = pygame.font.SysFont(None, font_size)
        self.text = self.font.render(text, True, font_color, background_color)
        self.textrect = self.text.get_rect()
        self.textrect.x = rect_position_x
        self.textrect.y = rect_position_y

    def display_text(self):
        self.screen.blit(self.text, self.textrect)

    def change_text(self, text):
        self.text = self.font.render(text, True, self.font_color, self.background_color)
import pygame
from pygame.locals import *

class Text:

    def __init__(self, screen, text, font_color, background_color,
                 rect_position_x, rect_position_y):
        self.screen = screen
        self.screen_area = screen.get_rect()
        self.font = pygame.font.SysFont(None, 48)
        self.text = self.font.render(text, True, font_color, background_color)
        self.textrect = self.text.get_rect()
        self.textrect.x = self.screen_area.centerx - self.textrect.w / 2
        self.textrect.y = self.screen_area.centery - self.textrect.h / 2
        ##elf.textrect = self.text.get_rect()
        #elf.textrect.centerx = screen.get_rect().centerx
        #elf.textrect.centery = screen.get_rect().centery


    def display_text(self):
        self.screen.blit(self.text, self.textrect)
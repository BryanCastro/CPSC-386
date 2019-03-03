import pygame
from pygame.locals import *

class Text:

    def __init__(self, screen, text, font_color, background_color,
                 rect_position_x, rect_position_y):
        self.screen = screen
        self.screen_area = screen.get_rect()
        self.font = pygame.font.SysFont(None, 48)
        self.text = str(text)
        self.text_rendered = self.font.render(text, True, font_color, background_color)
        self.textrect = self.text_rendered.get_rect()
        self.textrect.x = rect_position_x
        self.textrect.y = rect_position_y
        self.font_color = font_color
        self.background_color = background_color
        ##elf.textrect = self.text.get_rect()
        #elf.textrect.centerx = screen.get_rect().centerx
        #elf.textrect.centery = screen.get_rect().centery


    def display_text(self):
        self.screen.blit(self.text_rendered, self.textrect)

    def recalculate_text(self, new_text):
        update_text = self.text + str(new_text)
        self.text_rendered = self.font.render(update_text, True, self.font_color, self.background_color)
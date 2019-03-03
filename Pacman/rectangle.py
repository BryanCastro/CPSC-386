import pygame

class Rectangle:

    def __init__(self, screen, rect_pos_size, color = "Black"):
        self.rect = rect_pos_size
        self.rect_color = color
        self.tag = ""
        self.sprite_name = ""

    def blit_rect(self):
        pygame.draw.rect(self.screen, self.rect_color, self.rect)

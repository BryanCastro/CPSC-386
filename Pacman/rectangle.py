import pygame

class Rectangle:

    def __init__(self, screen, color, rect_pos_size):
        self.screen = screen
        self.rectangle = rect_pos_size
        self.rect_color = color
        print(color)

    def blit_rect(self):
        pygame.draw.rect(self.screen, self.rect_color, self.rectangle)

import pygame
from text import Text
from rectangle import Rectangle

class Main_Menu:

    def __init__(self, screen, colors):
        self.screen = screen
        self.screen_area = screen.get_rect()
        self.colors = colors
        print(self.colors["Red"])
        self.text = Text(self.screen, "Wuddup", colors["Red"], colors["Green"], 50, 50)
        self.background_Rect = Rectangle(screen, colors["Black"], pygame.Rect(self.screen_area.w / 2, 0,
                                         self.screen_area.w /2 , self.screen_area.h))

    def display_menu(self):
        self.background_Rect.blit_rect()
        self.text.display_text()

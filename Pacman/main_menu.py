import pygame
from text import Text
from rectangle import Rectangle

class Main_Menu:

    def __init__(self, screen, colors):
        #self.pacman = pacman
        self.screen = screen
        self.screen_area = screen.get_rect()
        self.colors = colors

        #TEXT WITH BACKGROUND RENDER
        #self.text_title = Text(self.screen, "Pacman", colors["Yellow"], colors["Black"],
        #                       self.screen_area.w/2, 50)
        #self.background_Rect = Rectangle(screen, (0,0, 500, 500), self.colors["Blue"])

        #RENDER BASED ON FONT
        self.myfont = pygame.font.Font("fonts/Early GameBoy.ttf", 50)
        self.title_label = self.myfont.render("PACMAN", 1, (255, 255, 0))
        self.title_label_x = self.center_text_x(self.title_label)
        self.title_label_2 = self.myfont.render("Portal", 1, (255, 255, 0))
        self.title_label_2_x = self.center_text_x(self.title_label_2)
        #self.press_space_label = self.myfont.render("Press Space to play", 1, (255, 255, 0))
        #self.press_space_label_x = self.center_text_x(self.press_space_label)


    def display_menu(self):
        #self.background_Rect.blit_rect()
        #self.text_title.display_text()

        self.screen.blit(self.title_label, (self.title_label_x, 100))
        self.screen.blit(self.title_label_2, (self.title_label_2_x, 150))
       # self.screen.blit(self.press_space_label, (self.press_space_label_x, 200))

    def center_text_x(self, text_label):
        rect = text_label.get_rect()
        return self.screen_area.w /2 - rect.w /2



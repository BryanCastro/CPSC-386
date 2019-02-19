import pygame
from text import Text


class Main_Menu:

    def __init__(self, screen):
        self.screen = screen
        self.screen_area = screen.get_rect()

        #Get title and align at middle of screen
        self.space_invaders_title = Text(screen,"SPACE INVADERS", (0, 255, 0), (0, 0, 0),
                                         self.screen_area.w, self.screen_area.h, 100)
        #self.space_invaders_title.textrect.x = self.space_invaders_title.textrect.x /2
        self.set_text_position_menu(self.space_invaders_title, 4, 6)

        #Get Press Enter Text
        self.press_enter_text = Text(screen, "Press Enter", (0, 255, 0), (0, 0, 0),
                                         self.screen_area.w, self.screen_area.h, 48)
        self.set_text_position_menu(self.press_enter_text, 2, 4, -100)
        #self.press_enter_text.textrect.x = self.press_enter_text.textrect.x / 2

    def set_text_position_menu(self, textObj, x_div, y_div, x_offset = 0, y_offset = 0):
        textObj.textrect.x = (textObj.textrect.x / x_div) + x_offset
        textObj.textrect.y = (textObj.textrect.y / y_div) + y_offset


    def render_menu(self):
        self.space_invaders_title.display_text()
        self.press_enter_text.display_text()
        pygame.display.update()


import pygame
import sys
from main_menu import Main_Menu
from sprite_sheet import Sprite_Sheet


class Game:

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        pygame.init()
        #Checks if game is running
        self.is_running = True
        #Screen Dimensions and info
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Test")

        #colors
        self.colors ={"Black": (0, 0, 0),
                 "Red": (255, 0, 0),
                 "Green": (0, 255, 0),
                 "Blue": (0, 0, 255),
                "White": (255, 255, 255)}

        #Create Objects Here
        self.sprite_sheet = Sprite_Sheet("images/Prototype.png", "text files/Prototype.xml")

        #Grabs sprite dictionary with cropping values
        self.sprite_dictionary = self.sprite_sheet.read_xml()

        #Dubugging and Logs
        #self.sprite_sheet.print_dic_log()

    def __check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def __fill_display(self, color):
        self.screen.fill(self.colors[color])

    def __refresh_display(self):
        self.sprite_sheet.test_sprite(self.screen, self.sprite_dictionary["Pacman_Closed.png"], True, 32)
        pygame.display.update()

    def run_game(self):

        # Objects
        menu = Main_Menu(self.screen, self.colors)

        while self.is_running:
            self.__check_events()
            self.__fill_display("Blue")
            menu.display_menu()
            self.__refresh_display()

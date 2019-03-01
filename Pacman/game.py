import pygame
import sys
from main_menu import Main_Menu
from sprite_sheet import Sprite_Sheet
from character import Pacman
from maze import Maze


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
        self.clock = pygame.time.Clock()

        #colors
        self.colors ={"Black": (0, 0, 0),
                 "Red": (255, 0, 0),
                 "Green": (0, 255, 0),
                 "Blue": (0, 0, 255),
                 "White": (255, 255, 255)}

        #Create Objects Here
        self.sprite_sheet = Sprite_Sheet("images/Prototype.png", "text files/Prototype.xml", self.screen)
        self.sprite_dictionary = self.sprite_sheet.dataDict
        self.maze = Maze(self.screen, self.sprite_sheet, "text files/pacmanportalmaze.txt")
        self.pacman = Pacman(self.screen, self.sprite_sheet, self.maze.scale_size_x, self.maze.scale_size_y)

        #Dubugging and Logs
        #self.sprite_sheet.print_dic_log()

    def __check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
               self.pacman.movement_keydown(event)
            #elif event.type == pygame.KEYUP:
             #   self.pacman.movement_keyup(event)

    def __fill_display(self, color):
        self.screen.fill(self.colors[color])

    def __refresh_display(self):
        #self.sprite_sheet.render_sprite(self.sprite_dictionary["Pacman_Closed.png"], (50, 50), True, 32)
        self.pacman.render_character()
        self.maze.render_maze()
        self.pacman.check_collision(self.maze.wall_coords)
        pygame.display.update()
        self.clock.tick(60)

    def update_movement(self):
        self.pacman.update_movement()

    def run_game(self):

        # Objects
        menu = Main_Menu(self.screen, self.colors)

        while self.is_running:
            self.__check_events()
            self.update_movement()
            self.__fill_display("Blue")
            menu.display_menu()
            self.__refresh_display()

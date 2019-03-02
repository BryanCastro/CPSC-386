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
        self.sprite_sheet = Sprite_Sheet("images/Pacman.png", "text files/Pacman.xml", self.screen)
        self.sprite_dictionary = self.sprite_sheet.dataDict
        self.maze = Maze(self.screen, self.sprite_sheet, "text files/New_Level.txt")
        self.pacman = Pacman(self.screen, self.sprite_sheet, self.maze.scale_size_x, self.maze.scale_size_y,
                             self.maze.pacman_start_x, self.maze.pacman_start_y)

        #Dubugging and Logs
        #self.sprite_sheet.print_dic_log()

        #Others
        self.pellet_collided = []

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
        #print(self.pellet_coords)

        self.maze.render_maze(self.pellet_collided)
        if self.maze.calc_pac_pos:
            self.set_pacman_position()
            self.maze.calc_pac_pos = False
        self.pacman.check_wall_collision(self.maze.wall_coords)
        self.pellet_collided = self.pacman.check_pellet_collision(self.maze.pellet_coords)
        self.pacman.render_character()

        pygame.display.update()
        self.clock.tick(60)

    def update_movement(self):
        self.pacman.update_movement()

    def set_pacman_position(self):
        self.pacman.rect.x = self.maze.pacman_start_x
        self.pacman.rect.y = self.maze.pacman_start_y

    def run_game(self):

        # Objects
        menu = Main_Menu(self.screen, self.colors)

        while self.is_running:
            self.__check_events()
            self.update_movement()
            self.__fill_display("Black")
            #menu.display_menu()
            self.__refresh_display()

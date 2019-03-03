import pygame
import sys
from main_menu import Main_Menu
from sprite_sheet import Sprite_Sheet
from character import Pacman
from maze import Maze
from text import Text
import settings

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

        #Settings
        self.pacman_lives_count = 3


        #Create Objects Here
        self.sprite_sheet = Sprite_Sheet("images/Pacman.png", "text files/Pacman.xml", self.screen)
        self.sprite_dictionary = self.sprite_sheet.dataDict
        self.maze = Maze(self.screen, self.sprite_sheet, "text files/pacmanportalmaze.txt")
        self.pacman = Pacman(self.screen, self.sprite_sheet, self.maze.scale_size_x, self.maze.scale_size_y,
                             self.maze.pacman_start_x, self.maze.pacman_start_y)
        self.score_text = Text(self.screen, "Points: ",self.colors["White"], self.colors["Black"],
                               self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT-self.maze.reserved_height)
        self.lives_text = Text(self.screen, "Lives: ", self.colors["White"], self.colors["Black"],
                               self.maze.half_reserved_width, self.SCREEN_HEIGHT-self.maze.reserved_height)

        self.pacman_lives_stored = []
        self.load_pacman_lives()

        #Center Text Properly
        self.score_text.textrect.x -= self.score_text.textrect.w /2

        #Dubugging and Logs
        #self.sprite_sheet.print_dic_log()

        #Others
        self.allow_movement = False
        self.main_menu = True
        self.pacman_game = False


    def __check_events(self, allow_movement):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.pacman.movement_keydown(event, allow_movement)
            #elif event.type == pygame.KEYUP:
             #   self.pacman.movement_keyup(event)

    def __fill_display(self, color):
        self.screen.fill(self.colors[color])

    def __game_display(self):
        self.update_movement()
        self.score_text.recalculate_text(self.maze.points)
        self.maze.render_maze()
        self.pacman.render_character()
        self.render_lives()
        # Here
        self.allow_movement = self.pacman.check_collision(self.maze, self.allow_movement)

    def __refresh_display(self):

        pygame.display.update()
        self.clock.tick(settings.FPS)

    def update_movement(self):
        self.pacman.update_movement()

    def set_pacman_position(self):
        self.pacman.rect.x = self.maze.pacman_start_x
        self.pacman.rect.y = self.maze.pacman_start_y

    def run_game(self):

        # Objects
        menu = Main_Menu(self.screen, self.colors)

        while self.is_running:
            self.__check_events(self.allow_movement)

            self.__fill_display("Black")
            if self.main_menu:
                menu.display_menu()
            elif self.pacman_game:
                self.__game_display()

            self.__refresh_display()

    def load_pacman_lives(self):
        x = self.lives_text.textrect.x + self.lives_text.textrect.w
        #y = self.SCREEN_HEIGHT-self.maze.reserved_height + self.lives_text.textrect.h/4
        y = self.lives_text.textrect.centery
        for life in range(self.pacman_lives_count):
            self.pacman_lives_stored.append(Pacman(self.screen, self.sprite_sheet, self.maze.scale_size_x,
                                            self.maze.scale_size_y, x, y))
            x += self.pacman.rect.w+self.pacman.rect.w/2

        for life in self.pacman_lives_stored:
            life.rect.y -= life.rect.h/2

    def render_lives(self):
        self.score_text.display_text()
        self.lives_text.display_text()

        for lives in self.pacman_lives_stored:
            lives.render_character()
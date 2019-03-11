import pygame
import sys
import settings
from sprite_sheet import  Sprite_Sheet
from maze import Maze
from character import Pacman
from main_menu import Main_Menu
from text import Text
from character import Ghost
from sound import Sound

class Game:

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):

        pygame.init()
        #Checks if game is running
        self.is_running = True
        #Screen Dimensions and info
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman Portal")
        self.clock = pygame.time.Clock()

        # colors
        self.colors = {"Black": (0, 0, 0),
                       "Red": (255, 0, 0),
                       "Green": (0, 255, 0),
                       "Blue": (0, 0, 255),
                       "White": (255, 255, 255),
                       "Yellow": (255, 255, 0),
                       "Orange": (255, 177, 33)}
        #dimensions
        self.pac_width = 20
        self.pac_height = 20

        #Objects
        self.sprite_sheet = Sprite_Sheet("images/Pacman.png", "text files/Pacman.xml", self.screen)
        self.maze = Maze(self.screen, self.sprite_sheet, "text files/pacmanportalmaze.txt")
        self.pacman = Pacman(self.screen, self.sprite_sheet, self.maze.pacman_start_x, self.maze.pacman_start_y,
                             self.pac_width, self.pac_height, self.maze, self.colors)
        self.pacman_menu = Pacman(self.screen, self.sprite_sheet, -200, 0, 30, 30, self.maze, self.colors)
        self.score_text = Text(self.screen, "Points: ", self.colors["White"], self.colors["Black"],
                               self.SCREEN_WIDTH -250, self.SCREEN_HEIGHT - 50)
        self.lives_text = Text(self.screen, "Lives: ", self.colors["White"], self.colors["Black"],
                               0, self.SCREEN_HEIGHT - 50)
        self.menu = Main_Menu(self.screen, self.colors)
        self.music = Sound("sounds/main_theme.wav", is_music = True)


        # Settings
        self.pacman_lives_count = self.pacman.live_count

        # Ghost
        self.ghost_orange = Ghost(self.screen, self.sprite_sheet,
                                  self.maze.orange_start_x, self.maze.orange_start_y, "Orange")
        self.ghost_blue = Ghost(self.screen, self.sprite_sheet,
             self.maze.blue_start_x, self.maze.blue_start_y, "Blue")
        self.ghost_red = Ghost(self.screen, self.sprite_sheet,
             self.maze.red_start_x, self.maze.red_start_y, "Red")
        self.ghost_pink = Ghost(self.screen, self.sprite_sheet,
                                  self.maze.pink_start_x, self.maze.pink_start_y, "Pink")
        self.ghost_blue.A_star = True
        self.ghost_list = [self.ghost_orange, self.ghost_blue, self.ghost_red, self.ghost_pink]

        #UI
        self.pacman_lives_stored = []
        self.load_pacman_lives()

        # Menus
        self.allow_movement = False
        self.main_menu = True
        self.pacman_game = False

    def update_movement(self):
        self.pacman.update_movement()

    def __check_events(self, allow_movement):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.pacman.movement_keydown(event, allow_movement)
                if event.key == pygame.K_SPACE:
                    self.main_menu = False
                    self.pacman_game = True
                    self.music.play_music()

    def shoot_bullet(self):
        if self.pacman.render_shot:
            self.pacman.spawn_shot()

    def ghost_stuff(self):
        self.ghost_orange.check_collision(self.maze, self.pacman)
        self.ghost_orange.movement()
        self.ghost_orange.render_ghost()
        self.ghost_blue.check_collision(self.maze, self.pacman)
        self.ghost_blue.movement()
        self.ghost_blue.render_ghost()
        self.ghost_red.check_collision(self.maze, self.pacman)
        self.ghost_red.movement()
        self.ghost_red.render_ghost()
        self.ghost_pink.check_collision(self.maze, self.pacman)
        self.ghost_pink.movement()
        self.ghost_pink.render_ghost()

        if self.pacman.ghost_are_scared:
            self.pacman.scared_ghost(self.ghost_pink, self.ghost_blue, self.ghost_orange, self.ghost_red)
        else:
            collision = self.pacman.check_collision_ghost(self.ghost_list)
            if collision:
                self.pacman_lives_count = self.pacman.live_count
                self.load_pacman_lives()
                collision = False


    def __fill_display(self, color):
        self.screen.fill(self.colors[color])

    def __game_display(self):
        self.maze.render_maze()
        self.shoot_bullet()
        self.allow_movement = self.pacman.check_collision(self.maze, self.allow_movement)
        self.pacman.check_shot_collision(self.pacman.portal)
        self.update_movement()
        self.pacman.render_character(self.pac_width, self.pac_height)
        self.pacman.portal.render_portal()
        self.ghost_stuff()
        self.score_text.recalculate_text(self.maze.points)
        self.render_lives()

    def __refresh_display(self):
        pygame.display.update()
        self.clock.tick(settings.FPS)

    def load_pacman_lives(self):
        self.pacman_lives_stored.clear()

        x = self.lives_text.textrect.x + self.lives_text.textrect.w
        y = self.lives_text.textrect.centery
        for life in range(self.pacman_lives_count):
            self.pacman = Pacman(self.screen, self.sprite_sheet, self.maze.pacman_start_x, self.maze.pacman_start_y,
                                 self.pac_width, self.pac_height, self.maze, self.colors)
            self.pacman_lives_stored.append(Pacman(self.screen, self.sprite_sheet,
                                                   x, y, self.pac_width, self.pac_height, self.maze, self.colors))
            x += self.pacman.rect.w+self.pacman.rect.w/2

        for life in self.pacman_lives_stored:
            life.rect.y -= life.rect.h/2

    def render_lives(self):
        self.score_text.display_text()
        self.lives_text.display_text()

        for lives in self.pacman_lives_stored:
            lives.render_character(self.pac_width, self.pac_height)

    def run_game(self):

        while self.is_running:
            self.__check_events(self.allow_movement)
            self.__fill_display("Black")
            if self.main_menu:
                self.menu.display_menu()
                self.pacman_menu.render_character(30, 30)
                self.pacman_menu.update_main_menu_movement()
            elif self.pacman_game:
                self.__game_display()

            self.__refresh_display()


game = Game(460, 600)
game.run_game()
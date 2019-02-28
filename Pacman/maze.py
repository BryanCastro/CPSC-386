import pygame
import math


class Maze():
    def __init__(self, screen, sprite_sheet, maze_txt):
        self.screen = screen
        self.screen_area = screen.get_rect()
        self.sprite_sheet = sprite_sheet
        self.maze_txt = maze_txt

        #####level things
        self.max_chars_line = 0
        self.max_lines = 0
        self.level_lines = self.load_maze() #function
        self.reserved_width = 0
        self.reserved_height = 0
        self.half_reserved_width = 0
        self.half_reserved_height = 0
        self.calculate_pixel_diff() #function


        #####Save wall coords for collision
        self.store_coords = True
        self.wall_coords = []

        #####calculate scale
        self.start_x = 0
        self.start_y = 0
        self.x_increase = 0
        self.y_increase = 0
        self.scale_size = 0
        self.calculate_scale() #function

    def calculate_pixel_diff(self):
        self.reserved_width = math.ceil(self.screen_area.w * .074)
        self.reserved_height = math.ceil(self.screen_area.h * .074)
        self.half_reserved_width = self.reserved_width / 2
        self.half_reserved_height = self.reserved_height / 2

    def calculate_scale(self):
        self.start_x = self.half_reserved_width
        self.start_y = self.half_reserved_height
        self.x_increase = int((self.screen_area.w - self.reserved_width) / self.max_chars_line)
        self.y_increase = int((self.screen_area.h - self.reserved_height) / self.max_lines)
        self.scale_size = self.x_increase

    def load_maze(self):

        with open(self.maze_txt, 'r') as level:
            level_lines = []
            for line in level.readlines():
                self.max_chars_line = 0
                self.max_lines += 1
                new_line = []
                for chars in line:
                    if chars != '\n':
                        self.max_chars_line += 1
                        new_line.append(chars)
                level_lines.append(new_line)

        return level_lines

    def render_maze(self):
        self.start_y = self.half_reserved_height
        self.start_x = self.half_reserved_width

        for line in self.level_lines:

            for char in line:
                sprite_name = ""
                if char == "X":
                   sprite_name = "Bord_Solid.png"
                   if self.store_coords:
                    self.wall_coords.append(pygame.Rect(self.start_x, self.start_y,
                                                        self.x_increase, self.y_increase))
                else:
                    sprite_name = "Ghost_Eyes_Down.png"

                self.sprite_sheet.render_sprite(self.sprite_sheet.dataDict[sprite_name],
                                                   (self.start_x, self.start_y), True, self.scale_size)

                self.start_x = self.start_x + self.x_increase

            self.start_y += self.y_increase
            self.start_x = self.half_reserved_width

        self.store_coords = False
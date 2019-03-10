import pygame
import math
from rectangle import Rectangle


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

        #####calculate scale
        self.start_x = 0
        self.start_y = 0
        self.x_increase = 0
        self.y_increase = 0
        self.scale_size_x = 0
        self.scale_size_y = 0
        self.calculate_scale() #function

        #pacman info
        self.pacman_start_x = 0
        self.pacman_start_y = 0

        #Ghost info
        self.blinky_start_x = 0
        self.blinky_start_y = 0

        #others
        self.pellets_left = 0
        self.store_nodes = []
        self.points = 0
        self.level_blocks = []
        self.load_maze_2() #function



    def calculate_pixel_diff(self):
        self.reserved_width = self.screen_area.w * .074
        self.reserved_height = self.screen_area.h * .074
        self.half_reserved_width = self.reserved_width / 2
        self.half_reserved_height = self.reserved_height / 2

    def calculate_scale(self):
        self.start_x = self.half_reserved_width
        self.start_y = self.half_reserved_height
        self.x_increase = int((self.screen_area.w - self.reserved_width) / self.max_chars_line)
        self.y_increase = int((self.screen_area.h - self.reserved_height) / self.max_lines)
        self.scale_size_x = self.x_increase
        self.scale_size_y = self.y_increase

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

    def load_maze_2(self):
        self.start_y = self.half_reserved_height
        self.start_x = self.half_reserved_width

        for line in self.level_lines:

            for char in line:
                new_rectangle = Rectangle(self.screen, (0, 0, 0, 0))
                new_rectangle.tag = "wall"
                self.scale_size_x = int(self.x_increase)
                self.scale_size_y = int(self.y_increase)

                if char == ".":
                    new_rectangle.sprite_name= "Blank.png"
                    new_rectangle.tag = "no collision"
                elif char == "X":
                    new_rectangle.sprite_name = "Border_Par_Up_Dn.png"
                elif char == "(":
                    new_rectangle.sprite_name = "Border_Curve_Tp_Lt.png"
                elif char == ")":
                    new_rectangle.sprite_name = "Border_Curve_Tp_Rt.png"
                elif char == "|":
                    new_rectangle.sprite_name = "Border_Par_Lt_Rt.png"
                elif char == "[":
                    new_rectangle.sprite_name = "Border_Curve_Bt_Lt.png"
                elif char == "]":
                    new_rectangle.sprite_name = "Border_Curve_Bt_Rt.png"
                elif char == "1":
                    new_rectangle.sprite_name = "Border_St_Lt.png"
                elif char == "-":
                    new_rectangle.sprite_name = "Border_St_Up.png"
                elif char == "_":
                    new_rectangle.sprite_name = "Border_St_Bt.png"
                elif char == "}":
                    new_rectangle.sprite_name = "Border_St_Rt.png"
                elif char == "S":
                    new_rectangle.sprite_name = "Blank.png"
                    new_rectangle.tag = "intersection_pacman_start"
                    self.pacman_start_x = self.start_x
                    self.pacman_start_y = self.start_y
                elif char == "B":
                    new_rectangle.sprite_name = "Blank.png"
                    self.blinky_start_x = self.start_x
                    self.blinky_start_y = self.start_y
                    new_rectangle.tag = "no collision"
                elif char == "O":
                    new_rectangle.sprite_name = "Pellet.png"
                    new_rectangle.tag = "pellet"
                    self.pellets_left += 1
                elif char == "!":
                    new_rectangle.sprite_name = "Blank.png"
                    new_rectangle.tag = "intersection"
                    self.store_nodes.append(new_rectangle)
                else:
                    new_rectangle.sprite_name = "Blank.png"
                    new_rectangle.tag = "no collision"

                new_rectangle.rect = pygame.Rect(int(self.start_x), int(self.start_y), self.scale_size_x, self.scale_size_y)


                self.level_blocks.append(new_rectangle)
                self.start_x = self.start_x + self.x_increase

            self.start_y += self.y_increase
            self.start_x = self.half_reserved_width

    def render_maze(self):

        for block in self.level_blocks:
            self.sprite_sheet.render_sprite(self.sprite_sheet.dataDict[block.sprite_name],
                                            (block.rect.x, block.rect.y), True,
                                            block.rect.w, block.rect.h)

    def save_coords(self, coord_obj):
        coord_obj.append(pygame.Rect(self.start_x, self.start_y,
                                            self.x_increase, self.y_increase))

   ##def dijstra(self, graph, start, goal):
   #    stortest_distance = {}
   #    predecessor = {}
   #    unseenNodes = graph
   #    infinity = 99999999
   #    path = []
   #    for node in unseenNodes:
   #        shortest_distance[node] = infinity
   #    shortest distance[start] = 0
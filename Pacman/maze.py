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
        self.level_lines = self.load_maze() #function

        #####calculate scale
        self.start_x = 0
        self.start_y = 0
        self.x_increase = 0
        self.y_increase = 0

        #pacman info
        self.pacman_start_x = 0
        self.pacman_start_y = 0

        #Ghost info
        self.orange_start_x = 0
        self.orange_start_y = 0
        self.red_start_x = 0
        self.red_start_y = 0
        self.blue_start_x = 0
        self.blue_start_y = 0
        self.pink_start_x = 0
        self.pink_start_y = 0
        #others
        self.pellets_left = 0
        self.store_nodes = []
        self.points = 0
        self.level_blocks = []
        self.load_maze_2() #function

    def load_maze(self):

        with open(self.maze_txt, 'r') as level:
            level_lines = []
            for line in level.readlines():
                self.max_chars_line = 0

                new_line = []
                for chars in line:
                    if chars != '\n':
                        self.max_chars_line += 1
                        new_line.append(chars)
                level_lines.append(new_line)

        return level_lines

    def load_maze_2(self):

        for line in self.level_lines:
            for char in line:
                new_rectangle = Rectangle(self.screen, (0, 0, 0, 0))
                new_rectangle.tag = "wall"

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
                elif char == "Y":
                    new_rectangle.sprite_name = "Blank.png"
                    self.orange_start_x = self.start_x
                    self.orange_start_y = self.start_y
                    new_rectangle.tag = "no collision"
                elif char == "B":
                    new_rectangle.sprite_name = "Blank.png"
                    self.blue_start_x = self.start_x
                    self.blue_start_y = self.start_y
                    new_rectangle.tag = "no collision"
                elif char == "P":
                    new_rectangle.sprite_name = "Blank.png"
                    self.pink_start_x = self.start_x
                    self.pink_start_y = self.start_y
                    new_rectangle.tag = "no collision"
                elif char == "R":
                    new_rectangle.sprite_name = "Blank.png"
                    self.red_start_x = self.start_x
                    self.red_start_y = self.start_y
                    new_rectangle.tag = "no collision"
                elif char == "O":
                    new_rectangle.sprite_name = "Pellet.png"
                    new_rectangle.tag = "pellet"
                    self.pellets_left += 1
                elif char == "!":
                    new_rectangle.sprite_name = "Blank.png"
                    new_rectangle.tag = "intersection"
                    self.store_nodes.append(new_rectangle)
                elif char == "T":
                    new_rectangle.sprite_name = "Power_Pellet.png"
                    new_rectangle.tag = "Power_Pellet"
                    self.store_nodes.append(new_rectangle)
                else:
                    new_rectangle.sprite_name = "Blank.png"
                    new_rectangle.tag = "no collision"

                new_rectangle.rect = pygame.Rect(int(self.start_x), int(self.start_y), 10, 10)

                self.level_blocks.append(new_rectangle)
                self.start_x += 10

            self.start_y += 10
            self.start_x = 0

    def render_maze(self):

        for block in self.level_blocks:
            self.sprite_sheet.render_sprite(self.sprite_sheet.dataDict[block.sprite_name],
                                            (block.rect.x, block.rect.y),
                                            width = block.rect.w, height = block.rect.h)

    def save_coords(self, coord_obj):
        coord_obj.append(pygame.Rect(self.start_x, self.start_y,
                                            self.x_increase, self.y_increase))

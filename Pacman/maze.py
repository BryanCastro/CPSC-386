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
        self.calc_pac_pos = True

        #####Save wall coords for collision
        self.store_coords = True
        self.wall_coords = []

        #####Save Pellets
        self.pellet_coords = []
        self.pellets_left = 0

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

    def calculate_pixel_diff(self):
        #HERE
        #self.reserved_width = math.ceil(self.screen_area.w * .074)
        #self.reserved_height = math.ceil(self.screen_area.h * .074)
        self.reserved_width = self.screen_area.w * .074
        self.reserved_height = self.screen_area.h * .074
        self.half_reserved_width = self.reserved_width / 2
        self.half_reserved_height = self.reserved_height / 2

    def calculate_scale(self):
        self.start_x = self.half_reserved_width
        self.start_y = self.half_reserved_height
        #HERE
        #self.x_increase = int((self.screen_area.w - self.reserved_width) / self.max_chars_line)
        #self.y_increase = int((self.screen_area.h - self.reserved_height) / self.max_lines)
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

    def render_maze(self, pellet_collided):
        self.start_y = self.half_reserved_height
        self.start_x = self.half_reserved_width

        for line in self.level_lines:

            for char in line:
                sprite_name = ""
                self.scale_size_x = int(self.x_increase)
                self.scale_size_y = int(self.y_increase)

                if char == ".":
                    sprite_name = "Blank.png"
                elif char == "X":
                   sprite_name = "Border_Par_Up_Dn.png"
                   if self.store_coords:
                       self.save_coords(self.wall_coords)
                elif char == "(":
                    sprite_name = "Border_Curve_Tp_Lt.png"
                    if self.store_coords:
                        self.save_coords(self.wall_coords)
                elif char == ")":
                    sprite_name = "Border_Curve_Tp_Rt.png"
                    if self.store_coords:
                        self.save_coords(self.wall_coords)
                elif char == "|":
                    sprite_name = "Border_Par_Lt_Rt.png"
                    if self.store_coords:
                        self.save_coords(self.wall_coords)
                elif char == "[":
                    sprite_name = "Border_Curve_Bt_Lt.png"
                    if self.store_coords:
                        self.save_coords(self.wall_coords)
                elif char == "]":
                    sprite_name = "Border_Curve_Bt_Rt.png"
                    if self.store_coords:
                        self.save_coords(self.wall_coords)
                elif char == "1":
                    sprite_name = "Border_St_Lt.png"
                    if self.store_coords:
                        self.save_coords(self.wall_coords)
                elif char == "-":
                    sprite_name = "Border_St_Up.png"
                    if self.store_coords:
                        self.save_coords(self.wall_coords)
                elif char == "_":
                    sprite_name = "Border_St_Bt.png"
                    if self.store_coords:
                        self.save_coords(self.wall_coords)
                elif char == "}":
                    sprite_name = "Border_St_Rt.png"
                    if self.store_coords:
                        self.save_coords(self.wall_coords)
                elif char == "S":
                    sprite_name = "Blank.png"
                    if self.calc_pac_pos:
                        self.pacman_start_x = self.start_x
                        self.pacman_start_y = self.start_y
                elif char == "O":
                    #sprite_name = "Pellet.png"
                    if self.store_coords:
                        sprite_name = "Pellet.png"
                        self.save_coords(self.pellet_coords)
                        self.pellets_left += 1
                    else:
                        for pellet in pellet_collided:
                            if int(self.start_x) == int(pellet.x) and int(self.start_y) == int(pellet.y):
                                sprite_name = "Pellet.png"
                                break
                            else:
                                sprite_name = "Blank.png"

                        if len(pellet_collided) <= 0:
                            sprite_name = "Blank.png"





                else:
                    sprite_name = "Blank.png"


                self.sprite_sheet.render_sprite(self.sprite_sheet.dataDict[sprite_name],
                                                   (self.start_x, self.start_y), True, self.scale_size_x, self.scale_size_y)

                self.start_x = self.start_x + self.x_increase

            self.start_y += self.y_increase
            self.start_x = self.half_reserved_width

        self.store_coords = False

    def save_coords(self, coord_obj):
        coord_obj.append(pygame.Rect(self.start_x, self.start_y,
                                            self.x_increase, self.y_increase))
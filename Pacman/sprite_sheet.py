import pygame
import re
import pandas as pd

class Sprite_Sheet:

    def __init__(self, sheet_file, xml_file):
        self.sheet = pygame.image.load(sheet_file).convert_alpha()
        self.filepath = xml_file
        self.dataDict = {}

    def parse_line(self, source, target, target_x, target_y, target_w, target_h):

        key = ""
        x = 0
        y = 0
        w = 0
        h = 0
        add_to_dict = False

        for i, t in enumerate(source):
            if t == target:
                key = source[i + 1].replace('"', '')
                add_to_dict = True
            if t == target_x:
                x = int(source[i + 1].replace('"', ''))
            if t == target_y:
                y = int(source[i + 1].replace('"', ''))
            if t == target_w:
                w = int(source[i + 1].replace('"', ''))
            if t == target_h:
                h = int(source[i + 1].replace('"', ''))

        if add_to_dict:
            print(key)
            print(w)
            self.dataDict[key] = pygame.Rect(x, y, w, h)
            add_to_dict = False

    def read_xml(self):
        with open(self.filepath, 'r') as file:
            file_context = file.readlines()
            for line in file_context:
                self.parse_line(line.split(), "n=", "x=", "y=", "w=", "h=")

        return self.dataDict

    def print_dic_log(self):
        print(self.dataDict)

    def test_sprite(self, screen, sprite_crop, testing = False, transform_size = 0):
        if testing:
           # print(sprite_crop)


            transform_divsor = sprite_crop.w / transform_size
            new_crop = pygame.Rect(0,0,0,0)
            new_crop.x = float(sprite_crop.x/transform_divsor)
            new_crop.y = float(sprite_crop.y/transform_divsor)
            new_crop.w = float(sprite_crop.w/transform_divsor)
            new_crop.h = float(sprite_crop.h/transform_divsor)
            subsurface_test = self.sheet.subsurface((sprite_crop))
            #print(new_crop)
            #screen.blit(pygame.transform.scale(self.sheet, (transform_size, transform_size)), (0, 0, 0, 0), new_crop)
            testin = pygame.transform.scale(subsurface_test, (transform_size, transform_size))
            screen.blit(testin, (0,0,0,0))
        else:
            screen.blit(self.sheet, (0, 0, 0, 0), sprite_crop)
#

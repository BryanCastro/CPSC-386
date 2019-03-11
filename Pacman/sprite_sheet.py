import pygame

class Sprite_Sheet:

    def __init__(self, sheet_file, xml_file, screen):
        self.screen = screen
        self.sheet = pygame.image.load(sheet_file).convert_alpha()
        self.file_path = xml_file
        self.revised_file = "revised.txt"
        self.dataDict = {}
        self.__read_xml()

########START-Used to clean up xml file-START###########
    def __parse_line(self, source):

        key = ""
        x = 0
        y = 0
        w = 0
        h = 0
        add_to_dict = False
        store = str(source)

        for line in store.split():
            if "n=" in line:
                add_to_dict = True
                key = self.__clean_string("n=", line)
            elif "x=" in line:
                x = self.__clean_string("x=", line, True)
            elif "y=" in line:
                y = self.__clean_string("y=", line, True)
            elif "w=" in line:
                w = self.__clean_string("w=", line, True)
            elif "h=" in line:
                h = self.__clean_string("h=", line, True)

        if add_to_dict:
            self.dataDict[key] = pygame.Rect(x, y, w, h)
            add_to_dict = False

    def __read_xml(self):

        fixed_file = open(self.revised_file, "w+")

        with open(self.file_path, 'r') as file:
            file_context = file.readlines()
            for line in file_context:
                nl = self.__remove_unecessaries(line.split())
                fixed_file.write(nl)

        fixed_file.close()

        with open(self.revised_file, 'r') as file:
            file_context = file.readlines()
            for line in file_context:
                self.__parse_line(line.split())

        return self.dataDict

    def print_dic_log(self):
        print("printing dic\n")
        print(self.dataDict)

    def __remove_unecessaries(self, source):
        store = str(source)
        newline=""

        for line in store.split():
            if "oX=" in line:
               self.__clean_string("oX=", line)
            elif "oY=" in line:
                self.__clean_string("oY=", line)
            elif "oW=" in line:
                self.__clean_string("oW=", line)
            elif "oH=" in line:
                self.__clean_string("oH=", line)
            else:
                newline += " " + line

        newline = newline.replace("'", '')
        newline += '\n'
        return newline

    def __clean_string(self, str_find, line, return_int=False):
        line = line.replace(str_find, '')
        line = line.replace('"', '')
        line = line.replace(',', '')
        line = line.replace("'", '')
        line = line.replace("/>", '')
        line = line.replace("]", '')

        if not return_int:
            return line
        else:
            return int(line)

########END-Used to clean up xml file-END###########

    def render_sprite(self, sprite_crop, sprite_position,
                      flipped_x = False, flipped_y = False, rotation_up = False, rotation_down = False,
                      width = 0, height = 0):

            subsurface_transform = self.sheet.subsurface(sprite_crop)
            scaled_sprite = pygame.transform.scale(subsurface_transform, (width, height))

            if flipped_x:
                flipped = pygame.transform.flip(scaled_sprite, True, False)
                self.screen.blit(flipped, sprite_position)
            elif flipped_y:
                flipped = pygame.transform.flip(scaled_sprite, False, True)
                self.screen.blit(flipped, sprite_position)
            elif rotation_up:
                rotation = pygame.transform.rotate(scaled_sprite, 90)
                self.screen.blit(rotation, sprite_position)
            elif rotation_down:
                rotation = pygame.transform.rotate(scaled_sprite, -90)
                self.screen.blit(rotation, sprite_position)
            else:
                self.screen.blit(scaled_sprite, sprite_position)

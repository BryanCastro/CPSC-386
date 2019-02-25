import pygame

class Character():

    def __init__(self, screen, sprite_sheet, char_dimensions):
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.animation_sprites = []
        self.death_sprites = []
        self.animation_frames = 0
        self.death_frames = len(self.death_sprites)
        self.rect = pygame.Rect(char_dimensions)
        self.animation_index = 0
        self.death_index = 0

    def render_character(self):
        print(self.animation_index)
        #self.sprite_sheet.render_sprite(self.sprite_sheet.dataDict["Pacman_Full_Open.png"], self.rect)
        self.sprite_sheet.render_sprite(self.animation_sprites[self.animation_index], self.rect)
        self.animation_index += 1


        if self.animation_index >= self.animation_frames:
            self.animation_index = 0

    def load_animation_sprites(self, sprites):
        for sprite in sprites:
            print(sprite)
            self.animation_sprites.append(self.sprite_sheet.dataDict[sprite])

        self.animation_frames = len(self.animation_sprites)

    def load_death_sprites(self, sprites):
        for sprite in sprites:
            self.death_sprites.append(sprite)


class Pacman(Character):

    def __init__(self, screen, sprite_sheet):
        super(Pacman, self).__init__(screen, sprite_sheet, (32, 32, 32, 32))
        self.animation_keys= ["Pacman_Closed.png", "Pacman_Semi_Open.png", "Pacman_Full_Open.png"]
        self.load_animation_sprites(self.animation_keys)
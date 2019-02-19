import pygame

class Special_Ship:

    def __init__(self,screen, sprite_sheet):
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.sprite_pos_sheet = 0
        self.rect = pygame.Rect(sprite_sheet.cell_list[0])
        self.sprite_crop = sprite_sheet.cell_list[self.sprite_pos_sheet]
        self.speed = 5.0

    def movement(self):
        self.rect.x += self.speed

    def blit_special_ship(self):
        self.screen.blit(self.sprite_sheet.sheet, self.rect, self .sprite_crop)

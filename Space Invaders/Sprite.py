import pygame

class Sprite:

    def __init__(self, screen, sprite_sheet, crop_index, rect_position_x, rect_position_y):
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.crop_location = pygame.Rect(sprite_sheet.cell_list[crop_index])
        self.rect_location = pygame.Rect(0, 0, 32, 32)
        self.rect_location.x = rect_position_x
        self.rect_location.y = rect_position_y

    def blitme(self):
        self.screen.blit(self.sprite_sheet.sheet, self.rect_location,self.crop_location)
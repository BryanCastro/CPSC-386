import pygame
import copy
from rectangle import Rectangle

class Portal():

    def __init__(self, sprite_sheet, screen, colors, orange = False, blue = False):
        self.screen = screen
        self.colors = colors
        self.sprite_sheet = sprite_sheet
        self.shot_sprite = sprite_sheet.dataDict["Power_Pellet.png"]

        self.shot_rect = pygame.Rect(0,0,0,0)
        self.shot_speed = 15

        self.is_shooting = False
        self.blue_shot = False
        self.orange_shot = False

        self.up = False
        self.right = False
        self.down = False
        self.left = False

        self.rectangle_portal = Rectangle(self.screen, pygame.Rect(0, 0, 0 ,0), self.colors["Black"])

        if orange:
            self.rectangle_portal.rect_color = self.colors["Orange"]


    def get_shot_direction(self, pacman_rect,up = False, right = False, down = False, left = False):

        if not self.is_shooting:
            copy_of_rect = copy.deepcopy(pacman_rect)
            self.shot_rect = copy_of_rect
            self.up = up
            self.right = right
            self.down = down
            self.left = left
            self.is_shooting = True
        else:
            self.update_shot()
            self.render_shot()

    def update_shot(self):
        if self.up:
            self.shot_rect.y -= self.shot_speed
        elif self.right:
            self.shot_rect.x += self.shot_speed
        elif self.down:
            self.shot_rect.y += self.shot_speed
        elif self.left:
            self.shot_rect.x -= self.shot_speed

    def render_shot(self):
        self.sprite_sheet.render_sprite(self.shot_sprite, self.shot_rect,
                                        width = 10, height = 10)

    def render_portal(self):

            if self.right:
                self.rectangle_portal.rect.x -= 10
            if self.down:
                self.rectangle_portal.rect.y -= 10


            #self.rectangle_portal.rect = wall_rect
            self.rectangle_portal.blit_rect()


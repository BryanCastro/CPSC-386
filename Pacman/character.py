import pygame

class Character():

    def __init__(self, screen, sprite_sheet, char_dimensions, scale_size):
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.animation_sprites = []
        self.death_sprites = []
        self.animation_frames = 0
        self.death_frames = len(self.death_sprites)
        self.rect = pygame.Rect(char_dimensions)
        self.animation_index = 0
        self.death_index = 0
        self.speed = 0
        self.scale_size = scale_size

    def render_character(self):
        self.sprite_sheet.render_sprite(self.animation_sprites[self.animation_index], self.rect, True, self.scale_size)
        self.animation_index += 1


        if self.animation_index >= self.animation_frames:
            self.animation_index = 0

    def load_animation_sprites(self, sprites):
        for sprite in sprites:
            self.animation_sprites.append(self.sprite_sheet.dataDict[sprite])

        self.animation_frames = len(self.animation_sprites)

    def load_death_sprites(self, sprites):
        for sprite in sprites:
            self.death_sprites.append(sprite)


class Pacman(Character):

    def __init__(self, screen, sprite_sheet, scale_size):
        super(Pacman, self).__init__(screen, sprite_sheet, (50, 50, 32, 32), scale_size)
        self.animation_keys= ["Pacman_Closed.png", "Pacman_Semi_Open.png", "Pacman_Full_Open.png",
                              "Pacman_Semi_Open.png", "Pacman_Closed.png"]
        self.load_animation_sprites(self.animation_keys)
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False
        self.speed = 5

    def movement_keydown(self, event):

        if event.key == pygame.K_RIGHT:
            self.move_right = True
        if event.key == pygame.K_LEFT:
            self.move_left = True
        if event.key == pygame.K_UP:
            self.move_up = True
        if event.key == pygame.K_DOWN:
            self.move_down = True


    def movement_keyup(self, event):
        if event.key == pygame.K_RIGHT:
            self.move_right = False
        if event.key == pygame.K_LEFT:
            self.move_left = False
        if event.key == pygame.K_UP:
            self.move_up = False
        if event.key == pygame.K_DOWN:
            self.move_down = False

    def update_movement(self):
        if self.move_right:
            self.rect.x += self.speed
        elif self.move_left:
            self.rect.x -= self.speed
        elif self.move_up:
            self.rect.y -= self.speed
        elif self.move_down:
            self.rect.y += self.speed

    def check_collision(self, wall_coords):

        for wall in wall_coords:
           if self.rect.x > wall.x and self.rect.x < (wall.x + wall.h) and self.rect.y > wall.y and self.rect.y < wall.y + wall.h:
                print("collision at :" + str(wall))
                self.move_left = False
                self.move_right = False
                self.move_down = False
                self.move_up = False

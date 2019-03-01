import pygame

class Character():

    def __init__(self, screen, sprite_sheet, char_dimensions, scale_size_x, scale_size_y):
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
        self.scale_size_x = scale_size_x * 2
        self.scale_size_y = scale_size_y * 2
        self.scale_sprite() #function

    def render_character(self):
        print(self.rect)
        print(self.scale_size_x)
        self.sprite_sheet.render_sprite(self.animation_sprites[self.animation_index], self.rect, True, self.scale_size_x, self.scale_size_y)
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

    def scale_sprite(self):
        self.rect.w = self.scale_size_x
        self.rect.h = self.scale_size_y

class Pacman(Character):

    def __init__(self, screen, sprite_sheet, scale_size_x, scale_size_y, start_x, start_y):
        super(Pacman, self).__init__(screen, sprite_sheet, (start_x, start_y, 32, 32), scale_size_x, scale_size_y)
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
        if event.key == pygame.K_q:
            pygame.quit()


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
            testvar = 10

            if self.rect.colliderect(wall):
                if self.rect.x >= wall.x and self.move_left:
                    self.rect.x += testvar
                    self.restart_movement()
                if self.rect.x <= wall.x and self.move_right:
                    self.rect.x -= testvar
                    self.restart_movement()
                if self.rect.y >= wall.y and self.move_up:
                    self.rect.y += testvar
                    self.restart_movement()
                if self.rect.y <= wall.y and self.move_down:
                    self.rect.y -= testvar
                    self.restart_movement()
                #print("Collision at: "+ str(wall))

    def restart_movement(self, move_left = False, move_right = False, move_up = False, move_down = False):
        self.move_left = move_left
        self.move_right = move_right
        self.move_up = move_up
        self.move_down = move_down

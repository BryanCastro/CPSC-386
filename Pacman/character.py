import pygame
import settings
import random
from portal import Portal
from sound import Sound

class Character():

    def __init__(self, screen, sprite_sheet, char_dimensions):
        self.screen = screen
        self.screen_area = self.screen.get_rect()
        self.sprite_sheet = sprite_sheet
        self.animation_sprites = []
        self.death_sprites = []
        self.animation_frames = 0
        self.death_frames = len(self.death_sprites)
        self.rect = pygame.Rect(char_dimensions)
        self.animation_index = 0
        self.death_index = 0
        self.speed = 5

        #Transformation
        self.flipped_x = False
        self.flipped_y = False
        self.rotation_up = False
        self.rotation_down = False

        #For Clock
        self.character_spawn_time = 0

    def render_character(self, width, height):
        self.character_spawn_time += 1

        self.sprite_sheet.render_sprite(self.animation_sprites[self.animation_index], self.rect,
                                        self.flipped_x, self.flipped_y, self.rotation_up, self.rotation_down,
                                        width, height)

        if  self.character_spawn_time % (settings.FPS/self.animation_frames) == 0:
            self.animation_index += 1

        if self.animation_index >= self.animation_frames:
            self.animation_index = 0

    def load_animation_sprites(self, sprites):
        self.animation_sprites.clear()

        for sprite in sprites:
            self.animation_sprites.append(self.sprite_sheet.dataDict[sprite])

        self.animation_frames = len(self.animation_sprites)

    def load_death_sprites(self, sprites):
        for sprite in sprites:
            self.death_sprites.append(sprite)

class Pacman(Character):

    def __init__(self, screen, sprite_sheet,start_x, start_y, width, height, maze, colors):
        super(Pacman, self).__init__(screen, sprite_sheet, (start_x, start_y, width, height))
        self.maze = maze
        self.animation_keys= ["Pacman_Closed.png", "Pacman_Semi_Open.png", "Pacman_Full_Open.png",
                              "Pacman_Semi_Open.png", "Pacman_Closed.png"]
        self.load_animation_sprites(self.animation_keys)
        self.colors = colors
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False

        self.facing_right = False
        self.facing_up = False
        self.facing_down = False
        self.facing_left = False

        self.render_shot = False

        self.live_count = 3

        self.pac_chomp = Sound("sounds/Pacman_Waka_Waka.wav", is_effect=True)

        # Shot
        self.portal = Portal(self.sprite_sheet, self.screen, self.colors, orange = True)
        self.blue_portal = Portal(self.sprite_sheet, self.screen, self.colors, blue = True)
        self.portal_num = 0

        #Ghost
        self.ghost_are_scared = False
        self.scared_counter = 1000

    def spawn_shot(self):
        if self.portal_num == 0:
            self.portal.get_shot_direction(self.rect,up =self.facing_up, right =self.facing_right,
                                           down = self.facing_down, left = self.facing_left)

    def movement_keydown(self, event, allow_movement):
        if allow_movement:
            if event.key == pygame.K_RIGHT:
                self.restart_movement(move_right=True)
                self.restart_transormation(flipped_x=False)
                self.set_bullet_direction(right = True)
            if event.key == pygame.K_LEFT:
                self.restart_movement(move_left=True)
                self.restart_transormation(flipped_x=True)
                self.set_bullet_direction(left = True)
            if event.key == pygame.K_UP:
                self.restart_movement(move_up=True)
                self.restart_transormation(rotation_up=True)
                self.set_bullet_direction(up = True)
            if event.key == pygame.K_DOWN:
                self.restart_movement(move_down=True)
                self.restart_transormation(rotation_down=True)
                self.set_bullet_direction(down = True)
            if event.key == pygame.K_s:
                self.speed *= 2
            if event.key == pygame.K_q:
                pygame.quit()
            if event.key == pygame.K_z:
                self.render_shot = True

    def update_movement(self):
        if self.move_right:
            self.rect.x += self.speed
        elif self.move_left:
            self.rect.x -= self.speed
        elif self.move_up:
            self.rect.y -= self.speed
        elif self.move_down:
            self.rect.y += self.speed

    def update_main_menu_movement(self):
        if self.rect.x + self.rect.w>= self.screen_area.w:
            self.rect.y +=self.speed
        elif self.rect.y + self.rect.h >=self.screen_area.h:
            self.rect.x -=self.speed
        elif self.rect.y > 0 and self.rect.x == 1:
            self.rect.y -=self.speed
        else:
            self.rect.x += self.speed

        if self.rect.y + self.rect.h == self.screen_area.h:
            self.rect.x -= 1
        if self.rect.y + self.rect.h == self.screen_area.h and self.rect.x == 1:
            self.rect.y -= 1

    def check_collision(self, maze, allow_movement):
        testvar = 10

        for block in maze.level_blocks:
            allow_movement = False
            if self.rect.colliderect(block.rect):

                if block.tag == "wall":
                    #self.rect.x += self.speed*2
                    if self.rect.x >= block.rect.x and self.move_left:
                        self.restart_movement()
                        self.rect.x += testvar
                    if self.rect.x <= block.rect.x and self.move_right:
                        self.rect.x -= testvar
                        self.restart_movement()
                    if self.rect.y>= block.rect.y and self.move_up:
                        self.rect.y += testvar
                        self.restart_movement()
                    if self.rect.y <= block.rect.y and self.move_down:
                        self.rect.y -= testvar
                        self.restart_movement()
                if block.tag == "pellet":
                    self.pac_chomp.play_sound()
                    block.sprite_name = "Blank.png"
                    block.tag = "no collision"
                    maze.pellets_left -= 1
                    maze.points += 10
                if block.tag == "intersection_pacman_start":
                    allow_movement = True
                    return allow_movement
                if block.tag == "intersection":
                    if block.rect.centerx == self.rect.centerx:
                        allow_movement = True
                        return allow_movement
                if block.tag == "Power_Pellet":
                    if block.rect.centerx == self.rect.centerx:
                        allow_movement = True
                        return allow_movement
                    block.sprite_name = "Blank.png"
                    block.tag = "no collision"
                    maze.pellets_left -= 1
                    self.ghost_are_scared = True
                    maze.points += 10

    def check_collision_ghost(self, ghost_list):

        for ghost in ghost_list:
            if self.rect.colliderect(ghost.rect):
                print(self.live_count)
                self.live_count -=1
                return True


    def check_shot_collision(self, shot):
        for block in self.maze.level_blocks:
            if shot.shot_rect.colliderect(block.rect):
                if block.tag == "wall":
                    self.render_shot = False
                    shot.is_shooting = False
                    shot.rectangle_portal.rect = pygame.Rect(block.rect)
                    return

    def restart_movement(self, move_left = False, move_right = False, move_up = False, move_down = False):
        self.move_left = move_left
        self.move_right = move_right
        self.move_up = move_up
        self.move_down = move_down

    def restart_transormation(self, flipped_x = False, flipped_y = False, rotation_up = False, rotation_down = False):
        self.flipped_x = flipped_x
        self.flipped_y = flipped_y
        self.rotation_up = rotation_up
        self.rotation_down = rotation_down

    def set_bullet_direction(self, up = False, right = False, down = False, left = False):
        self.facing_up = up
        self.facing_right = right
        self.facing_down = down
        self.facing_left = left

    def scared_ghost(self, ghost_1, ghost_2, ghost_3, ghost_4):
        self.scared_counter -= 1

        ghost_1.is_scared = True
        ghost_2.is_scared = True
        ghost_3.is_scared = True
        ghost_4.is_scared = True



class Ghost(Character):
    def __init__(self, screen, sprite_sheet, start_x, start_y, ghost_color):
        super(Ghost, self).__init__(screen, sprite_sheet, (start_x, start_y, 30, 30))

        self.ghost_color = ghost_color

        self.speed = 3

        self.A_star = False

        #Blue Ghost
        self.animation_keys_blue_up = ["Blue_Ghost_Up_1.png", "Blue_Ghost_Up_2.png"]
        self.animation_keys_blue_right =["Blue_Ghost_Right_1.png", "Blue_Ghost_Right_2.png"]
        self.animation_keys_blue_down = ["Blue_Ghost_Down_1.png", "Blue_Ghost_Down_2.png"]
        self.animation_keys_blue_left = ["Blue_Ghost_Left_1.png", "Blue_Ghost_Left_2.png"]

        #Orange Ghost
        self.animation_keys_orange_up = ["Orange_Ghost_Up_1.png", "Orange_Ghost_Up_2.png"]
        self.animation_keys_orange_right = ["Orange_Ghost_Right_1.png", "Orange_Ghost_Right_2.png"]
        self.animation_keys_orange_down = ["Orange_Ghost_Down_1.png", "Orange_Ghost_Down_2.png"]
        self.animation_keys_orange_left = ["Orange_Ghost_Left_1.png", "Orange_Ghost_Left_2.png"]

        #Red Ghost
        self.animation_keys_red_up = ["Red_Ghost_Up_1.png", "Red_Ghost_Up_2.png"]
        self.animation_keys_red_right = ["Red_Ghost_Right_1.png", "Red_Ghost_Right_2.png"]
        self.animation_keys_red_down = ["Red_Ghost_Down_1.png", "Red_Ghost_Down_2.png"]
        self.animation_keys_red_left = ["Red_Ghost_Left_1.png", "Red_Ghost_Left_2.png"]

        #Pink Ghost
        self.animation_keys_pink_up = ["Pink_Ghost_Up_1.png", "Pink_Ghost_Up_2.png"]
        self.animation_keys_pink_right = ["Pink_Ghost_Right_1.png", "Pink_Ghost_Right_2.png"]
        self.animation_keys_pink_down = ["Pink_Ghost_Down_1.png", "Pink_Ghost_Down_2.png"]
        self.animation_keys_pink_left = ["Pink_Ghost_Left_1.png", "Pink_Ghost_Left_2.png"]

        #Scared Ghost
        self.animation_keys_scared = ["Scared_Ghost_Blue.png", "Scared_Ghost_White.png"]

        if ghost_color == "Blue":
            self.load_animation_sprites(self.animation_keys_blue_up)
        elif ghost_color == "Orange":
            self.load_animation_sprites(self.animation_keys_orange_up)
        elif ghost_color == "Red":
            self.load_animation_sprites(self.animation_keys_red_up)
        elif ghost_color == "Pink":
            self.load_animation_sprites(self.animation_keys_pink_up)

        self.move_left = False
        self.move_right = True
        self.move_up = False
        self.move_down = False

        self.is_scared = False
        self.scared_counter = 10000

    def render_ghost(self):
        self.render_character(30, 30)

    def movement(self):
        if self.is_scared:
            self.load_animation_sprites(self.animation_keys_scared)
        elif self.A_star:
            self.compressed_a_star()
        else:
            self.compressed_base_star()



    def restart_movement(self, move_left = False, move_right = False, move_up = False, move_down = False):
        self.move_left = move_left
        self.move_right = move_right
        self.move_up = move_up
        self.move_down = move_down

    def check_collision(self, maze, pacman):

        for node in maze.store_nodes:
            if self.rect.colliderect(node):
                if self.is_scared:

                    self.scared_counter -= 1
                    if pacman.rect.x < self.rect.x and pacman.rect.y > self.rect.y:
                        self.restart_movement(move_up=True)
                    elif pacman.rect.x > self.rect.x and pacman.rect.y < self.rect.y:
                        self.restart_movement(move_down= True)
                    elif pacman.rect.x < self.rect.x:
                        self.restart_movement(move_right = True)
                    elif pacman.rect.y > self.rect.y:
                        self.restart_movement(move_down = True)
                    elif pacman.rect.x > self.rect.x:
                        self.restart_movement(move_left = True)

                    if self.scared_counter <= 0:
                        self.scared_counter = 10000
                        self.is_scared = False
                else:
                    if pacman.rect.x > self.rect.x and pacman.rect.y < self.rect.y:
                        self.restart_movement(move_up=True)
                    elif pacman.rect.x < self.rect.x and pacman.rect.y > self.rect.y:
                        self.restart_movement(move_down= True)
                    elif pacman.rect.x > self.rect.x:
                        self.restart_movement(move_right = True)
                    elif pacman.rect.y > self.rect.y:
                        self.restart_movement(move_down = True)
                    elif pacman.rect.x < self.rect.x:
                        self.restart_movement(move_left = True)

        if self.rect.x > self.screen_area.w:
            self.restart_movement(move_left = True)
        elif self.rect.x < 0:
            self.restart_movement(move_right = True)
        elif self.rect.y < 0:
            self.restart_movement(move_down = True)
        elif self.rect.y > self.screen_area.h:
            self.restart_movement(move_up = True)

    def compressed_a_star(self):
        rag = random.randint(1, 4)

        if self.ghost_color == "Blue":
            if rag == 1:
                self.move_right == True
                self.load_animation_sprites(self.animation_keys_blue_right)
                self.rect.x += self.speed
            if rag == 2:
                self.move_down == True
                self.load_animation_sprites(self.animation_keys_blue_down)
                self.rect.y += self.speed
            if rag == 3:
                self.move_left == True
                self.load_animation_sprites(self.animation_keys_blue_left)
                self.rect.x -= self.speed
            if rag == 4:
                self.move_up == True
                self.load_animation_sprites(self.animation_keys_blue_up)
                self.rect.y -= self.speed
        elif self.ghost_color == "Orange":
            if self.move_right == True:
                self.load_animation_sprites(self.animation_keys_orange_right)
                self.rect.x += self.speed
            elif self.move_down == True:
                self.load_animation_sprites(self.animation_keys_orange_down)
                self.rect.y += self.speed
            elif self.move_left == True:
                self.load_animation_sprites(self.animation_keys_orange_left)
                self.rect.x -= self.speed
            elif self.move_up == True:
                self.load_animation_sprites(self.animation_keys_orange_up)
                self.rect.y -= self.speed
        elif self.ghost_color == "Red":
            if self.move_right == True:
                self.load_animation_sprites(self.animation_keys_red_right)
                self.rect.x += self.speed
            elif self.move_down == True:
                self.load_animation_sprites(self.animation_keys_red_down)
                self.rect.y += self.speed
            elif self.move_left == True:
                self.load_animation_sprites(self.animation_keys_red_left)
                self.rect.x -= self.speed
            elif self.move_up == True:
                self.load_animation_sprites(self.animation_keys_red_up)
                self.rect.y -= self.speed
        elif self.ghost_color == "Pink":
            if self.move_right == True:
                self.load_animation_sprites(self.animation_keys_pink_right)
                self.rect.x += self.speed
            elif self.move_down == True:
                self.load_animation_sprites(self.animation_keys_pink_down)
                self.rect.y += self.speed
            elif self.move_left == True:
                self.load_animation_sprites(self.animation_keys_pink_left)
                self.rect.x -= self.speed
            elif self.move_up == True:
                self.load_animation_sprites(self.animation_keys_pink_up)
                self.rect.y -= self.speed

    def compressed_base_star(self):

        if self.ghost_color == "Blue":
            if self.move_right == True:
                self.load_animation_sprites(self.animation_keys_blue_right)
                self.rect.x += self.speed
            elif self.move_down == True:
                self.load_animation_sprites(self.animation_keys_blue_down)
                self.rect.y += self.speed
            elif self.move_left == True:
                self.load_animation_sprites(self.animation_keys_blue_left)
                self.rect.x -= self.speed
            elif self.move_up == True:
                self.load_animation_sprites(self.animation_keys_blue_up)
                self.rect.y -= self.speed
        elif self.ghost_color == "Orange":
            if self.move_right == True:
                self.load_animation_sprites(self.animation_keys_orange_right)
                self.rect.x += self.speed
            elif self.move_down == True:
                self.load_animation_sprites(self.animation_keys_orange_down)
                self.rect.y += self.speed
            elif self.move_left == True:
                self.load_animation_sprites(self.animation_keys_orange_left)
                self.rect.x -= self.speed
            elif self.move_up == True:
                self.load_animation_sprites(self.animation_keys_orange_up)
                self.rect.y -= self.speed
        elif self.ghost_color == "Red":
            if self.move_right == True:
                self.load_animation_sprites(self.animation_keys_red_right)
                self.rect.x += self.speed
            elif self.move_down == True:
                self.load_animation_sprites(self.animation_keys_red_down)
                self.rect.y += self.speed
            elif self.move_left == True:
                self.load_animation_sprites(self.animation_keys_red_left)
                self.rect.x -= self.speed
            elif self.move_up == True:
                self.load_animation_sprites(self.animation_keys_red_up)
                self.rect.y -= self.speed
        elif self.ghost_color == "Pink":
            if self.move_right == True:
                self.load_animation_sprites(self.animation_keys_pink_right)
                self.rect.x += self.speed
            elif self.move_down == True:
                self.load_animation_sprites(self.animation_keys_pink_down)
                self.rect.y += self.speed
            elif self.move_left == True:
                self.load_animation_sprites(self.animation_keys_pink_left)
                self.rect.x -= self.speed
            elif self.move_up == True:
                self.load_animation_sprites(self.animation_keys_pink_up)
                self.rect.y -= self.speed
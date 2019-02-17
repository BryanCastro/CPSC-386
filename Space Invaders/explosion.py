from settings import Settings


class Explosion():

    def __init__(self, sprite_sheet, screen):
        self.rect = None
        self.screen = screen
        self.fps = Settings.fps

        # Explosion Sprite Info
        self.explosion_done = False
        self.sprite_sheet = sprite_sheet
        self.explosion_index = [15, 16, 18, 19]
        self.explosion_start_index = 0
        self.frame_count = len(self.explosion_index)
        self.frame_counter = 0

    def draw_explosion(self):
        self.screen.blit(self.sprite_sheet.sheet, self.rect,
                         self.sprite_sheet.cell_list[self.explosion_index[self.explosion_start_index]])

        #if self.frame_counter % (self.fps / self.frame_count-2) == 0:
        if self.explosion_start_index == 3:
            self.explosion_done = True
        else:
            self.explosion_start_index += 1

        #self.frame_counter += 1
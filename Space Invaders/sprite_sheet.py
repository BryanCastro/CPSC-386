import pygame


class SpriteSheet:

    def __init__(self, filename, rows, cols):
        self.cols = cols
        self.rows = rows
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.total_cell_count = cols * rows
        self.rect = self.sheet.get_rect()
        self.cell_width = self.rect.width / cols
        self.cell_height = self.rect.height / rows
        self.cell_list = list([(index % cols * self.cell_width, int(index / cols) * self.cell_height,
                                self.cell_width, self.cell_height) for index in range(self.total_cell_count)])

    def sprite_sheet_log(self):
        for list in self.cell_list:
            print(list)


import pygame
from text import Text
from high_scores import High_Scores

class High_Scores_Screen:

    def __init__(self, screen):
        self.screen = screen
        self.screen_area = screen.get_rect()
        self.high_scores = High_Scores()
        self.scores_title = Text(screen, "HIGH SCORES", (0, 255, 0), (0, 0, 0),
                                    self.screen_area.w, self.screen_area.h, 100)
        self.set_text_position_menu(self.scores_title, 4, 6, 100)
        self.backspace_text = Text(screen, "Press Backspace To Return", (0, 255, 0), (0, 0, 0),
                                   self.screen_area.w, self.screen_area.h, 30)
        self.set_text_position_menu(self.backspace_text, 4, 6, 200, 80)
        self.scores_txt = []
        self.y = 250

        self.position_scores()

    def position_scores(self):

        self.y = 250

        self.scores_txt.clear()
        self.high_scores.score_list.clear()

        self.high_scores.update_scores()

        for line in self.high_scores.score_list:
            self.scores_txt.append(Text(self.screen, str(line), (255, 255, 255), (0, 0, 0),
                                        self.screen_area.w, self.y, 48))
            self.y += 50


        for line in self.scores_txt:
            self.set_text_position_menu(line, 2, 1, -100, 0)


    def set_text_position_menu(self, textObj, x_div, y_div, x_offset = 0, y_offset = 0):
        textObj.textrect.x = (textObj.textrect.x / x_div) + x_offset
        textObj.textrect.y = (textObj.textrect.y / y_div) + y_offset

    def draw_high_scores(self):
        self.scores_title.display_text()
        self.backspace_text.display_text()

        print(len(self.scores_txt))

        for line in self.scores_txt:
            line.display_text()

        pygame.display.update()

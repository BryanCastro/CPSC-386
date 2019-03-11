import pygame

class Sound():

    def __init__(self, sound_effect, is_music = False, is_effect= False):
        self.is_music = is_music
        self.is_effect = is_effect
        self.sound_effect = sound_effect

        if is_effect:
            self.effect = pygame.mixer.Sound(self.sound_effect)



    def play_music(self):
        pygame.mixer.music.load(self.sound_effect)
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_sound(self):
        self.effect.play
import pygame

class Sounds:

    def __init__(self, sound_destination):
        pygame.mixer.init()
        self.sound_destination = sound_destination

    def play_music(self):
        pygame.mixer.music.load(self.sound_destination)
        pygame.mixer.music.play()

    def play_sound(self, channel_num):
        pygame.mixer.Channel(channel_num).play(pygame.mixer.Sound(self.sound_destination))
import os
import random
import pygame
import threading

class SoundPlayer:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        pygame.mixer.init()

    def pick_random_sound(self):
        files = [f for f in os.listdir(self.folder_path) if f.endswith('.wav')]

        if not files:
            print("No .wav files found in: " + self.folder_path)
            return None

        return os.path.join(self.folder_path, random.choice(files))

    def play(self, sound_file):
        if sound_file is None:
            return

        def _play():
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()

        thread = threading.Thread(target=_play)
        thread.daemon = True
        thread.start()
        
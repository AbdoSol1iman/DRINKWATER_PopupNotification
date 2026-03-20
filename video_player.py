import os
import random
import vlc

class VideoPlayer:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.instance = vlc.Instance()

    def pick_random_video(self):
        files = [f for f in os.listdir(self.folder_path) if f.endswith('.mp4')]

        if not files:
            print("No .mp4 files found in: " + self.folder_path)
            return None

        return os.path.join(self.folder_path, random.choice(files))

    def play(self, video_file):
        if video_file is None:
            return

        media = self.instance.media_new(video_file)
        player = self.instance.media_player_new()
        player.set_media(media)
        player.play()
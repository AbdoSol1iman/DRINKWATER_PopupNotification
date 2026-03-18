import threading
import os
from sound_player import SoundPlayer
from notification_manager import NotificationManager

class SoundService:
    def __init__(self, folder_path, sound_gif_map, interval_minutes=10):
        self.player = SoundPlayer(folder_path)
        self.notification = NotificationManager()
        self.sound_gif_map = sound_gif_map
        self.interval_seconds = interval_minutes * 60
        self.timer = None

    def start(self):
        sound_path = self.player.pick_random_sound()

        if sound_path:
            sound_name = os.path.basename(sound_path)
            gif_path = self.sound_gif_map.get(sound_name, None)
            print("Playing: " + sound_name)

            self.notification.show(sound_name, gif_path)
        
            import time
            time.sleep(1)
        
            self.player.play(sound_path)

        self._schedule_next()
        
    def _schedule_next(self):
        self.timer = threading.Timer(self.interval_seconds, self.start)
        self.timer.daemon = True
        self.timer.start()

    def stop(self):
        if self.timer is not None:
            self.timer.cancel()
        print("Service stopped.")
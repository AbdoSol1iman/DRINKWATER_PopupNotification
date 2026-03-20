import threading
import os
from video_player import VideoPlayer
from notification_manager import NotificationManager

class SoundService:
    def __init__(self, folder_path, interval_minutes=10):
        self.player = VideoPlayer(folder_path)
        self.notification = NotificationManager()
        self.interval_seconds = interval_minutes * 60
        self.timer = None

    def start(self):
        video_path = self.player.pick_random_video()

        if video_path:
            video_name = os.path.basename(video_path)
            print("Playing: " + video_name)
            self.notification.show(video_path)

        self._schedule_next()

    def _schedule_next(self):
        self.timer = threading.Timer(self.interval_seconds, self.start)
        self.timer.daemon = True
        self.timer.start()

    def stop(self):
        if self.timer is not None:
            self.timer.cancel()
        print("Service stopped.")
    

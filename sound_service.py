import threading
import os
from video_player import VideoPlayer
from notification_manager import NotificationManager


class SoundService:
    def __init__(self, folder_path, interval_minutes: int = 30):
        self.player = VideoPlayer(folder_path)
        self.stop_event = threading.Event()
        self.notification = NotificationManager(self.stop_event)
        self.interval_seconds = interval_minutes * 60
        self._worker_thread: threading.Thread | None = None

    def start(self) -> None:
        """Start the background worker loop if not already running."""
        if self._worker_thread is not None and self._worker_thread.is_alive():
            return

        self.stop_event.clear()
        self._worker_thread = threading.Thread(target=self._run_loop, daemon=True)
        self._worker_thread.start()

    def _run_loop(self) -> None:
        """Worker loop: pick a video, play it fully, then wait for the next interval."""
        while not self.stop_event.is_set():
            video_path = self.player.pick_random_video()

            if video_path:
                video_name = os.path.basename(video_path)
                print("Playing: " + video_name)
                self.notification.show(video_path)

            # Wait for the next interval, but wake early if stopping.
            if self.stop_event.wait(self.interval_seconds):
                break

    def stop(self) -> None:
        """Request service shutdown and wait briefly for the worker to exit."""
        self.stop_event.set()
        self.notification.stop()

        if self._worker_thread is not None:
            self._worker_thread.join(timeout=5)
            self._worker_thread = None

        print("Service stopped.")

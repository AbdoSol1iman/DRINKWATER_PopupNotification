import tkinter as tk
import vlc
import threading
import time

class NotificationManager:
    def __init__(self):
        pass

    def show(self, video_file):
        thread = threading.Thread(target=self._play_video, args=(video_file,))
        thread.daemon = True
        thread.start()
        pass
    

    def _play_video(self, video_file):
        if video_file is None:
            print("No video file provided")
            return

        root = tk.Tk()
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        root.destroy()

        POPUP_W = 420
        POPUP_H = 300
        x = screen_w - POPUP_W - 20
        y = 20
        instance = vlc.Instance(
            '--no-xlib',
            '--quiet',
            f'--width={POPUP_W}',
            f'--height={POPUP_H}',
            f'--video-x={x}',
            f'--video-y={y}',
            '--no-video-deco',     
        )
        player = instance.media_player_new()
        media = instance.media_new(video_file)
        player.set_media(media)
        player.play()

        time.sleep(10)

        player.stop()
        player.release()
        instance.release()

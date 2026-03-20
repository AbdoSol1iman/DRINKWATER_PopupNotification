import tkinter as tk
import vlc
import threading

class NotificationManager:
    def __init__(self):
        pass

    def show(self, video_file):
        ready = threading.Event()
        thread = threading.Thread(target=self._show_popup, args=(video_file, ready))
        thread.daemon = True
        thread.start()
        ready.wait()

    def _show_popup(self, video_file, ready):
        if video_file is None:
            print("No video file provided")
            ready.set()
            return

        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes('-alpha', 0.0)
        root.configure(bg='black')

        POPUP_W = 420
        POPUP_H = 300

        root.update_idletasks()
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        x = screen_w - POPUP_W - 20
        y = screen_h - POPUP_H - 50
        root.geometry(f'{POPUP_W}x{POPUP_H}+{x}+{y}')

        video_frame = tk.Frame(root, bg='black', width=POPUP_W, height=POPUP_H)
        video_frame.pack()

        instance = vlc.Instance()
        player = instance.media_player_new()
        media = instance.media_new(video_file)
        player.set_media(media)

        root.update()
        player.set_xwindow(video_frame.winfo_id()) 

        player.play()

        ready.set()

        self._fade_in(root)

        root.after(10000, lambda: self._fade_out(root, player))

        root.mainloop()

    def _fade_in(self, window, opacity=0.0):
        if opacity < 1.0:
            window.attributes('-alpha', opacity)
            window.after(30, lambda: self._fade_in(window, round(opacity + 0.1, 1)))
        else:
            window.attributes('-alpha', 1.0)

    def _fade_out(self, window, player, opacity=1.0):
        if opacity > 0.0:
            window.attributes('-alpha', opacity)
            window.after(30, lambda: self._fade_out(window, player, round(opacity - 0.1, 1)))
        else:
            player.stop()
            window.destroy()

    def _animate_gif(self, label, frames, index):
        frame = frames[index]
        label.configure(image=frame)
        label.image = frame
        next_index = (index + 1) % len(frames)
        label.after(50, lambda: self._animate_gif(label, frames, next_index))

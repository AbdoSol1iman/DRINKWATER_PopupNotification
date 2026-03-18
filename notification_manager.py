import tkinter as tk
from PIL import Image, ImageTk
import threading

class NotificationManager:
    def __init__(self):
        pass

    def show(self, sound_file_name, gif_path):
        ready = threading.Event()
        thread = threading.Thread(target=self._show_popup, args=(sound_file_name, gif_path, ready))
        thread.daemon = True
        thread.start()
        ready.wait()

    def _show_popup(self, sound_file_name, gif_path, ready):
        if gif_path is None:
            print("No GIF mapped for: " + sound_file_name)
            ready.set()
            return

        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes('-alpha', 0.0)
        root.configure(bg='#1e1e1e')

        POPUP_W = 420
        POPUP_H = 300

        gif = Image.open(gif_path)
        frames = []
        try:
            while True:
                frame = gif.copy().resize((400, 300))
                frames.append(ImageTk.PhotoImage(frame))
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

        gif_label = tk.Label(root, bg='#1e1e1e')
        gif_label.pack(padx=10, pady=(10, 5))


        # Position at bottom-right
        root.update_idletasks()
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        win_w = root.winfo_width()
        win_h = root.winfo_height()
        x = screen_w - POPUP_W - 20
        y = screen_h - POPUP_H - 50
        root.geometry(f'{POPUP_W}x{POPUP_H}+{x}+{y}')
        
        self._animate_gif(gif_label, frames, 0)

        ready.set()

        self._fade_in(root)
        root.after(10000, lambda: self._fade_out(root))

        root.mainloop()

    def _fade_in(self, window, opacity=0.0):
        if opacity < 1.0:
            window.attributes('-alpha', opacity)
            window.after(30, lambda: self._fade_in(window, round(opacity + 0.1, 1)))
        else:
            window.attributes('-alpha', 1.0)

    def _fade_out(self, window, opacity=1.0):
        if opacity > 0.0:
            window.attributes('-alpha', opacity)
            window.after(30, lambda: self._fade_out(window, round(opacity - 0.1, 1)))
        else:
            window.destroy()

    def _animate_gif(self, label, frames, index):
        frame = frames[index]
        label.configure(image=frame)
        label.image = frame
        next_index = (index + 1) % len(frames)
        label.after(50, lambda: self._animate_gif(label, frames, next_index))
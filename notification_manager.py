import tkinter as tk
import vlc
import threading
import time


class NotificationManager:
    def __init__(self, stop_event: threading.Event | None = None):
        # Shared stop event so playback can react to service shutdown.
        self.stop_event = stop_event or threading.Event()
        self._current_player = None
        self._current_instance = None

    def show(self, video_file: str | None) -> None:
        """Play a single video notification to completion (blocking)."""
        self._play_video(video_file)

    def stop(self) -> None:
        """Request playback stop and clean up the current VLC player."""
        self.stop_event.set()
        if self._current_player is not None:
            try:
                self._current_player.stop()
            except Exception:
                pass
        if self._current_player is not None:
            try:
                self._current_player.release()
            except Exception:
                pass
        if self._current_instance is not None:
            try:
                self._current_instance.release()
            except Exception:
                pass
        self._current_player = None
        self._current_instance = None

    def _play_video(self, video_file: str | None) -> None:
        if video_file is None:
            print("No video file provided")
            return

        if self.stop_event.is_set():
            return

        # Get screen size using Tk, then destroy the root reliably.
        try:
            root = tk.Tk()
            root.withdraw()
            screen_w = root.winfo_screenwidth()
            screen_h = root.winfo_screenheight()
        except Exception as exc:
            print(f"Failed to get screen size via Tk: {exc}")
            return
        finally:
            try:
                root.destroy()
            except Exception:
                pass

        POPUP_W = 420
        POPUP_H = 300
        x = screen_w - POPUP_W - 20
        y = 20

        instance = None
        player = None
        try:
            instance = vlc.Instance(
                "--no-xlib",
                "--quiet",
                f"--width={POPUP_W}",
                f"--height={POPUP_H}",
                f"--video-x={x}",
                f"--video-y={y}",
                "--no-video-deco",
                "--no-video-title-show",
            )
            player = instance.media_player_new()
            media = instance.media_new(video_file)
            player.set_media(media)

            self._current_instance = instance
            self._current_player = player

            player.play()

            # Wait for full video playback, or until stopped, with a safety timeout.
            max_wait_seconds = 15 * 60
            start = time.time()

            while not self.stop_event.is_set():
                state = player.get_state()
                if state in (vlc.State.Ended, vlc.State.Stopped, vlc.State.Error):
                    break

                if time.time() - start > max_wait_seconds:
                    print("Stopping playback due to max duration timeout.")
                    break

                time.sleep(0.5)
        except Exception as exc:
            print(f"Error during video playback: {exc}")
        finally:
            if player is not None:
                try:
                    player.stop()
                except Exception:
                    pass
                try:
                    player.release()
                except Exception:
                    pass
            if instance is not None:
                try:
                    instance.release()
                except Exception:
                    pass
            self._current_player = None
            self._current_instance = None

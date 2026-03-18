# DRINKWATER_PopupNotification
# DrinkWater - Popup Notification

A lightweight background service that plays a random sound and displays an animated GIF popup notification at a set interval. Built to remind you to drink water, take a break, or anything else you want to be reminded of.

---

## How It Works

Every 10 minutes (configurable), the service picks a random `.wav` file from your `sounds/` folder, plays it, and shows an animated GIF popup in the bottom-right corner of your screen. The popup fades in, stays for 10 seconds, then fades out automatically.

---

## Project Structure

```
DrinkWater-PopupNotification/
├── main.py
├── sound_service.py
├── sound_player.py
├── notification_manager.py
├── sounds/
│   └── your_sound.wav
└── assets/
    └── your_animation.gif
```

---

## Requirements

### Python Version

Python 3.10 or higher.

### System Dependencies

**On Debian / Ubuntu:**
```bash
sudo apt install python3-tk python3-pygame
```

**On Windows:**

No system dependencies needed. Just install the Python packages below.

### Python Packages

```bash
pip install Pillow pygame
```

---

## Setup

**1. Clone the repository:**
```bash
git clone https://github.com/your-username/DrinkWater-PopupNotification.git
cd DrinkWater-PopupNotification
```

**2. Install dependencies:**
```bash
pip install Pillow pygame
```

**3. Add your files:**

- Put your `.wav` sound files inside the `sounds/` folder
- Put your `.gif` animation files inside the `assets/` folder

**4. Edit `main.py` to map each sound to its GIF:**

```python
SOUND_GIF_MAP = {
    "your_sound.wav" : os.path.join(BASE_DIR, "assets", "your_animation.gif"),
}
```

The key is the sound file name (without the full path), and the value is the full path to the GIF.

**5. Set your preferred interval in `main.py`:**

```python
service = SoundService(SOUNDS_FOLDER, SOUND_GIF_MAP, interval_minutes=10)
```

---

## Running the Service

### Run Manually

```bash
python3 main.py
```

To stop it, press `Ctrl + C`.

---

## Running in the Background on Linux (systemd)

This makes the service start automatically when you log in.

**1. Create the service file:**
```bash
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/drinkwater.service
```

**2. Paste the following, replacing the path and username with yours:**
```ini
[Unit]
Description=DrinkWater Popup Notification
After=graphical-session.target

[Service]
ExecStart=/usr/bin/python3 /full/path/to/DrinkWater-PopupNotification/main.py
Restart=always
RestartSec=5
Environment=DISPLAY=:0
Environment=XAUTHORITY=%h/.Xauthority
Environment=PULSE_SERVER=unix:/run/user/%U/pulse/native

[Install]
WantedBy=default.target
```

**3. Enable and start the service:**
```bash
systemctl --user daemon-reload
systemctl --user enable drinkwater
systemctl --user start drinkwater
```

**4. Check that it is running:**
```bash
systemctl --user status drinkwater
```

### Useful Commands

```bash
# Stop the service
systemctl --user stop drinkwater

# Start the service
systemctl --user start drinkwater

# Disable auto-start on login
systemctl --user disable drinkwater

# View logs
journalctl --user -u drinkwater -n 50
```

---

## Running in the Background on Windows (Task Scheduler)

This makes the service start automatically when you log in.

**1. Open Task Scheduler** from the Start menu.

**2. Click "Create Basic Task" and fill in the following:**

- Name: DrinkWater
- Trigger: When I log on
- Action: Start a program
- Program: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\pythonw.exe`
- Arguments: `"C:\full\path\to\DrinkWater-PopupNotification\main.py"`

Use `pythonw.exe` instead of `python.exe` to run without a console window.

**3. Click Finish.**

The service will now start silently every time you log into Windows.

To stop it, open Task Manager, find the `pythonw.exe` process, and end it.

---

## Configuration

All configuration is at the top of `main.py`:

| Variable | Description |
|---|---|
| `SOUNDS_FOLDER` | Path to folder containing `.wav` files |
| `SOUND_GIF_MAP` | Maps each sound file name to a GIF file path |
| `interval_minutes` | How often to play a sound (default: 10) |

---

## Notes

- Only `.wav` audio files are supported.
- The popup appears in the bottom-right corner and auto-dismisses after 10 seconds.
- On Linux with GNOME, make sure PulseAudio or PipeWire is running before the service starts.
- The project uses relative paths, so it works on any machine without changing the code as long as the folder structure is preserved.

# DrinkWater - Popup Notification

A lightweight background service that plays a random video popup notification at a set interval. Built to remind you to drink water, take a break, or anything else you want to be reminded of.

---

## How It Works

Every 10 minutes (configurable), the service picks a random `.mp4` file from your `videos/` folder and plays it in a popup window in the bottom-right corner of your screen. The popup fades in, stays for 10 seconds, then fades out automatically.

---

## Project Structure

```
DrinkWater-PopupNotification/
├── main.py
├── sound_service.py
├── video_player.py
├── notification_manager.py
└── videos/
    └── your_video.mp4
```

---

## Requirements

### Python Version

Python 3.10 or higher.

### System Dependencies

**On Debian / Ubuntu:**
```bash
sudo apt install python3-tk vlc
```

**On Windows:**

Install VLC from https://www.videolan.org/vlc then install the Python packages below.

### Python Packages

```bash
pip install python-vlc
```

---

## Media Files

The `videos/` folder is not included in the repository due to file size.

Download `media.zip` from the [Releases](../../releases) section, then extract it in the project folder:

```bash
unzip media.zip
```

This will create the `videos/` folder with all required files automatically.

Alternatively, you can use your own `.mp4` files by placing them inside the `videos/` folder.

---

## Setup

**1. Clone the repository:**
```bash
git clone https://github.com/AbdoSol1iman/DRINKWATER_PopupNotification.git
cd DRINKWATER_PopupNotification
```

**2. Install dependencies:**
```bash
sudo apt install vlc
pip install python-vlc
```

**3. Download and extract media files from the Releases section:**
```bash
unzip media.zip
```

**4. Set your preferred interval in `main.py`:**

```python
service = SoundService(VIDEOS_FOLDER, interval_minutes=10)
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

**2. Paste the following, replacing the path with yours:**
```ini
[Unit]
Description=DrinkWater Popup Notification
After=graphical-session.target

[Service]
ExecStart=/usr/bin/python3 /full/path/to/DRINKWATER_PopupNotification/main.py
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
- Arguments: `"C:\full\path\to\DRINKWATER_PopupNotification\main.py"`

Use `pythonw.exe` instead of `python.exe` to run without a console window.

**3. Click Finish.**

The service will now start silently every time you log into Windows.

To stop it, open Task Manager, find the `pythonw.exe` process, and end it.

---

## Configuration

All configuration is at the top of `main.py`:

| Variable | Description |
|---|---|
| `VIDEOS_FOLDER` | Path to folder containing `.mp4` files |
| `interval_minutes` | How often to show a notification (default: 10) |

---

## Notes

- Only `.mp4` video files are supported.
- The popup appears in the bottom-right corner and auto-dismisses after 10 seconds.
- On Linux with GNOME, make sure PulseAudio or PipeWire is running before the service starts.
- The project uses relative paths, so it works on any machine without changing the code as long as the folder structure is preserved.

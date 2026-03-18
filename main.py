import os
import signal
import sys
import time
from sound_service import SoundService

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SOUNDS_FOLDER = os.path.join(BASE_DIR, "sounds")

SOUND_GIF_MAP = {
    "Facebook(1).wav" : os.path.join(BASE_DIR, "assets", "Facebook(1).gif"),
    "Facebook(2).wav" : os.path.join(BASE_DIR, "assets", "Facebook(2).gif"),
    "Facebook(4).wav" : os.path.join(BASE_DIR, "assets", "Facebook(4).gif"),
    "Facebook(5).wav" : os.path.join(BASE_DIR, "assets", "Facebook(5).gif"),
    "Facebook(6).wav" : os.path.join(BASE_DIR, "assets", "Facebook(6).gif"),
    "Facebook(7).wav" : os.path.join(BASE_DIR, "assets", "Facebook(7).gif"),
}

service = SoundService(SOUNDS_FOLDER, SOUND_GIF_MAP, interval_minutes=10)

def handle_stop(sig, frame):
    service.stop()
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_stop)
signal.signal(signal.SIGINT, handle_stop)

service.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    service.stop()
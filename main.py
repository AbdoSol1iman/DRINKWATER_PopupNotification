import os
import signal
import sys
import time
from sound_service import SoundService

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_FOLDER = os.path.join(BASE_DIR, "videos")

service = SoundService(VIDEOS_FOLDER, interval_minutes=10)

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

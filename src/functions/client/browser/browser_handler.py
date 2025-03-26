import webbrowser
from datetime import datetime
from src.core.constants import (
    TIMING,
    EMULATOR
)

class BrowserHandler:
    def __init__(self, emulator=None):
        self.last_link_time = None
        self.emulator = emulator

    def can_open_link(self):
        if TIMING["overlapping"]:
            return True

        current_time = datetime.now()
        if self.last_link_time is None:
            self.last_link_time = current_time
            return True

        time_diff = (current_time - self.last_link_time).total_seconds()
        if time_diff >= TIMING["link_timer"]:
            self.last_link_time = current_time
            return True
        return False

    def open_url(self, url):
        if self.can_open_link():
            try:
                if EMULATOR["use_emulator"] and self.emulator:
                    return self.emulator.open_url_in_emulator(url)
                else:
                    webbrowser.open(url)
                    print(f"successfully opened URL: {url}")
                return True
            except Exception as e:
                print(f"error opening the URL: {e}")
                return False
        else:
            print(f"please wait {TIMING['link_timer']} seconds between opening links")
            return False
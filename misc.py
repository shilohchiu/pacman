"""
helper functions
"""

import time

class Countdown:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = 0
        self.is_running = False

    def start_timer(self):
        self.start_time = time.time()
        self.is_running = True

    def stop_timer(self):
        self.is_running = False

    def get_time_passed(self):
        if self.is_running:
            return time.time() - self.start_time
        return 0

    def timer_complete(self):
        return self.get_time_passed() >= self.duration

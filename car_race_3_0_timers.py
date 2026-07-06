import pygame
import random
from datetime import datetime

from car_race_3_0_config import GANTRY_DISPLAY_SIZE, TIMER_DISPLAY_SIZE, time_font, get_resource_path

class GantryTimer:
    TIMER_EVENT = pygame.USEREVENT + 1

    def __init__(self):
        # Load your 7 frame states (0 = all off, 1-5 = lights filling up, 6 = holding)
        self.images = [
            pygame.transform.scale(
                pygame.image.load(get_resource_path(f"resources/assets/gantry_{i}.png")), 
                GANTRY_DISPLAY_SIZE
            ).convert_alpha()
            for i in range(7)
        ]

        self.state = 0
        self.is_counting_down = False
        self.race_started = False

    def start(self):
        """Initializes and begins the F1 countdown sequence."""
        self.state = 0
        self.is_counting_down = True
        self.race_started = False
        pygame.time.set_timer(GantryTimer.TIMER_EVENT, 1000)

    def handle_event(self, event):
        """Processes the timer ticks. Call this inside your main event loop."""
        if event.type == GantryTimer.TIMER_EVENT:
            if self.state < 4: # Turn on lights one by one (States 0, 1, 2, 3)
                self.state += 1
            elif self.state == 4: # All lamps on for random time
                self.state = 5
                random_delay = int(random.uniform(200, 3000))
                pygame.time.set_timer(GantryTimer.TIMER_EVENT, random_delay)
            elif self.state == 5: # Race starts
                self.state = 0
                self.is_counting_down = False
                self.race_started = True
                
                # Turn off the gantry timer completely
                pygame.time.set_timer(GantryTimer.TIMER_EVENT, 0)

    def paint(self, surface):
        """Renders the gantry centered horizontally on the screen."""
        if self.is_counting_down or not self.race_started:
            img = self.images[self.state]
            x = (surface.get_width() // 2) - (img.get_width() // 2)
            surface.blit(img, (x, 200))

class RaceTimer:
    def __init__(self):
        self.start_time = None
        self.final_time_str = "00:00"
        self.is_running = False

        self.timer_image = pygame.image.load(get_resource_path("resources/assets/timer_watch.png")).convert()
        self.timer_image = pygame.transform.scale(self.timer_image, TIMER_DISPLAY_SIZE)
        self.timer_image.set_colorkey((255,255,255))

    def start(self):
        """Starts or resets the race clock."""
        self.start_time = datetime.now()
        self.is_running = True
        self.final_time_str = "00:00"

    def stop(self):
        """Freezes the clock (call this when a player wins)."""
        if self.is_running:
            self.final_time_str = self.get_time_string()
            self.is_running = False

    def reset(self):
        """Clears the clock entirely back to zero."""
        self.start_time = None
        self.is_running = False
        self.final_time_str = "00:00"

    def get_time_string(self):
        """Calculates elapsed time and returns it as an MM:SS string."""
        if not self.start_time:
            return "00:00"
        
        # If the race is over, return the cached final time
        if not self.is_running:
            return self.final_time_str

        elapsed = datetime.now() - self.start_time
        total_seconds = int(elapsed.total_seconds())
        
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        
        return f"{minutes:02d}:{seconds:02d}"

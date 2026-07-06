import time
import math
import pygame
import numpy as np

from car_race_3_0_config import (
    CAR_POS, DISPLAY_POS, FINISH_LINE_RECT, HALF_LAP_RECT, MAX_LAPS,
    RUNTIME_DISPLAY_SIZE,
    ui_font,
    get_resource_path
)

class Player(object):
    """
    Ein einfaches Spieler-Objekt. Es beinhaltet ein Bild für den Spieler
    sowie eine aktuelle Position
    """    
    def __init__(self, player, car_stats, mask_track, mask_fence):
        self.pos = list(CAR_POS[player])
        
        self.name = player
        self.car = car_stats["car_name"]
        self.display = self._load_image(car_stats["car_display"])
        self.display = pygame.transform.scale(self.display, RUNTIME_DISPLAY_SIZE)

        self.original = self._load_image(car_stats["car_image"])
        self.image = self.original

        self.mask_track = mask_track
        self.mask_fence = mask_fence
        self.mask = pygame.mask.from_surface(self.image)

        self.angle = 0
        self.speed = 0
        self.laps = 0
        self.race_time = 0
        self.lap_time = 0
        self.fastest_lap_time = np.inf
        self.starting_lap = True
        self.crossed_finish_last_frame = False
        self.did_full_lap = False

        self.max_speed = car_stats["max_speed"]
        self.accel = car_stats["accel"]
        self.turning_speed = car_stats["turning"]
        self.braking = car_stats["braking"]
        
    def _load_image(self, path):
        image = pygame.image.load(get_resource_path(path)).convert()
        new_width = int(image.get_width() * 0.3)
        new_height = int(image.get_height() * 0.3)
        image = pygame.transform.smoothscale(image, (new_width, new_height))
        image.set_colorkey((0,0,0))
        return image
    
    def paint(self, surface: pygame.Surface):
        image_cx = self.image.get_width() // 2
        image_cy = self.image.get_height() // 2

        # Paint the Car
        surface.blit(self.image, (self.pos[0] - image_cx, self.pos[1] - image_cy))

        # Paint the player display background
        surface.blit(self.display, (DISPLAY_POS[self.name][0], DISPLAY_POS[self.name][1]))

        # Paint the player display text
        lap_txt = f"{self.name} Laps: {self.laps} / {MAX_LAPS}".title()
        name_txt = self.car
        lap_surf = ui_font.render(lap_txt, True, (0, 0, 0))
        name_surf = ui_font.render(name_txt, True, (0, 0, 0))
        surface.blit(lap_surf, (DISPLAY_POS[self.name][0]+30, DISPLAY_POS[self.name][1]+10))
        surface.blit(name_surf, (DISPLAY_POS[self.name][0]+130, DISPLAY_POS[self.name][1]+55))

    def turn_left(self):
        speed_ratio = self.speed / self.max_speed
        handling_factor = 1.0 - (speed_ratio * 0.5)
        self.angle += self.turning_speed * handling_factor
        self.update_rotation()

    def turn_right(self):
        speed_ratio = self.speed / self.max_speed
        handling_factor = 1.0 - (speed_ratio * 0.5)
        self.angle -= self.turning_speed * handling_factor
        self.update_rotation()

    def update_rotation(self):
        winkel_in_grad = 360 / (2 * math.pi) * self.angle
        self.image = pygame.transform.rotate(self.original, winkel_in_grad)
        self.mask = pygame.mask.from_surface(self.image)

    def drive(self):
        self.speed += self.accel
        if self.speed > self.max_speed:
            self.speed = self.max_speed

    def brake(self):
        self.speed *= self.braking

    def roll_out(self):
        self.speed *= 0.99

    def apply_physics(self):
        old_x = self.pos[0]
        old_y = self.pos[1]
        
        started_in_wall, _ = self.check_collisions()

        # Calculate proposed movement steps
        move_x = math.cos(self.angle) * self.speed
        move_y = -math.sin(self.angle) * self.speed

        # --- X-AXIS ---
        self.pos[0] += move_x
        hit_fence_x, _ = self.check_collisions()
        
        if hit_fence_x and not (started_in_wall and not hit_fence_x):
            self.pos[0] = old_x

        # --- Y-AXIS ---
        self.pos[1] += move_y
        hit_fence_y, _ = self.check_collisions()
        
        if hit_fence_y and not (started_in_wall and not hit_fence_y):
            self.pos[1] = old_y

        # --- GRASS SLOWDOWN ---
        _, hit_grass = self.check_collisions()
        if hit_grass:
            self.speed *= 0.85 
            if self.speed > 1.5:
                self.speed = 1.5

        if abs(self.speed) < 0.1:
            self.speed = 0

    def check_collisions(self, mask_offset_x=278, mask_offset_y=280):
        """
        Returns a tuple: (hit_fence, hit_grass)
        """
        car_x = self.pos[0] - self.image.get_width() / 2
        car_y = self.pos[1] - self.image.get_height() / 2
        
        offset_x = int(car_x - mask_offset_x)
        offset_y = int(car_y - mask_offset_y)
        
        hit_fence = self.mask_fence.overlap(self.mask, (offset_x, offset_y)) is not None
        hit_grass = self.mask_track.overlap(self.mask, (offset_x, offset_y)) is not None
        
        return hit_fence, hit_grass

    def check_lap_conditions(self):
        car_rect = pygame.Rect(self.pos[0] - 10, self.pos[1] - 10, 20, 20)

        if car_rect.colliderect(HALF_LAP_RECT):
            self.did_full_lap = True

        if car_rect.colliderect(FINISH_LINE_RECT):
            if ((not self.crossed_finish_last_frame) or (not self.starting_lap)) and self.did_full_lap:
                self.compute_fastest_lap_time()
                self.crossed_finish_last_frame = True
            else:
                self.starting_lap = False
        else:
            self.crossed_finish_last_frame = False
    
    def compute_fastest_lap_time(self):
        self.laps += 1
        self.crossed_finish_last_frame = True
        self.did_full_lap = False
        now = time.time()

        if self.lap_time == 0:
            self.lap_time = now
            return
        
        current_lap_time = now - self.lap_time 

        if current_lap_time < self.fastest_lap_time:
            self.fastest_lap_time = current_lap_time

        self.lap_time = now

    def reset_race(self):
        self.pos[0] = CAR_POS[self.name][0]
        self.pos[1] = CAR_POS[self.name][1]
        self.angle = 0
        self.speed = 0
        self.laps = 0
        self.update_rotation()
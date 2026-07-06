import pygame
import numpy as np

from car_race_3_0_config import (
    MAX_LAPS,
    WINNER_DISPLAY_SIZE,
    time_font, restart_font, victory_font, second_font,
    get_resource_path
)

from car_race_3_0_player import Player
from car_race_3_0_timers import RaceTimer

def update_race_time_display(surface: pygame.Surface, race_timer: RaceTimer, screen_cx):
    # Timer background image
    overlay_x = screen_cx - race_timer.timer_image.get_width() // 2
    overlay_y = 20
    surface.blit(race_timer.timer_image, (overlay_x, overlay_y))

    # Timer text
    time_str = race_timer.get_time_string()
    time_surface = time_font.render(time_str, True, (255, 0, 0))
    sub_x = screen_cx - time_surface.get_width() // 2
    sub_y = 45
    surface.blit(time_surface, (sub_x, sub_y))

    # Restart race text
    sub_surface = restart_font.render("Press SPACE to restart", True, (0, 0, 0))
    sub_x = screen_cx - sub_surface.get_width() // 2
    sub_y = 150
    surface.blit(sub_surface, (sub_x, sub_y))

def update_winner_display(p1: Player, p2: Player, surface: pygame.Surface, screen_cx, screen_cy):
    # Determine the winner
    winner = "Player 1!" if p1.laps >= MAX_LAPS else "Player 2!"
    second = "Player 2" if p1.laps >= MAX_LAPS else "Player 1"
    fastest_lap = "P1" if p1.fastest_lap_time <= p2.fastest_lap_time else "P2"
    fastest_lap_time = p1.fastest_lap_time if p1.fastest_lap_time <= p2.fastest_lap_time else p2.fastest_lap_time

    winner_display = pygame.image.load(get_resource_path("resources/assets/winner_display.png")).convert()
    winner_display = pygame.transform.scale(winner_display, WINNER_DISPLAY_SIZE)
    winner_display.set_colorkey((0, 0, 0))

    overlay_x = screen_cx - winner_display.get_width() // 2
    overlay_y = screen_cy - winner_display.get_height() // 2
    surface.blit(winner_display, (overlay_x, overlay_y))

    # Create a dark overlay box behind the victory text for readability
    overlay = pygame.Surface((600, 200), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    
    # Render and center victory text inside the overlay box
    vic_surf = victory_font.render(winner, True, (255, 215, 0))
    vic_x = overlay_x  + 300
    vic_y = overlay_y + 250
    surface.blit(vic_surf, (vic_x, vic_y))
    
    # Render and center victory text inside the overlay box
    sec_surf = second_font.render(second, True, (34, 34, 34))
    sec_x = overlay_x  + 300
    sec_y = overlay_y + 370
    surface.blit(sec_surf, (sec_x, sec_y))

    # Render and center victory text inside the overlay box
    if fastest_lap_time == np.inf:
        time_display_str = "No time"
    else:
        time_display_str = f"{fastest_lap_time:.2f}s"

    lap_surf = second_font.render(f"{fastest_lap} with {time_display_str}", True, (34, 34, 34))
    lap_x = overlay_x  + 300
    lap_y = overlay_y + 490
    surface.blit(lap_surf, (lap_x, lap_y))

    # Subtext instruction
    sub_surf = restart_font.render("Press SPACE to restart", True, (0, 0, 0))
    sub_x = screen_cx - sub_surf.get_width() // 2
    sub_y = overlay_y + 650
    surface.blit(sub_surf, (sub_x, sub_y))
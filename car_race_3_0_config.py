import os
import sys

from pygame import Rect, font

# Initialize fonts for UI
font.init()
text_font = font.SysFont("Trebuchet MS", 16)
ui_font = font.SysFont("Trebuchet MS", 30, bold=True)
time_font = font.SysFont("consolas", 60, bold=True, italic=True)
victory_font = font.SysFont("Trebuchet MS", 54, bold=True, italic=True)
second_font = font.SysFont("Trebuchet MS", 48, bold=False, italic=True)
restart_font = font.SysFont("Trebuchet MS", 36, bold=True, italic=True)



CARS = {
    "Porsche": {
        "car_name": "Porsche",
        "car_image": "resources/cars/porsche.png",
        "car_display": "resources/assets/runtime_porsche.png",
        "max_speed": 3.2, "accel": 0.18, "turning": 0.06, "braking": 0.98},
    "Ferrari": {
        "car_name": "Ferrari",
        "car_image": "resources/cars/ferrari.png",
        "car_display": "resources/assets/runtime_ferrari.png",
        "max_speed": 3.2, "accel": 0.2, "turning": 0.05, "braking": 0.97},
    "Lamborghini": {
        "car_name": "Lamborghini",
        "car_image": "resources/cars/lambo.png",
        "car_display": "resources/assets/runtime_lambo.png",
        "max_speed":   3, "accel": 0.16, "turning": 0.06, "braking": 0.97},
    "McLaren": {
        "car_name": "McLaren",
        "car_image": "resources/cars/maclaren.png",
        "car_display": "resources/assets/runtime_maclaren.png",
        "max_speed": 3.5, "accel": 0.16, "turning": 0.045, "braking": 0.96},
}

MAX_STATS = {
    "max_speed":    max(c["max_speed"] for c in CARS.values()),
    "accel":        max(c["accel"] for c in CARS.values()),
    "turning":      max(c["turning"] for c in CARS.values()),
    "braking":      max(c["braking"] for c in CARS.values())
}

CAR_POS = {
    "player1": [393, 666],
    "player2": [393, 693]
}

DISPLAY_POS = {
    "player1": [50, 10],
    "player2": [745, 10]
}
RUNTIME_DISPLAY_SIZE = [400, 100]

GANTRY_DISPLAY_SIZE = [600, 210]

TIMER_DISPLAY_SIZE = [200, 100]

MAX_LAPS = 3

WINNER_DISPLAY_SIZE = [1000, 600]
FINISH_LINE_RECT = Rect(415, 640, 5, 120)
HALF_LAP_RECT = Rect(750, 278, 5, 110)

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
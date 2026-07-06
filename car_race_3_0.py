import pygame

from pygame.locals import *

from car_race_3_0_config import (MAX_LAPS, get_resource_path)

from car_race_3_0_setup import select_cars
from car_race_3_0_player import Player
from car_race_3_0_timers import GantryTimer, RaceTimer
from car_race_3_0_displays import update_race_time_display, update_winner_display

def paint(surface: pygame.surface.Surface):

    screen_cx = surface.get_width() // 2
    screen_cy = surface.get_height() // 2

    surface.blit(stadium_image, (0, 0))
    surface.blit(track_image, (278, 280))
    
    # To visualize, where the hidden checks are a player has to pass
    #pygame.draw.rect(surface, (0, 0, 255), FINISH_LINE_RECT)
    #pygame.draw.rect(surface, (0, 0, 255), HALF_LAP_RECT)

    player1.paint(surface)
    player2.paint(surface)

    update_race_time_display(surface, race_timer, screen_cx)
    
    if player1.laps >= MAX_LAPS or player2.laps >= MAX_LAPS:
        race_timer.stop()
        update_winner_display(player1, player2, surface, screen_cx, screen_cy)

    gantry_timer.paint(surface)

def step(events):
    # Holt eine Liste von allen gedrückten Tasten auf der Tastatur
    pressed = pygame.key.get_pressed()

    if pressed[K_SPACE]:
        player1.reset_race()
        player2.reset_race()
        race_timer.reset()
        if not gantry_timer.is_counting_down:
            gantry_timer.start()
        return

    if not gantry_timer.race_started:
        player1.speed = 0
        player2.speed = 0
        return
    
    # Player 1
    if pressed[K_UP]:
        player1.drive()
    elif pressed[K_DOWN]:
        player1.brake()
    else:
        player1.roll_out()

    player1.apply_physics()

    if pressed[K_LEFT]:
        player1.brake()
        player1.turn_left()
    if pressed[K_RIGHT]:
        player1.brake()
        player1.turn_right()

    # Player 2
    if pressed[K_w]:
        player2.drive()
    elif pressed[K_s]:
        player2.brake()
    else:
        player2.roll_out()

    player2.apply_physics()

    if pressed[K_a]:
        player2.brake()
        player2.turn_left()
    if pressed[K_d]:
        player2.brake()
        player2.turn_right()

    player1.check_lap_conditions()
    player2.check_lap_conditions()

pygame.init()

screenGeometry = (1190,1040)
screen = pygame.display.set_mode(screenGeometry)

img = pygame.image.load(get_resource_path("resources/assets/icon.ico"))
pygame.display.set_icon(img)

track_image = pygame.image.load(get_resource_path("resources/stadium/rennstrecke.png")).convert()
track_image.set_colorkey((255,255,255))

stadium_image = pygame.image.load(get_resource_path("resources/stadium/stadion.png")).convert()
stadium_image = pygame.transform.scale(stadium_image, (int(1195), int(1040)))

# Load the track mask (white = track)
mask_image_track = pygame.image.load(get_resource_path("resources/stadium/rennstrecke_mask_track.png")).convert()
mask_track = pygame.mask.from_threshold(mask_image_track, (0, 0, 0), (30, 30, 30))

# Load the fence mask (white = fences)
mask_image_fence = pygame.image.load(get_resource_path("resources/stadium/rennstrecke_mask_fence.png")).convert()
mask_fence = pygame.mask.from_threshold(mask_image_fence, (255, 255, 255), (30, 30, 30))


# Auswählen der Autos
p1, p2 = select_cars(screen)

# Erstelle ein Spieler-Objekt
player1 = Player("player1", p1, mask_track, mask_fence)
player2 = Player("player2", p2, mask_track, mask_fence)

clock = pygame.time.Clock()

race_timer = RaceTimer()

gantry_timer = GantryTimer()

gantry_timer.start()

wantsToQuit = False

while not wantsToQuit:

    # Schaut nach, ob neue Events eingetroffen sind. Ein
    # Event kann z.B. ein Mausklick, ein Tastendruck oder
    # ein Fenster-Schliessbefehl (QUIT) sein.
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            wantsToQuit = True
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            wantsToQuit = True

        gantry_timer.handle_event(event)

        if event.type == GantryTimer.TIMER_EVENT and gantry_timer.race_started:
            if not race_timer.is_running:
                race_timer.start()

    # Ändert den Zustand des Spiels
    step(events)

    # Ruft die paint-Prozedur auf, welche den aktuellen Zustand
    # auf den Bildschirm zeichnet
    paint(screen)

    # Macht die auf screen gezeichneten Änderungen am
    # Bildschirm sichtbar - ohne das flip() bleibt der
    # Fensterinhalt schwarz
    pygame.display.flip()

    clock.tick(60)

# Sorgt dafür, dass Pygame-Resourcen (z.B. Grafiken usw)
# sauber freigegeben werden
pygame.quit()

    

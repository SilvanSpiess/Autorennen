import os
import sys
import math
import pygame

from pygame.locals import *

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Player(object):
    """
    Ein einfaches Spieler-Objekt. Es beinhaltet ein Bild für den Spieler
    sowie eine aktuelle Position
    """    
    def __init__(self, pos):
        """
        Konstruiert ein Player-Objekt.

        Erwartet die Anfangsposition des Spielers auf dem Bildschirm als
        Argument, und zwar als Liste mit zwei Elementen, der x- und der y-
        Koordinate, also z.B. [50,60].
        """
        self.pos = list(pos)
        self.angle = 0
        self.original = self._load_image(get_resource_path("resources/cars/auto.png"))
        self.image = self.original
        self.speed = 3
        self.counter = 0 # Wie lange der SPieler forwarts gedrückt hat
        self.default_angle_inc = 0.04
        self.default_speed = 2
        

    def _load_image(self, path):
        image = pygame.image.load(path).convert()
        image.set_colorkey((63,72,204))
        return image
   
    
    def paint(self, surface):
        """
        Zeichnet die Spielfigur
        """
        surface.blit(self.image, (self.pos[0] - self.image.get_width() / 2, self.pos[1] - self.image.get_height() / 2))
   

    def turn_left(self):
        """
        Bewegt die Spielfigur nach links
        """
        # 0 ist der index für die x-Koordinate in der [x, y]-Liste.
        # Diese wird um 1 kleiner gemacht
        
        self.angle = self.angle + self.default_angle_inc
        winkel_in_grad = 360 / (2 * math.pi) * self.angle
        self.image = pygame.transform.rotate(self.original, winkel_in_grad)

    def turn_right(self):
        """
        Bewegt die Spielfigur nach rechts
        """
        # 0 ist der index für die x-Koordinate in der [x,y]-Liste
        # Diese wird um 1 grösser gemacht
        self.angle = self.angle - self.default_angle_inc
        winkel_in_grad = 360 / (2 * math.pi) * self.angle
        self.image = pygame.transform.rotate(self.original, winkel_in_grad)
        
 
    def move_forward(self):
        self.pos[1] = self.pos[1] - math.sin(self.angle) * self.speed 
        self.pos[0] = self.pos[0] + math.cos(self.angle) * self.speed 
                             
   
def paint(surface):
    """
    Zeichnet ein Bild auf die angegebene surface ("Leinwand")
    """
    
    surface.blit(frontbackground_image, (0,0))
    surface.blit(background_image,(278,280))

    player1.paint(surface)
    player2.paint(surface)


def step(events):
    """
    Ändert den Zustand des Spiels
    """
    # Holt eine Liste von allen gedrückten Tasten auf der Tastatur
    pressed = pygame.key.get_pressed()

    # LINKS
    if pressed[K_LEFT]:        
        player1.turn_left()

    if pressed[K_a]:        
        player2.turn_left()
        
    # RECHTS
    if pressed[K_RIGHT]:
        player1.turn_right()

    if pressed[K_d]:
        player2.turn_right()

    # VORWÄRTS
    if pressed[K_UP]:
        player1.move_forward()
        player1.counter = player1.counter + 1
    else:
        player1.counter = 0

    if pressed[K_w]:
        player2.move_forward()
        player2.counter = player2.counter + 1
    else:
        player2.counter = 0

    if player2.counter > 4:
        player2.speed = player2.speed + 0.02
        if pressed[K_a] or pressed[K_d]:
           player2.speed = player2.default_speed
    else:
        player2.speed = player2.default_speed

    if player1.counter > 10:
        player1.speed = player1.speed + 0.03
        if pressed[K_RIGHT] or pressed[K_LEFT]:
           player1.speed = player1.default_speed
    else:
        player1.speed = player1.default_speed
    

# Legt die Grösse des Bildschirmfensters in Pixeln fest
screenGeometry = (1190,1040)

# Öffnet ein Grafikfenster mit der angegebenen Gr�sse
# screen ist eine Art "Leinwand" (surface), auf die
# gezeichnet werden kann
screen = pygame.display.set_mode(screenGeometry)

img = pygame.image.load(get_resource_path("resources/assets/icon.ico"))
pygame.display.set_icon(img)

background_image = pygame.image.load(get_resource_path("resources/stadium/rennstrecke.png")).convert()
background_image.set_colorkey((255,255,255))

frontbackground_image = pygame.image.load(get_resource_path("resources/stadium/stadion.png")).convert()

frontbackground_image = pygame.transform.scale(frontbackground_image, (int(1195), int(1040)))

# Erstelle ein Spieler-Objekt
player1 = Player((393,669))
player2 = Player((393,693))

wantsToQuit = False

clock = pygame.time.Clock()

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

    

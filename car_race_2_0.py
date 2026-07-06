import sys
import pygame
import math

from pygame.locals import *

CAR_OPTIONS = [
    "resources/porsche.png",
    "resources/ferrari.png",
    "resources/lambo.png",
    "resources/maclaren.png"
]

class Player(object):
    """
    Ein einfaches Spieler-Objekt. Es beinhaltet ein Bild für den Spieler
    sowie eine aktuelle Position
    """    
    def __init__(self, pos, img_path):
        """
        Konstruiert ein Player-Objekt.

        Erwartet die Anfangsposition des Spielers auf dem Bildschirm als
        Argument, und zwar als Liste mit zwei Elementen, der x- und der y-
        Koordinate, also z.B. [50,60].
        """
        self.pos = list(pos)
        self.angle = 0
        self.original = self._load_image(img_path)
        self.image = self.original
        self.speed = 1
        self.counter = 0
        

    def _load_image(self, path):
        image = pygame.image.load(path).convert()
        new_width = int(image.get_width() * 0.35)
        new_height = int(image.get_height() * 0.35)
        image = pygame.transform.smoothscale(image, (new_width, new_height))
        image.set_colorkey((0,0,0))
        #image.set_colorkey((63,72,204))
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
        
        self.angle = self.angle + 0.09
        winkel_in_grad = 360 / (2 * math.pi) * self.angle
        self.image = pygame.transform.rotate(self.original, winkel_in_grad)

    def turn_right(self):
        """
        Bewegt die Spielfigur nach rechts
        """
        # 0 ist der index für die x-Koordinate in der [x,y]-Liste
        # Diese wird um 1 grösser gemacht
        self.angle = self.angle - 0.09
        winkel_in_grad = 360 / (2 * math.pi) * self.angle
        self.image = pygame.transform.rotate(self.original, winkel_in_grad)
        
 
    def move_forward(self):
        self.pos[1] = self.pos[1] - math.sin(self.angle) * self.speed 
        self.pos[0] = self.pos[0] + math.cos(self.angle) * self.speed
        pygame.time.delay(30)                      

def select_cars(screen):
    """
    Shows a selection screen. Returns the paths for P1 and P2 cars.
    """
    selected_paths = []
    font = pygame.font.SysFont("Arial", 30)
    
    # Load car surfaces for preview
    car_surfaces = []
    for p in CAR_OPTIONS:
        img = pygame.image.load(p).convert()
        
        # 1. Remove black background (ColorKey 0,0,0)
        img.set_colorkey((0, 0, 0))
        
        # 2. Scale down by 50%
        new_width = int(img.get_width() * 0.5)
        new_height = int(img.get_height() * 0.5)
        img = pygame.transform.smoothscale(img, (new_width, new_height))
        
        car_surfaces.append(img)
    
    # Define click areas (rects) for the 4 cars
    rects = []
    for i in range(4):
        # Adjusted spacing to look better with smaller cars
        rects.append(pygame.Rect(200 + i*200, 450, 100, 100))

    while len(selected_paths) < 2:
        screen.fill((30, 30, 30)) 
        
        curr_player = "Player 1" if len(selected_paths) == 0 else "Player 2"
        txt = font.render(f"{curr_player}: Select your car (Click or Press 1-4)", True, (255, 255, 255))
        screen.blit(txt, (300, 300))

        # Draw cars and numbers
        for i, (surf, rect) in enumerate(zip(car_surfaces, rects)):
            # Draw a subtle border for the "hitbox"
            pygame.draw.rect(screen, (100, 100, 100), rect, 1)
            
            # Center the scaled car in the rectangle
            car_x = rect.x + (rect.width - surf.get_width()) // 2
            car_y = rect.y + (rect.height - surf.get_height()) // 2
            screen.blit(surf, (car_x, car_y))
            
            num_txt = font.render(str(i+1), True, (255, 255, 255))
            screen.blit(num_txt, (rect.centerx - 5, rect.bottom + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            selection_idx = None
            if event.type == QUIT: pygame.quit(); sys.exit()
            
            if event.type == KEYDOWN:
                if K_1 <= event.key <= K_4:
                    selection_idx = event.key - K_1
            
            if event.type == MOUSEBUTTONDOWN:
                for i, rect in enumerate(rects):
                    if rect.collidepoint(event.pos):
                        selection_idx = i
            
            if selection_idx is not None:
                selected_paths.append(CAR_OPTIONS[selection_idx])
                pygame.time.delay(300) # Slightly longer delay to avoid double-input

    return selected_paths

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
    # Wenn die linke Cursortaste gedrückt ist...
    if pressed[K_LEFT] and pressed[K_UP]:        
        player1.turn_left()

    if pressed[K_a] and pressed[K_w]:        
        player2.turn_left()
        
    # Wenn die rechte Cursortaste gedr�ckt ist...
    if pressed[K_RIGHT] and pressed[K_UP]:
        player1.turn_right()

    if pressed[K_d] and pressed[K_w]:
        player2.turn_right()

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
        player2.speed = player2.speed + 0.1
        if pressed[K_a] or pressed[K_d]:
           player2.speed = 1
    else:
        player2.speed = 1

    if player1.counter > 10:
        player1.speed = player1.speed + 0.2
        if pressed[K_RIGHT] or pressed[K_LEFT]:
           player1.speed = 1
    else:
        player1.speed = 1
    
pygame.init()

# Legt die Grösse des Bildschirmfensters in Pixeln fest
screenGeometry = (1190,1040)

# Öffnet ein Grafikfenster mit der angegebenen Grösse
# screen ist eine Art "Leinwand" (surface), auf die
# gezeichnet werden kann
screen = pygame.display.set_mode(screenGeometry)

background_image = pygame.image.load("resources/rennstrecke.png").convert()
background_image.set_colorkey((255,255,255))

frontbackground_image = pygame.image.load("resources/stadion.png").convert()

frontbackground_image = pygame.transform.scale(frontbackground_image, (int(1195), int(1040)))


# Auswählen der Autos
p1_img, p2_img = select_cars(screen)

# Erstelle ein Spieler-Objekt
player1 = Player((393, 666), p1_img)
player2 = Player((393, 696), p2_img)

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

    # Ändert den Zustand des Spiels
    step(events)

    # Ruft die paint-Prozedur auf, welche den aktuellen Zustand
    # auf den Bildschirm zeichnet
    paint(screen)

    # Macht die auf screen gezeichneten Änderungen am
    # Bildschirm sichtbar - ohne das flip() bleibt der
    # Fensterinhalt schwarz
    pygame.display.flip()

# Sorgt dafür, dass Pygame-Resourcen (z.B. Grafiken usw)
# sauber freigegeben werden
pygame.quit()

    

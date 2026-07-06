import sys
import pygame

from pygame.locals import *

from car_race_3_0_config import (
    CARS, MAX_STATS,
    ui_font, text_font,
    get_resource_path
)

def select_cars(screen: pygame.surface.Surface):
    """
    Shows a selection screen. Returns the paths for P1 and P2 cars.
    """
    selected_data = []
    car_previews = []

    # Get all car images
    for name, stats in CARS.items():
        img = pygame.image.load(get_resource_path(stats["car_image"])).convert()
        img.set_colorkey((0, 0, 0))
        img = pygame.transform.smoothscale(img, (int(img.get_width()*0.5), int(img.get_height()*0.5)))
        car_previews.append({"name": name, "surf": img, "stats": stats})

    # Draw fancy rects around the images
    rects = [pygame.Rect(150 + i*250, 400, 150, 150) for i in range(len(car_previews))]

    while len(selected_data) < 2:
        screen.fill((30, 30, 30))        
        current_player = "Player 1" if len(selected_data) == 0 else "Player 2"

        txt = ui_font.render(f"{current_player}: Select your car", True, (255, 255, 255))
        screen.blit(txt, (450, 200))

        for i, item in enumerate(car_previews):
            rect = rects[i]
            # Draw box
            pygame.draw.rect(screen, (60, 60, 60), rect, 0, 5) # Background
            pygame.draw.rect(screen, (200, 200, 200), rect, 2, 5) # Border
            
            # Draw Car Image
            img_x = rect.centerx - item["surf"].get_width() // 2
            img_y = rect.y + 20
            screen.blit(item["surf"], (img_x, img_y))
            
            # Draw Name
            name_txt = text_font.render(item["name"], True, (255, 255, 255))
            screen.blit(name_txt, (rect.centerx - name_txt.get_width()//2, rect.y + 80))

            # Draw stat bars
            stat_list = [("Speed", "max_speed"), ("Accel.", "accel"), ("Agility", "turning"), ("Braking", "braking")]
            bar_width_max = 80
            
            for index, (label, key) in enumerate(stat_list):
                y_offset = rect.y + 170 + (index * 15)
                
                # Label
                lab_surf = text_font.render(label, True, (180, 180, 180))
                screen.blit(lab_surf, (rect.x, y_offset))
                
                # Bar Background (Dark Gray)
                bar_rect_bg = pygame.Rect(rect.x + 55, y_offset + 5, bar_width_max, 8)
                pygame.draw.rect(screen, (60, 60, 60), bar_rect_bg)
                
                # Bar Fill (Colored)
                fill_w = (item["stats"][key] / MAX_STATS[key]) * bar_width_max
                bar_rect_fill = pygame.Rect(rect.x + 55, y_offset + 5, fill_w, 8)
                pygame.draw.rect(screen, (0, 200, 100), bar_rect_fill)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT: pygame.quit(); sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                for i, rect in enumerate(rects):
                    if rect.collidepoint(event.pos):
                        selected_data.append(car_previews[i]["stats"])
                        pygame.time.delay(300)
    
    return selected_data
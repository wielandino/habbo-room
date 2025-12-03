import os
import pygame
import src.objects.room.room as room
import src.objects.furniture.floorfurniture as floorfurniture


# Init
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update
    # ...
    
    # Render
    screen.fill((0, 0, 0))
    room.create_room(None, screen)
    floorfurniture.add_floor_furniture(screen, (1, 3), "club_sofa")

    pygame.display.flip()
    clock.tick(60)
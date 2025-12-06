import os
from src.objects.furniture.floorfurniture import FloorFurniture
from src.data.furniture_registry import FurnitureRegistry
import definitions
import pygame
from src.objects.room.room import Room


# Init
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

FurnitureRegistry.preload_all(["club_sofa"])

room = Room(screen)

club_sofa = FloorFurniture(
    room_x=2,
    room_y=3,
    room_z=0,
    direction=6,
    type="club_sofa"
)

# club_sofa2 = FloorFurniture(
#     room_x=3,
#     room_y=2,
#     room_z=0,
#     direction=2,
#     type="club_sofa"
# )

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update
    # ...
    
    # Render
    screen.fill((0, 0, 0))

    room.render()
    club_sofa.render(screen)
    #club_sofa2.render(screen)

    pygame.display.flip()
    clock.tick(60)
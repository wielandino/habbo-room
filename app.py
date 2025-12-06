import definitions
from src.objects.furniture.furniture import Furniture
from src.data.furniture_registry import FurnitureRegistry
import pygame
from src.objects.room.room import Room
from typing import List

import pygame_gui

# Init
pygame.init()
screen = pygame.display.set_mode((800, 600))


FurnitureRegistry.preload_all(["club_sofa"])

room = Room(screen)

added_furnitures: List[Furniture] = []

club_sofa = Furniture(
    room_x=2,
    room_y=3,
    room_z=0,
    direction=2,
    type="club_sofa"
)

added_furnitures.append(club_sofa)

window_surface = pygame.display.set_mode((800, 600))

manager = pygame_gui.UIManager((800, 600))
clock = pygame.time.Clock()

furniture_ui_panel = None
rotate_button = None
selected_furniture = None
last_selected_furniture = None

panel_width = 200
panel_height = 150
panel_x = 800 - panel_width - 10 
panel_y = 560 - panel_height - 10

def update_furniture_ui(furniture):
    global furniture_ui_panel, rotate_button

    if furniture_ui_panel is not None:
        furniture_ui_panel.kill()
        furniture_ui_panel = None

    if rotate_button is not None:
        rotate_button.kill()
        rotate_button = None

    if furniture is None:
        return
    
    furniture_ui_panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect(panel_x, panel_y, panel_width, panel_height),
        starting_height=1,
        manager=manager
    )

    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0, 0), (panel_width, 20)),  # volle Panel-Breite, Höhe 20
        text=furniture.type,
        container=furniture_ui_panel,
        manager=manager,
    )

    icon_surface = pygame.image.load(
        f"{definitions.ROOT_DIR}/src/data/furnitures/{selected_furniture.type}/images/icon.png"
    ).convert_alpha()

    orig_w, orig_h = icon_surface.get_size()

    pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((40, 30), (orig_w, orig_h)),
            image_surface=icon_surface,
            container=furniture_ui_panel,
            manager=manager
        ) 
    
    rotate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(panel_x, panel_y + panel_height + 5, panel_width, 30),  # unter Panel
            text="Rotate",
            manager=manager
    )
    


running = True
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            for furniture in added_furnitures:
                if furniture.get_rect().collidepoint(mouse_pos):
                    selected_furniture = furniture
                    break
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == rotate_button:
                if selected_furniture is not None:
                    selected_furniture.rotate_clockwise()

        if selected_furniture != last_selected_furniture:
            update_furniture_ui(selected_furniture)
            last_selected_furniture = selected_furniture


    manager.update(time_delta)

    # Render
    screen.fill((0, 0, 0))
    room.render()
    club_sofa.render(screen)

    manager.draw_ui(window_surface)
    pygame.display.flip()
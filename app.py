import definitions
from src.objects.furniture.furniture import Furniture
from src.data.furniture_registry import FurnitureRegistry
import pygame
from src.objects.room.room import Room
from typing import List

import pygame_gui

from src.ui.furniture_ui_manager import FurnitureUIManager
from src.utils.furniture_selector import FurnitureSelector
from src.utils.ui_utils import SCREEN_HEIGHT, SCREEN_WIDTH

# Init
pygame.init()
screen = pygame.display.set_mode((800, 600))


FurnitureRegistry.preload_all(["club_sofa"])

room = Room(screen)

window_surface = pygame.display.set_mode((800, 600))

manager = pygame_gui.UIManager((800, 600))
clock = pygame.time.Clock()


class App:
    added_furnitures: List[Furniture] = []
    furnitures: List[Furniture]

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Furniture Placement")
        
        self.clock = pygame.time.Clock()
        self.ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.__initialize_game_objects()
        
        self.furniture_ui = FurnitureUIManager(self.ui_manager)
        self.selector = FurnitureSelector(self.furnitures)
        
        self.running = True


    def __initialize_game_objects(self):
        self.room = Room(self.screen)
        
        self.furnitures = [
            Furniture(
                room_x=2,
                room_y=3,
                room_z=0,
                direction=2,
                type="club_sofa"
            ),

            # Furniture(
            #     room_x=4,
            #     room_y=3,
            #     room_z=0,
            #     direction=2,
            #     type="nft_md_limukaappi"
            # ),

            Furniture(
                room_x=3,
                room_y=4,
                room_z=0,
                direction=2,
                type="rare_dragonlamp",
                color_id=11
            )
        ]
    
    def handle_events(self):
        time_delta = self.clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            self.ui_manager.process_events(event)
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self.furniture_ui.handle_button_click(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.__is_click_on_ui(event.pos):
                    if self.selector.handle_click(event.pos):
                        self.furniture_ui.update(self.selector.selected)
        
        for furniture in self.furnitures:
            furniture.update(time_delta)

        self.ui_manager.update(time_delta)
    
    def __is_click_on_ui(self, pos: tuple) -> bool:
        if self.furniture_ui.panel is not None:
            panel_rect = self.furniture_ui.panel.get_abs_rect()
            if panel_rect.collidepoint(pos):
                return True
        
        if self.furniture_ui.rotate_button is not None:
            button_rect = self.furniture_ui.rotate_button.get_abs_rect()
            if button_rect.collidepoint(pos):
                return True
            
        if self.furniture_ui.use_button is not None:
            button_rect = self.furniture_ui.use_button.get_abs_rect()
            if button_rect.collidepoint(pos):
                return True
        
        return False

    def render(self):
        self.screen.fill((0, 0, 0))
        self.room.render()
        
        for furniture in self.furnitures:
            furniture.render(self.screen)
        
        self.ui_manager.draw_ui(self.screen)
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.render()
        
        pygame.quit()

app = App()
app.run()
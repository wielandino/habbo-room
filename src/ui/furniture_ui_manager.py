from typing import Optional
import pygame
import pygame_gui

import definitions
from src.objects.furniture.furniture import Furniture
from src.utils.ui_utils import PANEL_HEIGHT, PANEL_MARGIN_X, PANEL_MARGIN_Y, PANEL_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH

class FurnitureUIManager:

    def __init__(self, manager: pygame_gui.UIManager):
        self.manager = manager
        self.panel: Optional[pygame_gui.elements.UIPanel] = None
        self.rotate_button: Optional[pygame_gui.elements.UIButton] = None
        self.current_furniture: Optional[Furniture] = None
        
        self.panel_x = SCREEN_WIDTH - PANEL_WIDTH - PANEL_MARGIN_X
        self.panel_y = SCREEN_HEIGHT - PANEL_HEIGHT - PANEL_MARGIN_Y
    
    def update(self, furniture: Optional[Furniture]):
        if furniture == self.current_furniture:
            return
        
        self.__clear_ui()
        self.current_furniture = furniture
        
        if furniture is None:
            return
        
        self.__create_panel(furniture)
        self.__create_rotate_button()
    
    def __clear_ui(self):
        if self.panel is not None:
            self.panel.kill()
            self.panel = None
        if self.rotate_button is not None:
            self.rotate_button.kill()
            self.rotate_button = None
    
    def __create_panel(self, furniture: Furniture):
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                self.panel_x, self.panel_y, 
                PANEL_WIDTH, PANEL_HEIGHT
            ),
            starting_height=1,
            manager=self.manager
        )
        
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (PANEL_WIDTH, 20)),
            text=furniture.type,
            container=self.panel,
            manager=self.manager
        )
        
        icon_path = f"{definitions.ROOT_DIR}/src/data/furnitures/{furniture.type}/images/icon.png"
        icon_surface = pygame.image.load(icon_path).convert_alpha()
        icon_w, icon_h = icon_surface.get_size()
        
        pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((40, 30), (icon_w, icon_h)),
            image_surface=icon_surface,
            container=self.panel,
            manager=self.manager
        )
    
    def __create_rotate_button(self):
        button_y = self.panel_y + PANEL_HEIGHT + 5
        self.rotate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                self.panel_x, button_y, 
                PANEL_WIDTH, 30
            ),
            text="Rotate",
            manager=self.manager
        )
    
    def handle_button_click(self, event) -> bool:
        if event.ui_element == self.rotate_button and self.current_furniture:
            self.current_furniture.change_direction()
            return True
        return False
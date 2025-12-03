import pygame
import definitions
from dataclasses import dataclass

@dataclass
class FurnitureAsset:
    flip_h: bool = False
    type: str = ""
    offset_x: int = 0
    offset_y: int = 0
    source_name: str = ""
    sprite: pygame.Surface = None
import pygame
from dataclasses import dataclass

@dataclass
class FurnitureAsset:
    name: str
    flip_h: bool = False
    type: str = ""
    offset_x: int = 0
    offset_y: int = 0
    source_name: str = ""
    sprite: pygame.Surface = None
    frame: int = 0

    def get_sprite(self, all_assets: dict) -> pygame.Surface:
        if self.sprite:
            return self.sprite
        
        if self.flip_h and self.source_name:
            source_asset = all_assets.get(self.source_name)
            if source_asset and source_asset.sprite:
                return pygame.transform.flip(source_asset.sprite, True, False)
        
        return None 
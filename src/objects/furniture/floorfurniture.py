import pygame

from src.objects.furniture.furniture import Furniture
from src.data.furniture_registry import FurnitureRegistry
from src.objects.room.room_config import RoomConfig

from dataclasses import dataclass, field

from src.utils.iso_utils import IsoUtils


@dataclass
class FloorFurniture:
    room_x: int
    room_y: int
    room_z: int
    direction: int
    type: str

    __furniture_data: Furniture = field(init=False, repr=False)

    def __post_init__(self):

        self.__furniture_data = FurnitureRegistry.load_furniture(self.type)
        
        if not self.__furniture_data:
            raise ValueError(f"Can't load Furniture-Type: '{self.type}' ")

    def render(self, surface: pygame.Surface):
   
        screen_x, screen_y = IsoUtils.grid_to_screen(self.room_x, self.room_y)
        
        sorted_layers = sorted(self.__furniture_data.layers, key=lambda l: l.z_index)
        
        for layer in sorted_layers:
            asset = layer.assets.get(self.direction)
            
            if not asset:
                continue
            
            sprite = asset.get_sprite(self.__furniture_data.all_assets)
            
            if not sprite:
                continue
            
            render_x, render_y = self._calculate_render_position(
                screen_x, screen_y, asset, sprite
            )
            
            surface.blit(sprite, (render_x, render_y))
    
    def _calculate_render_position(self, screen_x: int, screen_y: int, 
                                   asset: str, 
                                   sprite: pygame.Surface) -> tuple[int, int]:

        is_vertical = self.direction in [0, 4]
        needs_correction = asset.flip_h and is_vertical
        
        if not needs_correction:
            return (screen_x - asset.offset_x, screen_y - asset.offset_y)
        
        sprite_width = sprite.get_width()
        source_asset = self.__furniture_data.all_assets.get(asset.source_name)
        
        if not source_asset:
            return (screen_x - asset.offset_x, screen_y - asset.offset_y)
        
        flipped_offset_x = sprite_width - source_asset.offset_x

        tile_count = self.__furniture_data.tile_width
        tile_shift_x = (tile_count - 1) * (RoomConfig.TILE_WIDTH // 2)
        tile_shift_y = (tile_count - 1) * (RoomConfig.TILE_HEIGHT // 2)
        
        render_x = screen_x - flipped_offset_x - tile_shift_x
        render_y = screen_y - asset.offset_y + tile_shift_y
        
        return (render_x, render_y)
    
    def get_occupied_tiles(self) -> list[tuple[int, int]]:
        tiles = []
        tile_width = self.__furniture_data.tile_width
        tile_height = self.__furniture_data.tile_height
        
        if self.direction in [0, 4]:
            for dy in range(tile_width):
                for dx in range(tile_height):
                    tiles.append((self.room_x + dx, self.room_y + dy))
        else:
            for dx in range(tile_width):
                for dy in range(tile_height):
                    tiles.append((self.room_x + dx, self.room_y + dy))
        
        return tiles
    
    def rotate_clockwise(self):
        self.direction = (self.direction + 2) % 8
    
    def rotate_counter_clockwise(self):
        self.direction = (self.direction - 2) % 8
    
    @property
    def furniture_type(self) -> str:
        return self.__furniture_data.name
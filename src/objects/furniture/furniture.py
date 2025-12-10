import pygame

from src.data.furniture_asset import FurnitureAsset
from src.objects.furniture.furniture_base import FurnitureBase
from src.data.furniture_registry import FurnitureRegistry
from src.objects.room.room_config import RoomConfig

from dataclasses import dataclass, field

from src.utils.iso_utils import IsoUtils


@dataclass
class Furniture:
    room_x: int
    room_y: int
    room_z: int
    direction: int
    type: str

    screen_x: int = field(init=False)
    screen_y: int = field(init=False)

    __furniture_data: FurnitureBase = field(init=False, repr=False)

    def __post_init__(self):
        print(f"Furniture Class {self.type} created")
        self.__furniture_data = FurnitureRegistry.load_furniture(self.type)
        
        if not self.__furniture_data:
            raise ValueError(f"Can't load Furniture-Type: '{self.type}' ")
        
        self.screen_x, self.screen_y = IsoUtils.grid_to_screen(self.room_x, self.room_y)

    def render(self, surface: pygame.Surface):
   
        for layer in self.__furniture_data.layers:
            asset = layer.assets.get(self.direction)
            
            if not asset:
                continue
            
            sprite = asset.get_sprite(self.__furniture_data.all_assets)
            
            if not sprite:
                continue

            render_x, render_y = self.__calculate_render_position(
                self.screen_x, self.screen_y, asset, sprite
            )
            
            surface.blit(sprite, (render_x, render_y))
    
    def __calculate_render_position(self, screen_x: int, screen_y: int, 
                                   asset: FurnitureAsset, 
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
        
        render_x = screen_x - flipped_offset_x - tile_shift_x
        render_y = screen_y - asset.offset_y
        
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
    
    def change_direction(self):
        next_direction = self.direction + 2

        if next_direction in self.__furniture_data.possible_directions:
            self.direction = next_direction
        else:
            self.direction = self.__furniture_data.possible_directions[0]

    
    def get_rect(self) -> pygame.Rect:
        min_x = float('inf')
        min_y = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')

        for layer in self.__furniture_data.layers:
            asset = layer.assets.get(self.direction)
            if not asset:
                continue

            sprite = asset.get_sprite(self.__furniture_data.all_assets)
            if not sprite:
                continue

            sprite_w = sprite.get_width()
            sprite_h = sprite.get_height()

            is_vertical = self.direction in [0, 4]
            needs_correction = asset.flip_h and is_vertical

            if not needs_correction:
                render_x = self.screen_x - asset.offset_x
                render_y = self.screen_y - asset.offset_y
            else:
                source_asset = self.__furniture_data.all_assets.get(asset.source_name)
                flipped_offset_x = sprite_w - (source_asset.offset_x if source_asset else asset.offset_x)

                tile_count = self.__furniture_data.tile_width
                tile_shift_x = (tile_count - 1) * (RoomConfig.TILE_WIDTH // 2)
                tile_shift_y = (tile_count - 1) * (RoomConfig.TILE_HEIGHT // 2)

                render_x = self.screen_x - flipped_offset_x - tile_shift_x
                render_y = self.screen_y - asset.offset_y + tile_shift_y

            min_x = min(min_x, render_x)
            min_y = min(min_y, render_y)
            max_x = max(max_x, render_x + sprite_w)
            max_y = max(max_y, render_y + sprite_h)

        if min_x == float('inf') or min_y == float('inf'):
            return pygame.Rect(self.screen_x, self.screen_y, 0, 0)

        width = max_x - min_x
        height = max_y - min_y

        return pygame.Rect(min_x, min_y, width, height)

    @property
    def furniture_type(self) -> str:
        return self.__furniture_data.name
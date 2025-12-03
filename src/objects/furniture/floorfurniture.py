# floorfurniture.py
import pygame
import src.objects.room.room as room

def add_floor_furniture(surface: pygame.Surface, grid_position: tuple[int, int], type: str):

    room_size = 64
    

    grid_x, grid_y = grid_position
    
    tile_width = 128
    tile_height = 64
    offset_x = 400
    offset_y = 100
    
    iso_x, iso_y = room.grid_to_iso(grid_x, grid_y, tile_width, tile_height)

    screen_x = iso_x + offset_x
    screen_y = iso_y + offset_y
    

export = {
    "add_floor_furniture": add_floor_furniture
}
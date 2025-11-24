import pygame

# Init
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


def grid_to_iso(grid_x, grid_y, tile_width=64, tile_height=32):
    iso_x = (grid_x - grid_y) * (tile_width // 2)
    iso_y = (grid_y + grid_x) * (tile_height // 2)

    return iso_x, iso_y

def draw_iso_tile(surface, x, y, tile_width, tile_height, color):
    points = [
        (x, y),                              
        (x + tile_width // 2, y + tile_height // 2),
        (x, y + tile_height),
        (x - tile_width // 2, y + tile_height // 2)
    ]

    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, (145, 144, 92), points, 1)

def draw_iso_wall_left(surface, x, y, tile_width, tile_height, color):
    wall_height = tile_height * 2

    points = [
        (x, y),
        (x - tile_width // 2, y + tile_height // 2),
        (x - tile_width // 2, y + tile_height // 2 + wall_height),
        (x, y + wall_height)
    ]

    bx = x - 6
    by = y - 6

    top_points = [
        (bx, by), # top point
        (bx - tile_width // 2, by + tile_height // 2), # left point
        (bx - tile_width // 2 + 6, by + tile_height // 2 + 6), # bottom left point
        (bx + 6, by + 6) # bottom point
    ]

    left_side_points = [
        (bx - tile_width // 2, by + tile_height // 2), # top left
        (bx - tile_width // 2 + 5, by + tile_height // 2), # top right
        (bx - tile_width // 2 + 5, by + tile_height // 2 + wall_height + 10), # bottom right
        (bx - tile_width // 2, by + tile_height // 2 + wall_height + 6.5) # bottom left
    ]

    pygame.draw.polygon(surface, (255, 255, 255), left_side_points)
    pygame.draw.polygon(surface, (152, 152, 152), top_points)
    pygame.draw.polygon(surface, color, points)


def draw_iso_wall_top(surface, x, y, tile_width, tile_height, color):
    wall_height = tile_height * 2
    
    points = [
        (x, y),                          
        (x + tile_width // 2, y + tile_height // 2),            
        (x + tile_width // 2, y + tile_height // 2 + wall_height),
        (x, y + wall_height)
    ]
    bx = x + 6
    by = y - 6

    top_points = [
        (bx, by),   
        (bx + tile_width // 2, by + tile_height // 2),     
        (bx + tile_width // 2 - 6, by + tile_height // 2 + 6),  
        (bx - 6, by + 6)                                   
    ]
    
    right_side_points = [
        (bx + tile_width // 2, by + tile_height // 2),                    
        (bx + tile_width // 2 - 5, by + tile_height // 2),
        (bx + tile_width // 2 - 5, by + tile_height // 2 + wall_height + 10),  
        (bx + tile_width // 2, by + tile_height // 2 + wall_height + 6.5)      
    ]
    pygame.draw.polygon(surface, (203, 203, 203), right_side_points)
    pygame.draw.polygon(surface, (152, 152, 152), top_points)
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, color, points, 2)

def draw_iso_tile_left_outline(surface, x, y, tile_width, tile_height, color):
    points = [
        (x, y),                              
        (x + tile_width // 2, y + tile_height // 2),
        (x, y + tile_height),
        (x - tile_width // 2, y + tile_height // 2)
    ]
    
    bottom = points[2]
    left = points[3]
    pygame.draw.line(surface, color, bottom, left, 10)

def draw_iso_tile_right_outline(surface, x, y, tile_width, tile_height, color):
    points = [
        (x, y),                              
        (x + tile_width // 2, y + tile_height // 2),
        (x, y + tile_height),
        (x - tile_width // 2, y + tile_height // 2)
    ]
    
    bottom = points[2]
    right = points[1]
    pygame.draw.line(surface, color, bottom, right, 10)

def create_room(tilemap = None):
    tile_width = 128
    tile_height = 64

    if tilemap is None:
        # x = wall
        # o = floor
        tilemap = ("xxxxx\n"
                   "xoooo\n"
                   "xoooo\n"
                   "xoooo\n"
                   "xoooo")
        
    converted_tilemap = convert_tilemap(tilemap)

    offset_x = 400
    offset_y = 100

    for y, row in enumerate(converted_tilemap):
        for x, tile in enumerate(row):
            iso_x, iso_y = grid_to_iso(x, y, tile_width, tile_height)
            
            if tile == 1:
                colorWallLeft = (203, 203, 203)
                colorWallTop = (255, 255, 255)
                
                if x + 1 < len(row) and row[x + 1] == 0:
                    draw_iso_wall_left(screen, 
                                     iso_x + offset_x + tile_width // 2,   
                                     iso_y + offset_y - tile_height - (tile_height // 2),
                                     tile_width, tile_height, colorWallLeft)
                
                if y + 1 < len(converted_tilemap) and converted_tilemap[y + 1][x] == 0:
                    draw_iso_wall_top(screen, 
                                      iso_x + offset_x - tile_width // 2,   
                                      iso_y + offset_y - tile_height - (tile_height // 2),
                                      tile_width, tile_height, colorWallTop)
                    
            elif tile == 0:
                color = (152, 152, 101)
                draw_iso_tile(screen, iso_x + offset_x, iso_y + offset_y, 
                              tile_width, tile_height, color)
                
                if y + 1 == len(converted_tilemap):
                    draw_iso_tile_left_outline(screen, 
                                          iso_x + offset_x, 
                                          iso_y + offset_y, 
                                          tile_width, tile_height, 
                                          (132, 132, 81))
                    
                if x + 1 == len(row):
                    draw_iso_tile_right_outline(screen, 
                                           iso_x + offset_x, 
                                           iso_y + offset_y, 
                                           tile_width, tile_height, 
                                           (112, 112, 61))
            

            
def convert_tilemap(tilemap):
    def to_tile_type(ch):
        # 'x' = 1 (wall), 'o' = 0 (floor)
        if ch == "x":
            return 1
        if ch == "o":
            return 0
        return None

    lines = tilemap.split("\n")
    rows = [line.strip() for line in lines]                
    rows = [r for r in rows if len(r) > 0]                  
    converted = [[to_tile_type(ch) for ch in row] for row in rows]
    return converted



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update
    # ...
    
    # Render
    screen.fill((0, 0, 0))
    create_room(None)


    pygame.display.flip()
    clock.tick(60)
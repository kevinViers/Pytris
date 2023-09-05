import pygame
import random
from playsound import playsound
pygame.init()
import win32api

def get_monitor_refresh_rate():
    device = win32api.EnumDisplaySettings(None, -1)
    return device.DisplayFrequency
    
monitor_refresh_rate = get_monitor_refresh_rate()

WIDTH, HEIGHT = 300, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = monitor_refresh_rate
BLOCK_SIZE = 30
ROWS, COLS = HEIGHT // BLOCK_SIZE, WIDTH // BLOCK_SIZE
RED = (255, 0, 0)
BLACK = (0, 0, 0)
SPAWN_SPEED = FPS / 100
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

#art class
shapes = [
    [[1, 1, 1],
     [0, 1, 0]],
     
    [[0, 1, 1],
     [1, 1, 0]],
     
    [[1, 1, 0],
     [0, 1, 1]],
     
    [[1, 1],
     [1, 1]],
     
    [[1, 1, 1, 1]],
    
    [[1, 1, 1, 1, 1]],
    
    [[1, 1, 1, 1],
     [1, 1, 1, 1],
     [1, 1, 1, 1]],    
     
    [[1, 1, 1],
     [1, 0, 0]],
     
    [[1, 1, 1],
     [0, 0, 1]]
]

def rotate(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]
    
def collision(grid, shape, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if shape[row][col]:
                if y + row >= len(grid) or x + col >= len(grid[0]) or x + col < 0 or grid[y + row][x + col] != 0:
                    return True
    return False

def clear_rows(grid, rows_cleared):
    rows_to_clear = []
    for row in range(len(grid) - 1, -1, -1):
        if 0 not in grid[row]:
            rows_to_clear.append(row)
    
    for row in reversed(rows_to_clear):
        del grid[row]
        grid.insert(0, [0 for _ in range(len(grid[0]))])
        rows_cleared += 1
        pygame.mixer.init()
        my_sound = pygame.mixer.Sound('cleared_row.mp3')
        my_sound.play()
        my_sound.set_volume(0.25)  # set this to a volume that's reasonable. 100% made my ears bleed
        
    
    return rows_cleared         
    return rows_cleared


def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            color = RED if grid[y][x] else BLACK
            pygame.draw.rect(SCREEN, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            
def draw_grid_lines():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(SCREEN, (128, 128, 128), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(SCREEN, (128, 128, 128), (0, y), (WIDTH, y))

def draw_shape(shape, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                pygame.draw.rect(SCREEN, RED, ((x + col) * BLOCK_SIZE, (y + row) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                
                

def main():
    run = True
    shape = random.choice(shapes)
    x, y = 5, 0
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 500  # 500 milliseconds = 1/2 sec per square
    rows_cleared = 0
    
    key_timers = {"left": 0, "right": 0, "down": 0, "rotate": 0}
    key_delays = {"left": 150, "right": 150, "down": 50, "rotate": 200}  # in milliseconds

    while run:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        keys = pygame.key.get_pressed()

        # Left movement
        if keys[pygame.K_LEFT]:
            if current_time - key_timers["left"] > key_delays["left"]:
                if not collision(grid, shape, x - 1, y):
                    x -= 1
                key_timers["left"] = current_time

        # Right movement
        if keys[pygame.K_RIGHT]:
            if current_time - key_timers["right"] > key_delays["right"]:
                if not collision(grid, shape, x + 1, y):
                    x += 1
                key_timers["right"] = current_time

        # Down movement
        if keys[pygame.K_DOWN]:
            if current_time - key_timers["down"] > key_delays["down"]:
                if not collision(grid, shape, x, y + 1):
                    y += 1
                key_timers["down"] = current_time

        # Rotation
        if keys[pygame.K_UP]:
            if current_time - key_timers["rotate"] > key_delays["rotate"]:
                rotated = rotate(shape)
                if not collision(grid, rotated, x, y):
                    shape = rotated
                key_timers["rotate"] = current_time
        
        if pygame.time.get_ticks() - fall_time > fall_speed:
            if not collision(grid, shape, x, y + 1):
                y += 1
            else:
                for row in range(len(shape)):
                    for col in range(len(shape[0])):
                        if shape[row][col]:
                            grid[y + row][x + col] = 1
                shape = random.choice(shapes)
                x, y = 5, 0
                rows_cleared = clear_rows(grid, rows_cleared)
                
                score = rows_cleared * 10
                pygame.display.set_caption(f"Score: {score}")

            fall_time = pygame.time.get_ticks()
    
        SCREEN.fill(BLACK)  # Clear screen
        draw_grid()
        draw_shape(shape, x, y)
        draw_grid_lines()
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()
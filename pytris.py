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
BLOCK = (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))
BACKGROUND = (0,0,0)
SPAWN_SPEED = FPS / 100
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
im_drunk_col_sizes = [1.0 for _ in range(COLS)]

def update_im_drunk_col_sizes():
    global im_drunk_col_sizes
    available_units = len(im_drunk_col_sizes)
    for i in range(len(im_drunk_col_sizes)):
        if available_units > 1:
            new_size = random.uniform(0.25, 1.75)
            im_drunk_col_sizes[i] = new_size
            available_units -= new_size
        else:
            im_drunk_col_sizes[i] = available_units
            break
    random.shuffle(im_drunk_col_sizes)
    
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
        
    
    if rows_cleared % 2 == 0 and rows_cleared > 0:  # Every other row cleared
            apply_sabotage()
            
    return rows_cleared



def draw_grid():
    x_offset = 0
    for col in range(COLS):
        col_width = BLOCK_SIZE * im_drunk_col_sizes[col]
        for row in range(ROWS):
            color = BLOCK if grid[row][col] else BACKGROUND
            if sabotage_active == 'color_confusion':
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pygame.draw.rect(SCREEN, color, (x_offset, row * BLOCK_SIZE, col_width, BLOCK_SIZE))
        x_offset += col_width
        
def draw_grid_lines():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(SCREEN, (169, 169, 169), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(SCREEN, (169, 169, 169), (0, y), (WIDTH, y))

def draw_shape(shape, x, y):
    for row in range(len(shape)):
        col_start = x * BLOCK_SIZE
        for col in range(len(shape[row])):
            col_width = BLOCK_SIZE * im_drunk_col_sizes[x + col]
            if shape[row][col]:
                pygame.draw.rect(SCREEN, BLOCK, (col_start, (y + row) * BLOCK_SIZE, col_width, BLOCK_SIZE))
            col_start += col_width
def apply_sabotage():
    global sabotage_active, sabotage_end_time, column_sizes
    sabotage_list = ["reverse_c`ontrols", '',"block_morph", "color_confusion", "", ""]
    sabotage_active = random.choice(sabotage_list)
    sabotage_end_time = pygame.time.get_ticks() + 5000  # 5 seconds
    print(f"Sabotage activated: {sabotage_active}")
 

# Global variable for a second shape during 'double_trouble'
# Global variable for "I'm Drunk!" column sizes
im_drunk_col_sizes = [1 for _ in range(COLS)]

def update_im_drunk_col_sizes():
    global im_drunk_col_sizes
    total_size = 0
    new_sizes = []
    for _ in range(COLS):
        size = random.uniform(0.25, 1.75)
        new_sizes.append(size)
        total_size += size

    # Normalize sizes so the total remains the same
    im_drunk_col_sizes = [size / total_size for size in new_sizes]
second_shape = None

def main():
    global sabotage_active, sabotage_end_time, second_shape  # Declare global variables
    sabotage_active = None
    sabotage_end_time = 0

    run = True
    shape = random.choice(shapes)
    x, y = 5, 0
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 500  # 500 milliseconds = 1/2 sec per square
    rows_cleared = 0
    morph_time = 0  # Initialize morph time
    morph_speed = 500  # 500 milliseconds = 1/2 second per morph
    COLS = 10  # For example, if you have 10 columns
    column_sizes = [1 for _ in range(COLS)]  # Initialize all columns to size 1


    
    key_timers = {"left": 0, "right": 0, "down": 0, "rotate": 0}
    key_delays = {"left": 150, "right": 150, "down": 50, "rotate": 200}  # in milliseconds

    while run:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        keys = pygame.key.get_pressed()

        # Reverse Controls
        move_left_key = pygame.K_RIGHT if sabotage_active == 'reverse_controls' else pygame.K_LEFT
        move_right_key = pygame.K_LEFT if sabotage_active == 'reverse_controls' else pygame.K_RIGHT

        # Left movement
        if keys[move_left_key]:
            if current_time - key_timers["left"] > key_delays["left"]:
                if not collision(grid, shape, x - 1, y):
                    x -= 1
                key_timers["left"] = current_time

        # Right movement
        if keys[move_right_key]:
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

       # Block Morph
        if sabotage_active == 'block_morph':
            if pygame.time.get_ticks() - morph_time > morph_speed:
                shape = random.choice(shapes)
                morph_time = pygame.time.get_ticks()  # Reset the morph timer 
        try:
            if pygame.time.get_ticks() - fall_time > fall_speed:
                if not collision(grid, shape, x, y + 1):
                    y += 1
                else:
                    for row in range(len(shape)):
                        for col in range(len(shape[0])):
                            if shape[row][col]:
                                grid[y + row][x + col] = 1  # This line can cause IndexError
                    shape = random.choice(shapes)
                    x, y = 5, 0
                    rows_cleared = clear_rows(grid, rows_cleared)
                    
                    # Double Trouble
                    if sabotage_active == 'double_trouble':
                        second_shape = random.choice(shapes)
                    
                    score = rows_cleared * 10
                    pygame.display.set_caption(f"Score: {score}")
    
                fall_time = pygame.time.get_ticks()
            
            SCREEN.fill(BACKGROUND)  # Clear screen
            draw_grid()
            draw_shape(shape, x, y)
            
            # Draw second shape for Double Trouble
            if second_shape:
                draw_shape(second_shape, x + 3, y)  # Offset by 3 blocks
            
            draw_grid_lines()
            pygame.display.update()
    
            # Activate "I'm Drunk!" sabotage
            if sabotage_active == 'im_drunk':
                update_im_drunk_col_sizes()
                
            
        # Activate "I'm Drunk!" sabotage
            if sabotage_active == 'im_drunk':
                update_im_drunk_col_sizes()

        # Deactivate the sabotage
                if pygame.time.get_ticks() - sabotage_end_time > 5000:  # 5 seconds
                    sabotage_active = None  # Reset the sabotage
                    second_shape = None  # Reset the second shape
        except IndexError:
            # Reset everything in case of IndexError
            shape = random.choice(shapes)
            x, y = 5, 0
            sabotage_active = None

    pygame.quit()


if __name__ == "__main__":
    main()

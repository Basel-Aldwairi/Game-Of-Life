import numpy as np
import pygame

#  Constants
ROWS = 54
COLS = 96
CELL_SIZE = 20
WIDTH ,HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

DEAD, ALIVE = 0,1

#  Game grid
grid = np.zeros((ROWS,COLS),dtype=np.uint8)

COLORS = {
    DEAD: (0,0,0),
    ALIVE: (255,255,255)
}

# Game initializations
pygame.init()
screen = pygame.display.set_mode(((WIDTH,HEIGHT)))
clock = pygame.time.Clock()

font = pygame.font.Font(None,24)
running = True
auto_step = False
spead_list = [1,5,10,15,20,30,40,50,100,200]
spead = 2
generation = 0
population = 0

#  Draw the grid on the Pygame window
def draw():
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(screen,COLORS[int(grid[y,x])],
                             (x*CELL_SIZE,y*CELL_SIZE, CELL_SIZE,CELL_SIZE))

# Get the number of neighbors
def get_number_of_neighbors(x,y):
    neighbors = grid[max(y-1,0):min(y+2,ROWS),max(x-1,0):min(x+2,COLS)].copy()
    # print(neighbors)
    if y != 0:
        y = 1
    if x != 0:
        x = 1
    neighbors[y,x] = 0
    alive_count = neighbors.sum()
    return alive_count

def get_population():
    global grid
    return grid.sum()

# Simulation Physics
def sim_step():
    global grid, generation
    next_grid = np.zeros((ROWS,COLS),dtype=np.uint8)
    for ny in range(ROWS):
        for nx in range(COLS):

            # Logic for Updating
            alive_neighbors = get_number_of_neighbors(nx,ny)
            alive_state = True if grid[ny,nx] == 1 else False
            n2 = True if alive_neighbors == 2 else False
            n3 = True if alive_neighbors == 3 else False

            alive_state = (alive_state and (n2 or n3) )or (not alive_state and n3)
            next_grid[ny,nx] = 1 if alive_state else 0
    # Update grid
    generation += 1
    grid = next_grid.copy()


# Game loop
while running:
    for event in pygame.event.get():
     # Controls
     if event.type == pygame.QUIT:
            running = False

     if event.type == pygame.MOUSEBUTTONDOWN:
         key_pressed = event.button
         mx, my = pygame.mouse.get_pos()
         x, y = mx // CELL_SIZE, my // CELL_SIZE
         if 0 <= x < COLS and 0 <= y < ROWS:
             if key_pressed == 1:
                 if grid[y, x] == DEAD:
                     grid[y, x] = ALIVE
             elif key_pressed == 3:
                 if grid[y, x] == ALIVE:
                     grid[y, x] = DEAD

     elif event.type == pygame.KEYDOWN:
        key_pressed = event.key
        # Right arrow: Single Step
        if key_pressed == pygame.K_RIGHT and not auto_step:
            sim_step()

        # Left arrow: Toggle Auto Steps
        if key_pressed == pygame.K_LEFT:
            auto_step = not auto_step

            # Up & Down arrows: Increase & Decrease auto_step speed
        if key_pressed == pygame.K_UP:
            spead = (spead + 1) % len(spead_list)

        if key_pressed == pygame.K_DOWN:
            spead = (spead - 1) % len(spead_list)

    if auto_step:
        sim_step()

    screen.fill((0,0,0))
    draw()

    # Show Current Information
    text_dict = {
        'Population' : get_population(),
        'Generation' : generation,
        'Speed' : spead_list[spead],
        'Auto Step' : auto_step
    }

    y_text = 10
    x_text = 100
    for key, value in text_dict.items():

        key_text = font.render(str(key), True,(255,255,255))
        value_text = font.render(f' :    {value}', True,(255,255,255))
        screen.blit(key_text,(x_text,y_text))
        screen.blit(value_text, (x_text + 100, y_text))
        y_text += 24


    pygame.display.flip()

    # Change Clock Speed based on auto_step
    if auto_step:
        clock.tick(spead_list[spead])
    else:
        clock.tick(60)

pygame.quit()
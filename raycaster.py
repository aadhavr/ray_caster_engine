import pygame
import numpy as np
import math

# Initialize Pygame
pygame.init()

# Set up the game window
worldx, worldy = 800, 600
grid_size = 8
cell_size = min(worldx, worldy) // grid_size
window = pygame.display.set_mode((worldx, worldy))
pygame.display.set_caption("Raycaster")

# Colors
BLACK = (0, 0, 0)
WHITE = (255,255,255)
GREY = (220,220,220)

# Player properties
player_width, player_height = cell_size/4, cell_size/4
player_x = (worldx - player_width) // 2
player_y = (worldy - player_height) // 2
player_speed = 7
player_dx = 0
player_dy = 0
player_a = 0


# MAP
obstacles = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

# Game loop
main = True
clock = pygame.time.Clock()

while main:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main = False

    # THIS CODE WORKS FOR JUST CONTROLLING THE PLAYER
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_a]:
    #     player_x -= player_speed
    # if keys[pygame.K_d]:
    #     player_x += player_speed
    # if keys[pygame.K_w]:
    #     player_y -= player_speed
    # if keys[pygame.K_s]:
    #     player_y += player_speed

    # code that prevents it from hitting the walls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        next_x = int(player_x) // cell_size
        if next_x >= 0 and not obstacles[int(player_y) // cell_size][next_x]:
            player_x -= player_speed
        player_a -= 0.1
        if player_a < 0:
            player_a += 2 * np.pi
        player_dx = np.cos(player_a)*5
        player_dy = np.sin(player_a)*5
    if keys[pygame.K_d]:
        next_x = int(player_x + player_width) // cell_size
        if next_x < grid_size and not obstacles[int(player_y) // cell_size][next_x]:
            player_x += player_speed
        player_a += 0.1
        if player_a > (2*np.pi):
            player_a -= 2 * np.pi
        player_dx = np.cos(player_a)*5
        player_dy = np.sin(player_a)*5
    if keys[pygame.K_w]:
        next_y = int(player_y) // cell_size
        if next_y >= 0 and not obstacles[next_y][int(player_x) // cell_size]:
            player_y -= player_speed
    if keys[pygame.K_s]:
        next_y = int(player_y + player_height) // cell_size
        if next_y < grid_size and not obstacles[next_y][int(player_x) // cell_size]:
            player_y += player_speed


    # Draw the game objects
    window.fill(BLACK)
    
    
    
    # draw player
    pygame.draw.rect(window, (255, 0, 0), (player_x, player_y, player_width, player_height))


    # Calculate the end point of the line based on player's direction
    line_length = 100  # Adjust the length of the line as needed
    line_end_x = player_x + player_dx * line_length
    line_end_y = player_y + player_dy * line_length

    # Draw the line representing player's perspective
    pygame.draw.line(window, (255, 255, 0), (player_x, player_y), (line_end_x, line_end_y))


    # draw walls to obstacles
    for y in range(grid_size):
        for x in range(grid_size):
            if obstacles[y][x] == 1:
                pygame.draw.rect(window, WHITE, (x * cell_size, y * cell_size, cell_size, cell_size))
                pygame.draw.rect(window, GREY, (x * cell_size, y * cell_size, cell_size, cell_size), 1)



    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()

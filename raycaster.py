import pygame
import numpy as np

pygame.init()

# set up the game window
worldx, worldy = 600, 600
grid_size = 8
cell_size = min(worldx, worldy) // grid_size
window = pygame.display.set_mode((worldx * 2, worldy))
pygame.display.set_caption("Raycaster")

# colors
BLACK = (0, 0, 0)
WHITE = (255,255,255)
GREY = (220,220,220)
PURPLE = (120, 0, 120)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# player properties
player_width, player_height = cell_size / 4, cell_size / 4
player_x = (worldx - player_width) // 2
player_y = (worldy - player_height) // 2
player_pos = pygame.math.Vector2(player_x,player_y)
player_speed = 15
player_dir = pygame.math.Vector2(1, 0)
player_a = 0


# the blocks on the map
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

num_rays = 60

raycaster_surface = pygame.Surface((worldx, worldy))
raycaster_3d_surface = pygame.Surface((worldx, worldy))

# stuff that keeps the main loop working, but can't be in there
main = True
clock = pygame.time.Clock()

while main:
    # lets you quit
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
        player_dir = pygame.math.Vector2(np.cos(player_a),np.sin(player_a))
    
    if keys[pygame.K_d]:
        next_x = int(player_x + player_width) // cell_size
        if next_x < grid_size and not obstacles[int(player_y) // cell_size][next_x]:
            player_x += player_speed
        
        player_a += 0.1
        if player_a > (2*np.pi):
            player_a -= 2 * np.pi
        player_dir = pygame.math.Vector2(np.cos(player_a),np.sin(player_a))
    
    if keys[pygame.K_w]:
        next_pos = player_pos + player_dir * player_speed
        top_left = next_pos
        top_right = next_pos + pygame.math.Vector2(player_width, 0)
        bottom_left = next_pos + pygame.math.Vector2(0, player_height)
        bottom_right = next_pos + pygame.math.Vector2(player_width, player_height)
        if (
            not obstacles[int(top_left.y) // cell_size][int(top_left.x) // cell_size]
            and not obstacles[int(top_right.y) // cell_size][int(top_right.x) // cell_size]
            and not obstacles[int(bottom_left.y) // cell_size][int(bottom_left.x) // cell_size]
            and not obstacles[int(bottom_right.y) // cell_size][int(bottom_right.x) // cell_size]
        ):
            player_pos = next_pos   

    if keys[pygame.K_s]:
        next_pos = player_pos + player_dir * -player_speed
        top_left = next_pos
        top_right = next_pos + pygame.math.Vector2(player_width, 0)
        bottom_left = next_pos + pygame.math.Vector2(0, player_height)
        bottom_right = next_pos + pygame.math.Vector2(player_width, player_height)
        if (
            not obstacles[int(top_left.y) // cell_size][int(top_left.x) // cell_size]
            and not obstacles[int(top_right.y) // cell_size][int(top_right.x) // cell_size]
            and not obstacles[int(bottom_left.y) // cell_size][int(bottom_left.x) // cell_size]
            and not obstacles[int(bottom_right.y) // cell_size][int(bottom_right.x) // cell_size]
        ):
            player_pos = next_pos   


    raycaster_surface.fill(BLACK)
    raycaster_3d_surface.fill(BLACK)


    line_length = 100  # this line doesn't affect player performance. just helps dev w future changes
    line_end = (player_pos + pygame.math.Vector2(player_width / 2, player_height / 2)) + player_dir * line_length
    distances = []

    
    # raycasting logic
    for i in range(num_rays):
        angle = player_a - np.pi / 6 + (i / num_rays) * np.pi / 3  # adjust the field of view as needed
        ray_dir = pygame.math.Vector2(np.cos(angle), np.sin(angle))

        ray_x = player_pos.x + player_width / 2
        ray_y = player_pos.y + player_height / 2

        cos_ang = player_a - angle

        distance = 0

        while True:
            ray_step_size = player_speed / line_length
            ray_x += ray_dir.x * ray_step_size
            ray_y += ray_dir.y * ray_step_size

            if obstacles[int(ray_y // cell_size)][int(ray_x // cell_size)] == 1:
                break

            distance += 1 * ray_step_size * np.cos(cos_ang) # cos_ang helps reduce fisheye

        distances.append(distance)
        pygame.draw.line(
            raycaster_surface,
            PURPLE,
            (player_pos.x + player_width / 2, player_pos.y + player_height / 2),
            (ray_x, ray_y),
        )

    print(distances)

    # draw walls on the raycaster surface
    for y in range(grid_size):
        for x in range(grid_size):
            if obstacles[y][x] == 1:
                pygame.draw.rect(raycaster_surface, WHITE, (x * cell_size, y * cell_size, cell_size, cell_size))
                pygame.draw.rect(raycaster_surface, GREY, (x * cell_size, y * cell_size, cell_size, cell_size), 1)

    for i in range(num_rays):
        height = (line_length / distances[i]) * (worldy / 2)
        SHADERS = (255-distances[i]/2, 255-distances[i]/2, 255-distances[i]/2)
        pygame.draw.rect(raycaster_3d_surface, SHADERS, (i * (worldx / num_rays), worldy / 2 - height / 2, worldx / num_rays, height))
        # Replaced WHITE with SHADERS



    window.blit(raycaster_surface, (0, 0))
    window.blit(raycaster_3d_surface, (worldx, 0))
    pygame.draw.rect(window, RED, (*player_pos, player_width, player_height))
    pygame.draw.line(window, YELLOW, (player_pos + pygame.math.Vector2(player_width / 2, player_height / 2)), line_end)

    pygame.display.flip()
    clock.tick(60)



pygame.quit()

import sys
import pygame
from pygame import K_d, K_a, K_w, K_s
import math

pygame.init()

size = width, height = 500, 500
black = 0, 0, 0
white = 255, 255, 255

SHIP_W = 24
SHIP_H = 50
MAX_SPEED = 4

screen = pygame.display.set_mode(size)

ship_pos = x, y = [width // 2, height // 2]

relative_ship = [[-SHIP_W // 2, SHIP_H * 2 // 5],
                [SHIP_W // 2, SHIP_H * 2 // 5],
                [0, -SHIP_H * 3 // 5]]

ship_dir = 0
delta_speed = 0
delta_dir = 0
speed = [0, 0]

def move_ship(delta_speed, ship_pos):
    points = []
    rad = -math.radians(ship_dir)
    sx = delta_speed * math.sin(rad)
    sy = delta_speed * math.cos(rad)
    speed[0] -= sx
    speed[1] += sy

    if speed[0] > MAX_SPEED:
        speed[0] = MAX_SPEED
    elif speed[0] < -MAX_SPEED:
        speed[0] = -MAX_SPEED
    if speed[1] > MAX_SPEED:
        speed[1] = MAX_SPEED
    elif speed[1] < -MAX_SPEED:
        speed[1] = -MAX_SPEED

    ship_pos[0] += speed[0]
    ship_pos[1] += speed[1]
    if ship_pos[0] < 0:
        ship_pos[0] += width
    elif ship_pos[0] > width:
        ship_pos[0] -= width
    if ship_pos[1] < 0:
        ship_pos[1] += height
    elif ship_pos[1] > height:
        ship_pos[1] -= height
    for point in relative_ship:
        dx = ship_pos[0] + point[0] * math.cos(rad) - point[1] * math.sin(rad)
        dy = ship_pos[1] + point[1] * math.cos(rad) + point[0] * math.sin(rad)
        points.append([dx, dy])

    pygame.draw.polygon(screen, white, points, 2)
    return(ship_pos)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)

    keys = pygame.key.get_pressed()
    if keys[K_w]:
        delta_speed -= 1
    elif keys[K_s]:
        delta_speed += 1

    if keys[K_a]:
        ship_dir += 1
    elif keys[K_d]:
        ship_dir -= 1

    ship_pos = move_ship(delta_speed, ship_pos)

    delta_dir = 0
    delta_speed = 0

    pygame.display.flip()
    pygame.time.wait(25)

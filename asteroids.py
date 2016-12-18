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

class Ship:

    speed = [0, 0]
    direction = 0
    delta_speed = 0

    def __init__(self, position, width, height, color):
        self.position = position
        self.width = width
        self.height = height
        self.color = color
        self.relative_coord = [[-self.width // 2, self.height * 2 // 5],
                        [self.width // 2, self.height * 2 // 5],
                        [0, -self.height * 3 // 5]]

    def move(self):
        rad = -math.radians(self.direction)
        sx = self.delta_speed * math.sin(rad)
        sy = self.delta_speed * math.cos(rad)
        self.speed[0] -= sx
        self.speed[1] += sy

        if self.speed[0] > MAX_SPEED:
            self.speed[0] = MAX_SPEED
        elif self.speed[0] < -MAX_SPEED:
            self.speed[0] = -MAX_SPEED
        if self.speed[1] > MAX_SPEED:
            self.speed[1] = MAX_SPEED
        elif self.speed[1] < -MAX_SPEED:
            self.speed[1] = -MAX_SPEED

        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]
        if self.position[0] < 0:
            self.position[0] += width
        elif self.position[0] > width:
            self.position[0] -= width
        if self.position[1] < 0:
            self.position[1] += height
        elif self.position[1] > height:
            self.position[1] -= height

    def points(self):
        point_list = []
        rad = -math.radians(self.direction)

        for point in self.relative_coord:
            dx = self.position[0] + point[0] * math.cos(rad) - point[1] * math.sin(rad)
            dy = self.position[1] + point[1] * math.cos(rad) + point[0] * math.sin(rad)
            point_list.append([dx, dy])
        return point_list

    def show(self):
        pygame.draw.polygon(screen, self.color, self.points(), 2)


def game(ship):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        screen.fill(black)

        ship.show()

        ship.delta_speed = 0

        keys = pygame.key.get_pressed()
        if keys[K_w]:
            ship.delta_speed -= 1
        elif keys[K_s]:
            ship.delta_speed += 1

        if keys[K_a]:
            ship.direction += 2
        elif keys[K_d]:
            ship.direction -= 2

        ship.move()

        pygame.display.flip()
        pygame.time.wait(25)

def init():
    ship = Ship([width // 2, height // 2],
                SHIP_W,
                SHIP_H,
                white)
    game(ship)

if __name__ == '__main__':
    init()

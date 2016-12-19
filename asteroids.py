import sys
import pygame
from pygame import K_d, K_a, K_w, K_s, K_SPACE
import math

SIZE = WIDTH, HEIGHT = 500, 500
black = 0, 0, 0
white = 255, 255, 255

SHIP_W = 24
SHIP_H = 50
MAX_SPEED = 4

pygame.init()
screen = pygame.display.set_mode(SIZE)

class Space_Object():
    speed = [0, 0]
    direction = 0
    delta_speed = 0
    speed_limit = MAX_SPEED

    def __init__(self, position, width, height, color):
        self.position = position
        self.width = width
        self.height = height
        self.color = color

    def move(self):
        rad = -math.radians(self.direction)
        sx = self.delta_speed * math.sin(rad)
        sy = self.delta_speed * math.cos(rad)
        self.speed[0] -= sx
        self.speed[1] += sy

        if self.speed[0] > self.speed_limit:
            self.speed[0] = self.speed_limit
        elif self.speed[0] < -self.speed_limit:
            self.speed[0] = -self.speed_limit
        if self.speed[1] > self.speed_limit:
            self.speed[1] = self.speed_limit
        elif self.speed[1] < -self.speed_limit:
            self.speed[1] = -self.speed_limit

        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]
        if self.position[0] < 0 - 10:
            self.position[0] += WIDTH
        elif self.position[0] > WIDTH + 10:
            self.position[0] -= WIDTH
        if self.position[1] < 0 - 10:
            self.position[1] += HEIGHT
        elif self.position[1] > HEIGHT + 10:
            self.position[1] -= HEIGHT

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

class Ship(Space_Object):
    shots = []
    shot_limit = 10
    shot_delay = 0

    def __init__(self, position, width, height, color):
        Space_Object.__init__(self, position, width, height, color)
        self.relative_coord = [[-self.width // 2, self.height * 2 // 5],
                        [self.width // 2, self.height * 2 // 5],
                        [0, -self.height * 3 // 5]]

    def shoot(self):
        origin = self.points()[2]
        if self.shot_delay == 0:
            if len(self.shots) < 10:
                self.shots.append(Shot(origin, self.direction, self.color))
                self.shot_delay = 8
        else:
            self.shot_delay -= 1

    def remove_shots(self):
        for i in range(len(self.shots)):
            if self.shots[i].position[0] < 0 or self.shots[i].position[1] < 0:
                del self.shots[i]
                break
            elif self.shots[i].position[0] > WIDTH or self.shots[i].position[1] > HEIGHT:
                del self.shots[i]
                break

class Shot(Space_Object):

    width = 2
    height = 6
    speed_limit = MAX_SPEED + 4

    def __init__(self, position, direction, color):
        self.position = position
        self.direction = direction
        self.color = color
        rad = -math.radians(self.direction)
        self.speed = [self.speed_limit * math.sin(rad),
                    -self.speed_limit * math.cos(rad)]
        self.relative_coord = [[0, 0], [0, self.height]]

    def show(self):
        points = self.points()
        pygame.draw.line(screen, self.color, points[0], points[1], self.width)


def game(ship):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        screen.fill(black)

        ship.show()
        ship.remove_shots()

        for shot in ship.shots:
            shot.show()
            shot.move()

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

        if keys[K_SPACE]:
            ship.shoot()

        ship.move()

        pygame.display.flip()
        pygame.time.wait(25)

def init():

    ship = Ship([WIDTH // 2, HEIGHT // 2],
                SHIP_W,
                SHIP_H,
                white)

    game(ship)

if __name__ == '__main__':
    init()

import sys
import pygame
from pygame import K_d, K_a, K_w, K_s, K_SPACE
import math
import random

SIZE = WIDTH, HEIGHT = 500, 500
black = 0, 0, 0
white = 255, 255, 255

SHIP_W = 12
SHIP_H = 25
MAX_SPEED = 3
ASTEROID_LIMIT = 5

pygame.init()
screen = pygame.display.set_mode(SIZE)
font = pygame.font.SysFont('monospace', 25)

asteroids = []
explosions = []
acceleration = 0.5
turn_speed = 5


class Space_Object:
    speed = [0, 0]
    direction = 0
    delta_speed = 0
    speed_limit = MAX_SPEED
    rotation = 0

    def __init__(self, position, width, height, color):
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.width = width
        self.height = height
        self.color = color

    def move(self):
        rad = -math.radians(self.direction + self.rotation)
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

        self.x += self.speed[0]
        self.y += self.speed[1]
        if self.x < 0 - 10:
            self.x += WIDTH
        elif self.x > WIDTH + 10:
            self.x -= WIDTH
        if self.y < 0 - 10:
            self.y += HEIGHT
        elif self.y > HEIGHT + 10:
            self.y -= HEIGHT
        self.position = [self.x, self.y]

    def points(self):
        point_list = []
        rad = -math.radians(self.direction)

        for point in self.relative_coord:
            dx = self.x + point[0] * math.cos(rad) - point[1] * math.sin(rad)
            dy = self.y + point[1] * math.cos(rad) + point[0] * math.sin(rad)
            point_list.append([dx, dy])
        return point_list

    def show(self):
        pygame.draw.polygon(screen, self.color, self.points(), 2)

    def collision(self, item):
        min_safe_x = self.width / 2 + item.width / 4
        min_safe_y = self.height / 2 + item.height / 4
        min_safe_dist = math.sqrt(min_safe_x ** 2 + min_safe_y ** 2)
        abs_x = abs(self.x - item.x)
        abs_y = abs(self.y - item.y)
        abs_dist = math.sqrt(abs_x ** 2 + abs_y ** 2)
        if abs_dist < min_safe_dist:
            return True
        """
        if item.x >= self.x - self.width / 2:
            if item.x <= self.x + self.width / 2:
                if item.y >= self.y - self.height / 2:
                    if item.y <= self.y + self.height / 2:
                        return True
                        """

    def explode(self):
        explosion = []
        direction = random.randint(0, 365)
        debris_amount = 5
        for i in range(debris_amount):
            explosion.append(Debris(self.position, direction, white))
            direction += 73
        explosions.append(explosion)


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
            if self.shots[i].x < 0 or self.shots[i].y < 0:
                del self.shots[i]
                break
            elif self.shots[i].x > WIDTH or self.shots[i].y > HEIGHT:
                del self.shots[i]
                break


class Shot(Space_Object):

    width = 2
    height = 6
    speed_limit = MAX_SPEED + 4

    def __init__(self, position, direction, color):
        Space_Object.__init__(self, position, self.width, self.height, color)
        self.direction = direction
        rad = -math.radians(self.direction)
        self.speed = [self.speed_limit * math.sin(rad),
                      -self.speed_limit * math.cos(rad)]
        self.relative_coord = [[0, 0], [0, self.height]]

    def show(self):
        points = self.points()
        pygame.draw.line(screen, self.color, points[0], points[1], self.width)


class Asteroid(Space_Object):

    def __init__(self, position, color):
        ASTEROID_SHAPES = [
                        [[-self.width / 2, -self.height / 3],
                         [-self.width / 3, -self.height / 2],
                         [self.width / 6, -self.height / 2],
                         [self.width / 2, -self.height / 6],
                         [self.width / 2, self.height / 3],
                         [self.width / 3, self.height / 2],
                         [self.width / 6, self.height / 2],
                         [-self.width / 6, self.height / 6],
                         [-self.width / 3, self.height / 6],
                         [-self.width / 2, 0]],
                        [[0, self.height / 2],
                         [self.width / 6, self.height / 2],
                         [self.width / 3, self.height / 3],
                         [self.width / 3, self.height / 6],
                         [self.width / 2, 0],
                         [self.width / 2, -self.height / 6],
                         [self.width / 3, -self.height / 3],
                         [self.width / 6, -self.height / 3],
                         [0, -self.height / 2],
                         [-self.width / 6, -self.height / 2],
                         [-self.width / 6, -self.height / 3],
                         [-self.width / 2, 0],
                         [-self.width / 2, self.height / 6],
                         [-self.width / 3, self.height / 3],
                         [-self.width / 6, self.height / 3]]
                        ]

        if position is None:
            start = random.choice([1, 2, 3, 4])
            if start == 1:
                position = [0, random.randint(0, HEIGHT)]
            elif start == 2:
                position = [WIDTH, random.randint(0, HEIGHT)]
            elif start == 3:
                position = [random.randint(0, WIDTH), 0]
            else:
                position = [random.randint(0, WIDTH), HEIGHT]

        Space_Object.__init__(self, position, self.width, self.height, color)

        self.speed = random.randint(1, self.speed_limit)
        self.direction = random.randint(0, 365)

        self.relative_coord = ASTEROID_SHAPES[random.randint(0, len(ASTEROID_SHAPES) - 1)] # noqa

        rad = -math.radians(self.direction)
        self.speed = [self.speed_limit * math.sin(rad),
                      -self.speed_limit * math.cos(rad)]

        self.rotation = random.randint(-20, 20)

    def break_apart(self):
        self.explode()


class Big_Asteroid(Asteroid):
    height = 75
    width = 75
    speed_limit = MAX_SPEED - 2

    def __init__(self, position, color):
        Asteroid.__init__(self, position, color)

    def break_apart(self):
        for i in range(3):
            asteroids.append(Small_Asteroid(self.position, self.color))
        self.explode()


class Small_Asteroid(Asteroid):
    height = 20
    width = 20
    speed_limit = MAX_SPEED - 1

    def __init__(self, position, color):
        Asteroid.__init__(self, position, color)


class Debris(Shot):
    width = 1

    def __init__(self, position, direction, color):
        self.height = random.randint(1, 20)
        Shot.__init__(self, position, direction, color)
        self.timer = random.randint(5, 15)


ship = Ship([WIDTH // 2, HEIGHT // 2],
            SHIP_W,
            SHIP_H,
            white)


def collision_check(asteroids, shots, score):
    collisions = []
    for i in range(len(asteroids)):
        for j in range(len(shots)):
            if asteroids[i].collision(shots[j]):
                asteroids[i].break_apart()
                if isinstance(asteroids[i], Big_Asteroid):
                    score += 100
                else:
                    score += 50
                del asteroids[i]
                del shots[j]
                return score

    for asteroid in asteroids:
        if ship.collision(asteroid):
            ship.explode()
            game_over()

    return score


def handle_explosions():
    for explosion in explosions:
        for i in range(len(explosion)):
            if explosion[i].timer <= 0:
                del explosion[i]
                return
            else:
                explosion[i].timer -= 1


def handle_score(score):
    display_score = font.render(str(score), False, white)
    width, height = font.size(str(score))
    screen.blit(display_score, (WIDTH - width - 10, HEIGHT - height - 10))


def game_over():
    ship.x = WIDTH // 2
    ship.y = HEIGHT // 2


def game(score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(black)

        handle_score(score)

        ship.show()
        ship.remove_shots()

        for shot in ship.shots:
            shot.show()
            shot.move()

        ship.delta_speed = 0

        keys = pygame.key.get_pressed()

        if keys[K_w]:
            ship.delta_speed -= acceleration
        elif keys[K_s]:
            ship.delta_speed += acceleration

        if keys[K_a]:
            ship.direction += turn_speed
        elif keys[K_d]:
            ship.direction -= turn_speed

        if keys[K_SPACE]:
            ship.shoot()

        ship.move()

        if len(asteroids) < ASTEROID_LIMIT:
            if random.choice([True, False]):
                asteroids.append(Big_Asteroid(None, white))

        for asteroid in asteroids:
            asteroid.move()
            asteroid.show()

        score = collision_check(asteroids, ship.shots, score)

        handle_explosions()

        for explosion in explosions:
            for debris in explosion:
                debris.move()
                debris.show()

        pygame.display.flip()
        pygame.time.wait(25)


if __name__ == '__main__':
    score = 0
    game(score)

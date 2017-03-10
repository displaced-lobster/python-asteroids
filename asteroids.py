#!/usr/bin/python3
import math
import pygame
import random
import sys

from pygame import K_d, K_a, K_w, K_s, K_SPACE

SIZE = WIDTH, HEIGHT = 500, 500
BLACK = 0, 0, 0
WHITE = 255, 255, 255

SHIP_W = 12
SHIP_H = 25
MAX_SPEED = 3
ASTEROID_LIMIT = 2


class Game_Space:
    """Initiates and holds all variables needed for the game to run. Also
    includes all methods for changing the state of the game: move, shoot, etc.
    """

    def __init__(self):
        # Sets screen, font, and generates player's ship
        self.screen = pygame.display.set_mode(SIZE)
        self.font = pygame.font.SysFont('monospace', 25)
        self.ship = Ship([WIDTH // 2, HEIGHT // 2], SHIP_W, SHIP_H)
        self.asteroids = []
        self.explosions = []
        self.score = 0
        self.big_asteroids = 0
        self.satelite = None
        self.target_score = 1000

    def collision_check(self):
        # Collision check for all objects in the GameSpace
        if self.satelite is not None:
            for i in range(len(self.ship.shots)):
                if self.satelite.collision(self.ship.shots[i]):
                    self.score += 850
                    del self.ship.shots[i]
                    self.satelite.explode()
                    self.satelite = None
                    return

        for i in range(len(self.asteroids)):
            for j in range(len(self.ship.shots)):
                if self.asteroids[i].collision(self.ship.shots[j]):
                    self.asteroids[i].break_apart()
                    if isinstance(self.asteroids[i], Big_Asteroid):
                        self.score += 100
                        self.big_asteroids -= 1
                    else:
                        self.score += 50
                    del self.asteroids[i]
                    del self.ship.shots[j]
                    return

        for asteroid in self.asteroids:
            if self.ship.collision(asteroid):
                self.ship.explode()
                self.game_over()

    def handle_explosions(self):
        # Cleans up explosion debris
        for explosion in self.explosions:
            for i in range(len(explosion)):
                if explosion[i].timer <= 0:
                    del explosion[i]
                    return
                else:
                    explosion[i].timer -= 1

    def update_score(self):
        # Updates the score displayed on the screen
        display_score = self.font.render(str(self.score), False, WHITE)
        width, height = self.font.size(str(self.score))
        self.screen.blit(display_score, (WIDTH - width - 10,
                                         HEIGHT - height - 10))

    def game_over(self):
        # Game over operation
        # TODO: End game, display high scores
        self.ship.x = WIDTH // 2
        self.ship.y = HEIGHT // 2

    def draw_all(self):
        # Draw all objects in the GameSpace
        self.ship.draw()
        for asteroid in self.asteroids:
            asteroid.draw()
        for shot in self.ship.shots:
            shot.draw()
        for explosion in self.explosions:
            for debris in explosion:
                debris.draw()
        if self.satelite is not None:
            self.satelite.draw()

    def move_all(self):
        # Move all objects in the GameSpace
        self.ship.move()
        for asteroid in self.asteroids:
            asteroid.move()
        for shot in self.ship.shots:
            shot.move()
        for explosion in self.explosions:
            for debris in explosion:
                debris.move()
        if self.satelite is not None:
            self.satelite.move()

    def spawn_asteroids(self):
        # Spawns BigAsteroids if currently under the limit
        if self.big_asteroids < ASTEROID_LIMIT:
            if random.choice([True, False]):
                self.asteroids.append(Big_Asteroid(None))
                self.big_asteroids += 1

    def spawn_satelite(self):
        # Spawns Satelite object if target score is met, increases target each
        # spawn
        if self.score > self.target_score:
            if self.satelite is None:
                self.satelite = Satelite()
                self.target_score *= 3
            elif self.satelite.x < 0:
                self.satelite = None

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill(BLACK)
            self.update_score()
            self.draw_all()
            self.ship.control(pygame.key.get_pressed())
            self.collision_check()
            self.move_all()
            self.spawn_asteroids()
            self.spawn_satelite()
            self.handle_explosions()
            self.ship.remove_shots()
            pygame.display.flip()
            pygame.time.wait(25)


class Menu:
    """Menu object to be displayed before and after every game. Work in
    progress, not yet implmented.
    """

    def __init__(self):
        # Set font and grab current pygame surface
        self.font_inactive = pygame.font.SysFont('monospace', 45)
        self.font_active = pygame.font.SysFont('monospace', 60)
        self.screen = pygame.display.get_surface()
        self.options = [['New Game', True], ['Exit', False]]
        self.spacing = 10
        self.padding_top = 100
        self.padding_left = 80

    def make_menu(self):
        # Draw the menu on the screen
        x = self.padding_left
        y = self.padding_top
        for menu_item in self.options:
            option = menu_item[0]
            active = menu_item[1]
            if active:
                button = self.font_active.render(option, False, WHITE)
                width, height = self.font_active.size(option)
            else:
                button = self.font_inactive.render(option, False, WHITE)
                width, height = self.font_inactive.size(option)
            self.screen.blit(button, (x, y))
            y += height + self.spacing

    def action(self, keys):
        # Get user input and change active menu item or do menu action.
        for i in range(len(self.options)):
            if self.options[i][1]:
                pos = i
        if keys[K_w]:
            if pos > 0:
                self.options[pos][1] = False
                self.options[pos - 1][1] = True
        elif keys[K_s]:
            if pos < len(self.options) - 1:
                self.options[pos][1] = False
                self.options[pos + 1][1] = True
        elif keys[K_SPACE]:
            if self.options[pos][0] == 'New Game':
                game.run_game()
            elif self.options[pos][0] == 'Exit':
                sys.exit()


class Space_Object:
    """Base object for all other objects. Includes draw and move methods."""

    def __init__(self, position, width, height):
        # Requires position, width, and height as inputs. Gets the current
        # pygame surface
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.width = width
        self.height = height
        self.screen = pygame.display.get_surface()
        self.speed = [0, 0]
        self.direction = 0
        self.delta_speed = 0
        self.speed_limit = MAX_SPEED
        self.rotation = 0
        self.color = WHITE
        self.screen_wrap = True

    def move(self):
        # Adjust the objects position variables depending on it's speed and
        # direction
        rad = -math.radians(self.direction + self.rotation)
        sx = self.delta_speed * math.sin(rad)
        sy = self.delta_speed * math.cos(rad)
        self.delta_speed = 0
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

        if self.screen_wrap:
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
        # Returns the objects relative shape adjusted for orientation and
        # position
        point_list = []
        rad = -math.radians(self.direction)

        for point in self.relative_coord:
            dx = self.x + point[0] * math.cos(rad) - point[1] * math.sin(rad)
            dy = self.y + point[1] * math.cos(rad) + point[0] * math.sin(rad)
            point_list.append([dx, dy])
        return point_list

    def draw(self):
        # Draws object on the screen
        pygame.draw.polygon(self.screen, self.color, self.points(), 2)

    def collision(self, item):
        # Determines if a collision has taken place between two objects using
        # their positions, widths, and heights
        min_safe_x = self.width / 2 + item.width / 4
        min_safe_y = self.height / 2 + item.height / 4
        min_safe_dist = math.sqrt(min_safe_x ** 2 + min_safe_y ** 2)
        abs_x = abs(self.x - item.x)
        abs_y = abs(self.y - item.y)
        abs_dist = math.sqrt(abs_x ** 2 + abs_y ** 2)
        if abs_dist < min_safe_dist:
            return True

    def explode(self):
        # Create an explosion effect be generating debris
        explosion = []
        direction = random.randint(0, 365)
        debris_amount = 5
        for i in range(debris_amount):
            explosion.append(Debris(self.position, direction))
            direction += 73
        game.explosions.append(explosion)


class Ship(Space_Object):
    """The user controlled space ship. Has special methods shoot, control, and
    remove_shots. Stores the number of ship shots currently active and applies
    a shot limit. Holds the ships limiting factors: acceleration, turn speed.
    """

    def __init__(self, position, width, height):
        # Initialize SpaceObject and set object shape
        Space_Object.__init__(self, position, width, height)
        self.relative_coord = [[-self.width // 2, self.height * 2 // 5],
                               [0, self.height // 5],
                               [self.width // 2, self.height * 2 // 5],
                               [0, -self.height * 3 // 5]]
        self.shots = []
        self.shot_limit = 10
        self.shot_delay = 0
        self.acceleration = 2
        self.turn_speed = 5

    def shoot(self):
        # Generate a shot from the front of the ship
        origin = self.points()[3]
        if self.shot_delay == 0:
            if len(self.shots) < 10:
                self.shots.append(Shot(origin, self.direction))
                self.shot_delay = 8
        else:
            self.shot_delay -= 1

    def remove_shots(self):
        # Cleans up shots that have moveed off screen
        for i in range(len(self.shots)):
            if self.shots[i].x < 0 or self.shots[i].y < 0:
                del self.shots[i]
                break
            elif self.shots[i].x > WIDTH or self.shots[i].y > HEIGHT:
                del self.shots[i]
                break

    def control(self, keys):
        # Defines the result from user input and applies it
        if keys[K_w]:
            self.delta_speed -= self.acceleration
        elif keys[K_s]:
            self.delta_speed += self.acceleration

        if keys[K_a]:
            self.direction += self.turn_speed
        elif keys[K_d]:
            self.direction -= self.turn_speed

        if keys[K_SPACE]:
            self.shoot()


class Shot(Space_Object):
    """Shot object, fired from ship and can collide with other space objects.
    """

    def __init__(self, position, direction):
        # Calculates speed on initiation
        self.width = 2
        self.height = 6
        self.speed_limit = MAX_SPEED + 4
        self.screen_wrap = False
        Space_Object.__init__(self, position, self.width, self.height)
        self.direction = direction
        rad = -math.radians(self.direction)
        self.speed = [self.speed_limit * math.sin(rad),
                      -self.speed_limit * math.cos(rad)]
        self.relative_coord = [[0, 0], [0, self.height]]

    def draw(self):
        # Drawn as a line instead of the default polygon
        points = self.points()
        pygame.draw.line(self.screen,
                         self.color,
                         points[0],
                         points[1],
                         self.width)


class Asteroid(Space_Object):
    """Base object for asteroids. Includes different shapes and break apart
    methods for asteroid destruction.
    """

    def __init__(self, position):
        # Randomly chooses asteroid from collection of shapes.
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

        # Randomly choose start position if position is not inherited
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

        Space_Object.__init__(self, position, self.width, self.height)

        self.speed = random.randint(1, self.speed_limit)
        self.direction = random.randint(0, 365)

        self.relative_coord = ASTEROID_SHAPES[random.randint(0, len(ASTEROID_SHAPES) - 1)] # noqa

        rad = -math.radians(self.direction)
        self.speed = [self.speed_limit * math.sin(rad),
                      -self.speed_limit * math.cos(rad)]

        self.rotation = random.randint(-20, 20)

    def break_apart(self):
        # Default break_apart calls base explode method
        self.explode()


class Big_Asteroid(Asteroid):
    """Big asteroids are slow and break apart into small asteroids."""

    def __init__(self, position):
        self.height = 75
        self.width = 75
        self.speed_limit = MAX_SPEED - 2
        Asteroid.__init__(self, position)

    def break_apart(self):
        for i in range(random.randint(1, 4)):
            game.asteroids.append(Small_Asteroid(self.position))
        self.explode()


class Small_Asteroid(Asteroid):
    """Small asteroids are fast and are destroyed on collision with a shot."""

    height = 20
    width = 20
    speed_limit = MAX_SPEED - 1

    def __init__(self, position):
        Asteroid.__init__(self, position)


class Debris(Shot):
    """Debris uses the shot class to show destruction. Incldues a timer
    variable to be deleted when timer hits zero.
    """

    def __init__(self, position, direction):
        self.width = 1
        self.height = random.randint(1, 20)
        Shot.__init__(self, position, direction)
        self.timer = random.randint(5, 15)


class Satelite(Space_Object):
    """Special, high value target. Moves from right to left across the middle
    of the screen. A more complex shape than the other sopace objects.
    """

    def __init__(self):
        Space_Object.__init__(self, [WIDTH, HEIGHT // 2], 12, 10)
        self.speed = [-MAX_SPEED, 0]
        self.screen_wrap = False

    def draw(self):
        # Draw method includes a circle and three lines.
        line_1 = [[self.x, self.y - self.height // 4],
                  [self.x + self.width * 3 // 4, self.y - self.height // 2]]
        line_2 = [[self.x + self.width // 4, self.y],
                  [self.x + self.width * 3 // 4, self.y]]
        line_3 = [[self.x, self.y + self.height // 4],
                  [self.x + self.width * 3 // 4, self.y + self.height // 2]]
        pygame.draw.circle(self.screen,
                           self.color,
                           (int(self.x), int(self.y)),
                           self.width // 4)
        pygame.draw.line(self.screen, self.color, line_1[0], line_1[1], 1)
        pygame.draw.line(self.screen, self.color, line_2[0], line_2[1], 1)
        pygame.draw.line(self.screen, self.color, line_3[0], line_3[1], 1)


def main(game):
    menu = Menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        game.screen.fill(BLACK)
        menu.make_menu()
        menu.action(pygame.key.get_pressed())

        pygame.display.flip()
        pygame.time.wait(25)


if __name__ == '__main__':
    pygame.init()
    game = Game_Space()
    main(game)

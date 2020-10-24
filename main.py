import pygame as pg
import math as m
from random import randint
from abc import ABC, abstractmethod

RES = WIDTH, HEIGHT = 1300, 700
FPS = 120
G = 6  # gravity constant
planets = list()  # list o the planets

pg.init()
done = False
surface = pg.display.set_mode(RES, pg.RESIZABLE)
clock = pg.time.Clock()


def event_overview(events):
    global done
    for event in events:
        if event.type == pg.QUIT:
            done = True


class Body(ABC):

    @abstractmethod
    def __init__(self, mass, x, y, r):
        self.m = mass
        self.x, self.y = x, y
        self.r = r
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def draw(self):
        pg.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.r)


class MovementBody(Body):
    standard_radius = 5

    def __init__(self, mass, x, y, V=0.0, ang=0, r=standard_radius):
        super(MovementBody, self).__init__(mass, x, y, r)
        self.Vx, self.Vy = V * m.cos(ang / 180 * m.pi), V * m.sin(ang / 180 * m.pi)
        self.tracer = [(0, 0) for i in range(1001)]
        self.tracer[0] = (x, y)
        self.it = 1

    def move(self, p=None, lenght=0):
        acceleration = a(p.m, lenght)
        k = lenght / acceleration
        self.Vx += (p.x - self.x) / k
        self.Vy += (p.y - self.y) / k
        self.x += self.Vx
        self.y += self.Vy

    def draw(self):
        for x, y in self.tracer:
            pg.draw.circle(surface, (255 - self.color[0], 255 - self.color[1], 255 - self.color[2]), (x, y), 1)
        pg.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.r)
        self.tracer[self.it] = (int(self.x), int(self.y))
        if self.it == 1000:
            self.it = -1
        self.it += 1


class StaticBody(Body):
    standard_radius = 15

    def __init__(self, mass, x, y, r=standard_radius):
        super(StaticBody, self).__init__(mass, x, y, r)

    def move(self):
        pass

    def draw(self):
        super(StaticBody, self).draw()


def a(mass, lenght):
    return G * mass / lenght ** 2


def r(p1, p2):
    return (abs(p1.x - p2.x) ** 2 + abs(p1.y - p2.y) ** 2) ** 0.5


def calculation_and_drawing(planets):
    for i in range(-1, len(planets) - 1):
        if type(planets[i]) == StaticBody:
            continue
        distance = r(planets[i], planets[i + 1])
        planets[i].move(planets[i + 1], distance)
    for planet in planets:
        planet.draw()


def main_loop():
    global done
    planets.append(StaticBody(333, WIDTH // 2, HEIGHT // 2))
    planets.append(MovementBody(1, WIDTH // 2, HEIGHT // 2 + 150, 3.5, 0))
    while not done:
        surface.fill(pg.Color("black"))
        event_overview(pg.event.get())
        calculation_and_drawing(planets)
        # pg.display.set_caption(str(distance))
        pg.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main_loop()

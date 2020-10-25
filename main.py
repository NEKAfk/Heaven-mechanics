import pygame as pg
from random import randint
from abc import ABC, abstractmethod

RES = WIDTH, HEIGHT = 1300, 700
FPS = 120
G_move = 1
G_static_0D = 0.000003
G_static_1D = 0.001
G_static_2D = 0.1
G_static_3D = 6
planets = list()  # list o the planets
tracer_num = 1000

pg.init()
pg.display.set_caption("Heaven")
star = pg.image.load("Bodies/sun.png")
earth = pg.image.load("Bodies/earth.png")
saturn = pg.image.load("Bodies/saturn.png")
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
    def __init__(self, mass, x, y):
        self.m = mass
        self.x, self.y = x, y
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def draw(self):
        pg.draw.circle(surface, self.color, (int(self.x), int(self.y)), 15)


class MovementBody(Body, pg.sprite.Sprite):
    standard_radius = 10

    def __init__(self, mass, x, y, Vx=0.0, Vy=0.0, image=None):
        Body.__init__(self, mass, x, y)
        pg.sprite.Sprite.__init__(self)
        self.image = image
        if image != None:
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = x - image.get_width() // 2, y - image.get_height() // 2
        self.Vx, self.Vy = Vx, Vy
        self.tracer = [(0, 0) for i in range(tracer_num + 1)]
        self.tracer[0] = (x, y)
        self.it = 1

    def __add__(self, other):
        self.r = (self.r**2 + other.r**2)**0.5
        self.m += other.m
        if type(other) == MovementBody:
            self.Vx += other.Vx
            self.Vy += other.Vy
        return self

    def move(self, p=None, lenght=0):
        G = G_move if type(p) == MovementBody else G_static_3D
        self.Vx += G * p.m * (p.x - self.x) / lenght**3
        self.Vy += G * p.m * (p.y - self.y) / lenght**3

        # G = G_move if type(p) == MovementBody else G_static_2D
        # self.Vx += G * p.m * (p.x - self.x) / lenght**2
        # self.Vy += G * p.m * (p.y - self.y) / lenght**2

        # G = G_move if type(p) == MovementBody else G_static_1D
        # self.Vx += G * p.m * (p.x - self.x) / lenght ** 1
        # self.Vy += G * p.m * (p.y - self.y) / lenght ** 1

        # G = G_move if type(p) == MovementBody else G_static_0D
        # self.Vx += G * p.m * (p.x - self.x)
        # self.Vy += G * p.m * (p.y - self.y)

    def draw(self):
        self.x += self.Vx
        self.y += self.Vy
        for x, y in self.tracer:
            pg.draw.circle(surface, (255 - self.color[0], 255 - self.color[1], 255 - self.color[2]), (x, y), 1)
        self.tracer[self.it] = (int(self.x), int(self.y))
        if self.it == tracer_num:
            self.it = -1
        self.it += 1
        if self.image == None:
            pg.draw.circle(surface, self.color, (int(self.x), int(self.y)), 10)
        else:
            self.rect.left = self.x - self.image.get_width() // 2
            self.rect.top = self.y - self.image.get_height() // 2
            surface.blit(self.image, self.rect)



class StaticBody(Body, pg.sprite.Sprite):

    def __init__(self, mass, x, y, image=None):
        Body.__init__(self, mass, x, y)
        pg.sprite.Sprite.__init__(self)
        self.image = image
        if image != None:
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = x - image.get_width() // 2, y - image.get_height() // 2

    def move(self):
        pass

    def draw(self):
        if self.image == None:
            Body.draw(self)
        else:
            surface.blit(self.image, self.rect)


def r(p1, p2):
    return (abs(p1.x - p2.x) ** 2 + abs(p1.y - p2.y) ** 2) ** 0.5


def calculation_and_drawing(planets):
    for p1 in planets:
        for p2 in planets[0:planets.index(p1)] + planets[planets.index(p1) + 1:]:
            try:
                if type(p1) == StaticBody:
                    break
                distance = r(p1, p2)
                if distance < 5:
                    planets[planets.index(p1)] = p1 + p2
                    planets.remove(p2)
                    continue
                p1.move(p2, distance)
            except Exception:
                break
    for planet in planets:
        planet.draw()


def main_loop():
    global done
    planets.append(StaticBody(250, WIDTH // 2, HEIGHT // 2, star))
    planets.append(MovementBody(1, WIDTH // 2, HEIGHT // 2 + 300, 2.25, 0, saturn))
    planets.append(MovementBody(10, WIDTH // 2 - 150, HEIGHT // 2, 0, 2.25, earth))
    while not done:
        surface.fill(pg.Color("black"))
        event_overview(pg.event.get())
        calculation_and_drawing(planets)
        pg.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main_loop()

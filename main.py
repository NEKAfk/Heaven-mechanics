import pygame as pg
from random import randint
from abc import ABC, abstractmethod
import contextlib
from mywidgets import Background, Button, TextInput

RES = WIDTH, HEIGHT = 1400, 700
FPS = 120
G_0D = 0.000003
G_1D = 0.001
G_2D = 0.075
G_3D = 6
planets = list()  # list of the planets
buttons = list()  # list of the buttons
text_inputs = list()  # list of the text_inputs
TRACER_NUM = 100
CLICK_POS_DOWN = (0, 0)
CLICK_POS_UP = (0, 0)
FLAG = False

pg.init()
screen = pg.display.set_mode(RES, pg.RESIZABLE)
pg.display.set_caption("Heaven")
DONE = False
RESET = False
clock = pg.time.Clock()

bg_image = pg.image.load("bg.png")
bg = Background(screen, bg_image)
star = pg.image.load("Bodies/sun.png")
earth = pg.image.load("Bodies/earth.png")
saturn = pg.image.load("Bodies/saturn.png")


def event_overview(events, btns, txt_inputs):
    global DONE, RESET, FLAG
    global CLICK_POS_DOWN, CLICK_POS_UP
    for event in events:
        if event.type == pg.QUIT:
            DONE = RESET = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            CLICK_POS_DOWN = pg.mouse.get_pos()
            FLAG = False
            click_buttons(btns)
            click_text_inputs(txt_inputs)
        elif event.type == pg.MOUSEBUTTONUP:
            global CLICK_POS_UP
            CLICK_POS_UP = pg.mouse.get_pos()
            spawn_bodies()
        user_input(event, txt_inputs)


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
        pg.draw.circle(screen, self.color, (int(self.x), int(self.y)), 15)


class MovementBody(Body, pg.sprite.Sprite):
    standard_radius = 10

    def __init__(self, mass, x, y, Vx=0.0, Vy=0.0, image=None):
        Body.__init__(self, mass, x, y)
        pg.sprite.Sprite.__init__(self)
        self.image = image
        if image is not None:
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = x - image.get_width() // 2, y - image.get_height() // 2
        self.Vx, self.Vy = Vx, Vy
        self.tracer = [(x, y)]
        self.it = 0

    def __add__(self, other):
        self.m += other.m
        if type(other) == MovementBody:
            self.Vx = (self.Vx * self.m + other.Vx * other.m) / (self.m + other.m)
            self.Vy = (self.Vy * self.m + other.Vy * other.m) / (self.m + other.m)
        else:
            self.Vx *= self.m / (self.m + other.m)
            self.Vy *= self.m / (self.m + other.m)
        self.m += other.m
        return self

    def move(self, p=None, lenght=0):
        G = G_3D
        self.Vx += G * p.m * (p.x - self.x) / lenght ** 3
        self.Vy += G * p.m * (p.y - self.y) / lenght ** 3

        # G = G_2D
        # self.Vx += G * p.m * (p.x - self.x) / lenght**2
        # self.Vy += G * p.m * (p.y - self.y) / lenght**2

        # G = G_1D
        # self.Vx += G * p.m * (p.x - self.x) / lenght ** 1
        # self.Vy += G * p.m * (p.y - self.y) / lenght ** 1

        # G = G_0D
        # self.Vx += G * p.m * (p.x - self.x)
        # self.Vy += G * p.m * (p.y - self.y)

    def draw(self):
        self.x += self.Vx
        self.y += self.Vy
        if len(self.tracer) < TRACER_NUM:
            self.tracer.append((self.x, self.y))
        elif self.it < TRACER_NUM:
            self.tracer[self.it] = (self.x, self.y)
            self.it += 1
        else:
            self.it = 0
        for x, y in self.tracer:
            pg.draw.circle(screen, (255 - self.color[0], 255 - self.color[1], 255 - self.color[2]), (int(x), int(y)), 1)
        if self.image is None:
            pg.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10)
        else:
            self.rect.left = self.x - self.image.get_width() // 2
            self.rect.top = self.y - self.image.get_height() // 2
            screen.blit(self.image, self.rect)


class StaticBody(Body, pg.sprite.Sprite):

    def __init__(self, mass, x, y, image=None):
        Body.__init__(self, mass, x, y)
        pg.sprite.Sprite.__init__(self)
        self.image = image
        if image is not None:
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = x - image.get_width() // 2, y - image.get_height() // 2

    def move(self):
        pass

    def draw(self):
        if self.image is None:
            Body.draw(self)
        else:
            screen.blit(self.image, self.rect)


def r(p1, p2):
    return (abs(p1.x - p2.x) ** 2 + abs(p1.y - p2.y) ** 2) ** 0.5


def calculation_moves(bodies):
    for b1 in bodies:
        for b2 in bodies[0:bodies.index(b1)] + bodies[bodies.index(b1) + 1:]:
            with contextlib.suppress(Exception):
                if type(b1) == StaticBody:
                    break
                distance = r(b1, b2)
                if distance < 15:
                    bodies[bodies.index(b1)] = b1 + b2
                    bodies.remove(b2)
                    continue
                b1.move(b2, distance)


def draw_bodies(bodies):
    for body in bodies:
        body.draw()


def draw_buttons(btns):
    for btn in btns:
        btn.draw()


def click_buttons(btns):
    global FLAG
    for btn in btns:
        FLAG = FLAG or btn.click(CLICK_POS_DOWN)


def draw_text_inputs(txt_inputs):
    for txt_input in txt_inputs:
        txt_input.draw()


def click_text_inputs(txt_inputs):
    global FLAG
    for txt_input in txt_inputs:
        FLAG = FLAG or txt_input.click(CLICK_POS_DOWN)


def user_input(event, txt_inputs):
    for txt_input in txt_inputs:
        txt_input.user_text_input(event)


def spawn_bodies():
    if not FLAG:
        Vx = (CLICK_POS_UP[0] - CLICK_POS_DOWN[0]) / 25
        Vy = (CLICK_POS_UP[1] - CLICK_POS_DOWN[1]) / 25
        if Vx == 0 and Vy == 0:
            planets.append(StaticBody(int(mass_input.text), CLICK_POS_DOWN[0], CLICK_POS_DOWN[1], star))
        else:
            planets.append(MovementBody(int(mass_input.text), CLICK_POS_DOWN[0], CLICK_POS_DOWN[1], Vx, Vy, earth))


def cursor_line():
    mouse, _, _ = pg.mouse.get_pressed()
    if mouse and not FLAG:
        pg.draw.line(screen, (255, 0, 0), CLICK_POS_DOWN, pg.mouse.get_pos(), 2)


def reset():
    global RESET
    RESET = True


mass_input = TextInput(screen, 0, 0, 200, 100)
res = Button(screen, WIDTH - 200, 0, 200, 100, reset, "RESET", 50, bg_image, (0, 255, 0))


def main_loop():
    global RESET, planets
    RESET = False
    planets = list()
    while not RESET:
        bg.draw()
        event_overview(pg.event.get(), buttons, text_inputs)
        cursor_line()
        draw_buttons(buttons)
        draw_text_inputs(text_inputs)
        calculation_moves(planets)
        draw_bodies(planets)
        pg.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    buttons.append(res)
    text_inputs.append(mass_input)
    while not DONE:
        main_loop()

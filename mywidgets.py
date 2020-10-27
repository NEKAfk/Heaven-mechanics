import pygame as pg
import time as t


class Label:
    def __init__(self, surface, x, y, text, size, color):
        font_name = pg.font.match_font("colibri")
        font = pg.font.Font(font_name, size)
        self.text_surface = font.render(text, True, color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.midtop = (x, y)
        self.surface = surface

    def draw(self):
        self.surface.blit(self.text_surface, self.text_rect)


class Button(pg.sprite.Sprite):
    def __init__(self, surface, x, y, width, height, command, text="", size=25, btn_color=(100, 100, 100),
                 txt_color=(0, 255, 0)):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.command = command
        self.label = Label(surface, x + width // 2, y + height // 2, text, size, txt_color)
        self.delta_click = t.time()
        self.surface = surface
        self.btn_color = btn_color

    def click(self, mouse):
        if t.time() - self.delta_click < 0.1:
            return False
        self.delta_click = t.time()
        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            self.command()
            return True
        return False

    def draw(self):
        if type(self.btn_color) == pg.Surface:
            self.surface.blit(self.btn_color, (self.x, self.y), (0, 0, self.width, self.height))
        else:
            pg.draw.rect(self.surface, self.btn_color, (self.x, self.y, self.width, self.height))
        self.label.draw()


class Background(pg.sprite.Sprite):
    def __init__(self, surface, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.left = self.rect.top = 0
        self.rect.right, self.rect.bottom = surface.get_width(), surface.get_height()
        self.surface = surface

    def draw(self):
        self.surface.blit(self.image, self.rect)


class TextInput:
    def __init__(self, surface, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.text = ""
        self.text_box = Label(surface, x + width // 2, y + height // 4, self.text, height, (0, 0, 0))
        self.surface = surface
        self.active = False
        self.color = (100, 100, 100)

    def click(self, mouse):
        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            self.active = True
            self.color = (150, 150, 150)
            return True
        self.active = False
        self.color = (100, 100, 100)
        return False

    def user_text_input(self, event):
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pg.K_RETURN:
                    return self.text
                else:
                    self.text += event.unicode
                self.text_box = Label(self.surface, self.x + self.width // 2, self.y + self.height // 4,
                                      self.text, self.height, (0, 0, 0))

    def draw(self):
        pg.draw.rect(self.surface, self.color, self.rect, 0)
        self.text_box.draw()

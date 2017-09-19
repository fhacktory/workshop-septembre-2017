import os
import math
import sys, pygame
from operator import add


pygame.init()


class Cube(object):
    def __init__(self, x=0, y=0, image=None):
        super(Cube, self).__init__()

        if image is not None:
            self.set_image(image)
        else:
            self.sprite = None
            self.width = 0
            self.height = 0
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

    def set_position(self, value):
        self.position = value

    def touchedSide(self, element):
        if self.x <= element.x+element.width <= self.x+10 and \
                (element.y <= self.y <= element.y+element.height or element.y <= self.y+self.height <= element.y+element.height):
            return 'right'
    
        if self.y <= element.y+element.width <= self.y+10 and \
                (element.x <= self.x+self.width <= element.width or element.x <= self.x <= element.x + element.width):
            return 'bottom'
    
        if self.x+self.width-10 <= element.x <= self.x+self.width and \
                (element.y <= self.y <= element.y+element.height or element.y <= self.y+self.height <= element.y+element.height):
            return 'left'
    
        if self.y+self.height-10 <= element.y <= self.y+self.height and \
                (element.x <= self.x+self.width <= element.width or element.x <= self.x <= element.x + element.width):
            return 'top'
        return 'none'

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def get_rect(self):
        return self.sprite.get_rect()

    def set_image(self, image):
        self.sprite = pygame.image.load(image).convert_alpha()
        self.width = self.sprite.get_rect().size[0]
        self.height = self.sprite.get_rect().size[1]


class Ball(Cube):
    def __init__(self, x=0, y=0):
        super(Ball, self).__init__(x, y, os.path.join('assets', 'ball_black.png'))


class Cursor(Cube):
    def __init__(self, x=0, y=0):
        super(Cursor, self).__init__(x, y, os.path.join('assets', 'bumper.png'))


class Brick(Cube):
    def __init__(self, resistance, x=0, y=0):
        print(resistance)
        super(Brick, self).__init__(self, x, y)
        self.resistance = resistance
        self.kicks = 0
        self.get_brick_image()

    def is_alive(self):
        return self.kicks < self.resistance

    def increment_kicks(self):
        self.kicks += 1
        if self.kicks > self.resistance:
            self.kicks = self.resistance
        self.get_brick_image()

    def get_brick_image(self):
        image = 'square_blue_state{state}.png'
        if self.resistance == 2:
            image = 'square_yellow_state{state}.png'
        if self.resistance >= 3:
            image = 'square_red_state{state}.png'

        new_state = self.get_brick_state()
        self.set_image(os.path.join('assets', image.format(state=new_state)))

    def get_brick_state(self):
        return math.floor(1 + 2*self.kicks/self.resistance)


class Cursor(Cube):
    def __init__(self, x=0, y=0):
        super(Cursor, self).__init__(x, y, os.path.join('assets', 'bumper.png'))


class Life(Cube):
    def __init__(self, x=0, y=0):
        super(Life, self).__init__(x, y, os.path.join('assets', 'life.png'))




class GameEngine():
    elements = []

    def __init__(self, width, height):
        screen_size = width, height
        self.screen = pygame.display.set_mode(screen_size)

        background_image = os.path.join('assets', 'background.png')
        self.background = pygame.image.load(background_image)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        self.screen.blit(self.background, (0, 0))

    def register_elements(self, elements):
        self.elements = elements

    def render(self, items):
        for item_value in items:
            item_value.move()
            self.screen.blit(item_value.sprite, [item_value.x, item_value.y])

        pygame.display.flip()
        # If delay is needed
        # pygame.time.delay(10)

    def get_key_pressed(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            return 'left'
        elif keys[pygame.K_RIGHT]:
            return 'right'
        else:
            return 'none'

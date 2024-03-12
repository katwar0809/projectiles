import user_inputs
import pygame
import sys
import math
from random import randint


class Particle(object):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.uX = 0
        self.uY = 0
        self.vX = 0
        self.vY = 0
        self.acc = -9.81
        self.t = 0
        self.vel = 0.0
        self.coeff_rest = None
        self.trail = Trail()
        self.launch_arrow = Arrow(1, user_inputs.WHITE)
        self.velx_arrow, self.vely_arrow = Arrow(3, user_inputs.RED), Arrow(3, user_inputs.RED)
        self.projected = False


    def create(self):
        # changed name from draw to create so I wouldn't get confused w the pygame draw function
        pygame.draw.circle(user_inputs.window, user_inputs.BLACK, (self.x, self.y), self.radius)



    def findInitVel(self):
        line_length = pygame.mouse.get_pos()[0] - self.x
        line_height = self.y - pygame.mouse.get_pos()[1]

        self.uX = line_length / 5
        self.uY = line_height / 5

    def bounce(self, bounceType):
        x_sign = -1 if self.vX > 0 else 1
        y_sign = -1 if self.vY > 0 else 1

        if bounceType == 'horizontal':
            self.uY = self.coeff_rest * self.vY
            self.uX = -self.coeff_rest * self.vX
            x,y = self.x + x_sign * self.radius, self.y
            return x,y

        elif bounceType == 'vertical':
            self.uY = -self.coeff_rest * self.vY
            self.uX = self.coeff_rest * self.vX
            x,y = self.x, self.y - y_sign * self.radius
            return x,y



    def findBounces(self):
        bounce_num = math.log(1 / abs(self.uY), self.coeff_rest) if self.coeff_rest > 0 else 1
        return bounce_num

    def path(self, initX, initY, t):

        self.trail.update((self.x, self.y))

        if t == 0:
            self.vX, self.vY = self.uX, self.vY
            self.x, self.y = initX, initY

        else:
            sX = self.uX * t
            sY = (self.uY * t) + (self.acc / 2 * (t ** 2))
            self.vX = self.uX
            self.vY = self.uY + self.acc * t
            self.x, self.y = initX + sX, initY - sY

        self.vel = math.sqrt(self.vX ** 2 + self.vY ** 2)


class Trail(object):
    def __init__(self):
        self.contents = []

    def update(self, coord):
        self.contents.append(coord)
        if len(self.contents) > 1000:
            self.contents.pop(0)

    def plot(self):
        if self.contents:
            for coord in self.contents:
                pygame.draw.circle(user_inputs.window, user_inputs.WHITE, coord, 1)
            self.contents.pop(0)


class Point(object):
    def __init__(self):
        self.x = randint(10, user_inputs.wScreen - 10)
        self.y = randint(10, user_inputs.hScreen - 10)
        self.collected = False

    def create(self):
        pygame.draw.circle(user_inputs.window, user_inputs.YELLOW, (self.x, self.y), 5)

    def collides(self, particle_coords, rad):
        if particle_coords[0]-rad <= self.x <= particle_coords[0]+rad and particle_coords[1]-rad <= self.y <= particle_coords[1]+rad:
            self.collected = True
            return True


class Obstacle(object):
    def __init__(self):
        self.x = randint(0, user_inputs.wScreen - 50)
        self.y = randint(0, user_inputs.hScreen - 50)
        self.width = 50
        self.height = user_inputs.hScreen - self.y
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)
        self.collisiontype = None

    def draw(self):
        pygame.draw.rect(user_inputs.window, user_inputs.BLUE, self.shape)


    def checkCollision(self, coords, rad):
        x,y = coords[0],coords[1]


        if x >= self.shape.left-rad and x <= self.shape.right+rad:
            if y > self.shape.top:
                self.collisiontype = 'horizontal'
                return True


class MovingObstacle(Obstacle):
    def __init__(self):
        super().__init__()
        self.initialx = self.x
        self.speed = randint(1,5)/10
        self.range = randint(100,400)
        self.direction = 1
    def update(self):
        self.x += self.speed*self.direction
        self.shape.x = self.x

        if self.x >= self.initialx+self.range or self.x <= self.initialx-self.range:
            self.direction*=-1


class Arrow(object):
    def __init__(self, thickness, colour):
        self.thickness = thickness
        self.colour = colour
        self.start = None
        self.end = None

    def draw(self):
        pygame.draw.line(user_inputs.window, self.colour, self.start, self.end, self.thickness)

        horizontal = self.end[0] - self.start[0]
        vertical = self.end[1] - self.start[1]
        angle = math.atan2(vertical, horizontal)
        # makes sense

        arrowhead_points = [
            self.end,
            (self.end[0] + 15 * math.cos(angle + math.pi * 5 / 6),
             self.end[1] + 15 * math.sin(angle + math.pi * 5 / 6)),

            (self.end[0] + 15 * math.cos(angle - math.pi * 5 / 6),
             self.end[1] + 15 * math.sin(angle - math.pi * 5 / 6))
        ]

        pygame.draw.line(user_inputs.window, self.colour, self.end, arrowhead_points[1], self.thickness)
        pygame.draw.line(user_inputs.window, self.colour, self.end, arrowhead_points[2], self.thickness)


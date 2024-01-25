import pygame
import math

e = 0.7
# coefficient of restitution

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (64, 64, 64)

wScreen = 1440
hScreen = 800
window = pygame.display.set_mode((wScreen, hScreen))


class Particle(object):
    def __init__(self, x, y, radius):
        # self.init_vel = None
        self.x = x
        self.y = y
        self.radius = radius
        self.uX = 0
        self.uY = 0
        self.vX = 0
        self.vY = 0
        self.acc = -9.8
        self.t = 0

    def create(self):
        # changed name from draw to create so i wouldn't get confused w the pygame draw function
        pygame.draw.circle(window, BLACK, (self.x, self.y), self.radius)

    def findInitVel(self):
        line_length = pygame.mouse.get_pos()[0] - particle.x
        line_height = particle.y - pygame.mouse.get_pos()[1]

        self.uX = line_length / 5
        self.uY = line_height / 5

    def findBounces(self):
        bounce_num = math.log(2/abs(self.uY),e)

        return bounce_num

    def path(self, initX, initY, t):

        if t == 0:
            self.vX, self.vY = self.uX, self.vY
            self.x, self.y = initX, initY

        else:
            sX = self.uX * t
            sY = (self.uY * t) + (self.acc/2 * (t ** 2))
            self.vX = self.uX
            self.vY = self.uY + self.acc * t
            self.x, self.y = initX + sX, initY - sY

    def bounceOffParabola(self):
        # Check if the particle collides with the parabolic curve
        if self.y >= -0.0005 * (self.x - wScreen / 2) ** 2 + (hScreen-50):
            # Calculate the new velocity after the bounce
            self.uY = -e * self.vY


def drawArrow(particle_pos, mouse_pos, arrowhead_length):
    pygame.draw.line(window, WHITE, particle_pos, mouse_pos, 1)

    horizontal = mouse_pos[0] - particle_pos[0]
    vertical = mouse_pos[1] - particle_pos[1]
    angle = math.atan2(vertical, horizontal)
    # makes sense

    arrowhead_points = [
        mouse_pos,
        (mouse_pos[0] + arrowhead_length * math.cos(angle + math.pi * 5 / 6),
         mouse_pos[1] + arrowhead_length * math.sin(angle + math.pi * 5 / 6)),

        (mouse_pos[0] + arrowhead_length * math.cos(angle - math.pi * 5 / 6),
         mouse_pos[1] + arrowhead_length * math.sin(angle - math.pi * 5 / 6))
    ]

    pygame.draw.line(window, WHITE, mouse_pos, arrowhead_points[1], 1)
    pygame.draw.line(window, WHITE, mouse_pos, arrowhead_points[2], 1)


def drawParabola():
    for x_coord in range(wScreen):
        y_coord = -0.0005 * (x_coord - wScreen / 2) ** 2 + 0 * (x_coord - wScreen / 2) + hScreen - 50
        pygame.draw.circle(window, BLACK, (x_coord, int(y_coord)), 1)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CORE CODE: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


particle = Particle(wScreen / 2, hScreen / 2, 10)
projected = False
clock = pygame.time.Clock()
ground = hScreen - particle.radius

time = 0



def redrawWindow():
    window.fill(GREY)
    drawParabola()
    particle.create()
    drawArrow((particle.x, particle.y), pygame.mouse.get_pos(), 15)
    pygame.display.update()


running = True

while running:
    clock.tick(400)

    if projected:
        if bounces < max_bounces:

            time += 0.05

            particle.bounceOffParabola()

            if particle.x <= particle.radius:
                x, y = particle.x + particle.radius, particle.y
                time = 0
                bounces += 1
                particle.uY = e * particle.vY
                particle.uX = -e * particle.vX

            if particle.x >= wScreen - particle.radius:
                x, y = particle.x - particle.radius, particle.y
                time = 0
                bounces += 1
                particle.uY = e * particle.vY
                particle.uX = -e * particle.vX

            if particle.y <= particle.radius:
                x, y = particle.x, particle.y + particle.radius
                time = 0
                bounces += 1
                particle.uY = -e * particle.vY
                particle.uX = e * particle.vX
            '''
            if particle.y >= hScreen - particle.radius + 1:
                x, y = particle.x, particle.y - particle.radius
                time = 0
                bounces += 1
                particle.uX = e * particle.vX
                particle.uY = -e * particle.vY
            '''

            particle.path(x,y,time)

        else:
            projected = False
            particle.y = particle.y
            particle.x = x

    redrawWindow()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not projected:
                x = particle.x
                y = particle.y
                particle.findInitVel()
                bounces = 0
                max_bounces = particle.findBounces()
                projected = True
            # checks that particle isn't already being projected. if not, then particle is projected.

pygame.quit()

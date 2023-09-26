import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (64, 64, 64)

wScreen = 1440
hScreen = 800
window = pygame.display.set_mode((wScreen, hScreen))


class Particle(object):
    def __init__(self, x, y, radius):
        #self.init_vel = None
        self.x = x
        self.y = y
        self.radius = radius
        self.uX = 0
        self.uY = 0
        self.vX = 0
        self.vY = 0

    def create(self):
        # changed name from draw to create so i wouldn't get confused w the pygame draw function
        pygame.draw.circle(window, BLACK, (self.x, self.y), self.radius)

    def findInitVel(self):
        line_length = pygame.mouse.get_pos()[0] - particle.x
        line_height = particle.y - pygame.mouse.get_pos()[1]

        self.uX = line_length/8
        self.uY = line_height/8

        #hyp = math.sqrt((line_length ** 2) + (line_height ** 2))

        #self.init_vel = hyp / 8


    def path(self, initX, initY, angle, t):
        #uX = init_vel * math.cos(angle)
        #uY = init_vel * math.sin(angle)

        sX = self.uX * t
        sY = (self.uY * t) + (-4.9 * (t ** 2))

        self.vX = self.uX
        self.vY = (sY + (-4.9*(t**2)))/t

        new_position = (initX + sX, initY - sY)

        return new_position

    def checkCollision(self, boundary):
        collision = False
        boundary_vector = boundary.vector

        particle_vector = (particle.x - boundary.pt1[0]), (particle.y - boundary.pt1[1])
        particle_magnitude = math.sqrt((particle_vector[0])**2 + (particle_vector[1])**2)

        # finding l:
        dot_product = (boundary_vector[0] * particle_vector[0]) + (boundary_vector[1] * particle_vector[1])
        angle = math.acos(dot_product / (boundary.magnitude * particle_magnitude))

        distance_to_wall = math.sin(angle) * particle_magnitude

        # checking if collision:
        if distance_to_wall < particle.radius:
            collision = True

        return collision


class Boundary(object):
    def __init__(self, pt1, pt2):
        self.pt1 = pt1
        self.pt2 = pt2
        self.vector = (pt2[0]-pt1[0]), (pt2[1]-pt1[1])
        self.magnitude = math.sqrt((self.vector[0])**2 + (self.vector[1])**2)

    def create(self):
        pygame.draw.line(window,BLACK,self.pt1,self.pt2,1)


def findAngle(mouse_pos):
    start_x = particle.x
    start_y = particle.y
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]

    if start_x - mouse_x == 0:
        angle = math.pi / 2

    else:
        angle = math.atan((start_y - mouse_y) / (start_x - mouse_x))

    if start_x > mouse_x and mouse_y > start_y:
        # bottom left quad
        angle = math.pi + abs(angle)

    elif start_x > mouse_x and start_y > mouse_y:
        # top left quad
        angle = math.pi - angle

    elif mouse_x > start_x and mouse_y > start_y:
        # bottom right quad
        angle = (math.pi*2) - angle

    elif mouse_x > start_x and start_y > mouse_y:
        # top right quad
        angle = abs(angle)

    return angle

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



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CORE CODE: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


particle = Particle(wScreen/2, hScreen/2, 10)
projected = False
clock = pygame.time.Clock()
ground = hScreen - particle.radius

time = 0

walls = [Boundary((0,0),(0,hScreen)), Boundary((0,0),(wScreen,0)), Boundary((wScreen,0),(wScreen,hScreen))]

def redrawWindow():
    window.fill(GREY)
    particle.create()
    drawArrow((particle.x, particle.y), pygame.mouse.get_pos(), 15)
    pygame.display.update()


running = True
collision = False

while running:
    clock.tick(400)

    if projected:

        if particle.y < ground:
            # only runs if particle is still in the air

            time += 0.05

            # testing collisions without actually using collision method j to see if it works normally

            if particle.x <= 0 or particle.x >= wScreen:
                particle.uX = -particle.vX

            if particle.y <= 0 or particle.y >= hScreen:
                particle.uY = -particle.vY

            projection_path = particle.path(x, y, theta, time)


            particle.x = projection_path[0]
            particle.y = projection_path[1]


        else:
            projected = False
            particle.y = ground - 1
            time = 0


    redrawWindow()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not projected:
                x = particle.x
                y = particle.y
                theta = findAngle(pygame.mouse.get_pos())
                particle.findInitVel()
                projected = True
            # checks that particle isn't already being projected. if not, then particle is projected.


pygame.quit()
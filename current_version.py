import pygame
import sys
import math
from random import randint
pygame.init()

e = 0.7
# coefficient of restitution

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (64, 64, 64)
YELLOW = (255, 255, 0)

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
        self.acc = -9.81
        self.t = 0
        self.vel = 0.0
        self.trail = Trail()

    def create(self):
        # changed name from draw to create so I wouldn't get confused w the pygame draw function
        pygame.draw.circle(window, BLACK, (self.x, self.y), self.radius)

    def findInitVel(self):
        line_length = pygame.mouse.get_pos()[0] - self.x
        line_height = self.y - pygame.mouse.get_pos()[1]

        self.uX = line_length / 5
        self.uY = line_height / 5

    def findBounces(self):
        bounce_num = math.log(2 / abs(self.uY), e)
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
                pygame.draw.circle(window, WHITE, coord, 1)
            self.contents.pop(0)


class Obstacle(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def create(self):
        pygame.draw.line(window, WHITE, self.start, self.end)

    def check_collision(self, particle_pos):
        line_m = (self.end[1] - self.start[1])/(self.end[0] - self.start[0])
        c = self.start[1] - line_m*self.start[0]

        if particle_pos[1] > line_m*particle_pos[0] + c + 1:
            return True


class Point(object):
    def __init__(self):
        self.x = randint(10,wScreen-10)
        self.y = randint(10,hScreen-10)
        self.collected = False

    def create(self):
        pygame.draw.circle(window, YELLOW, (self.x, self.y), 5)

    def collides(self, particle_coords, rad):
        if particle_coords[0]-rad <= self.x <= particle_coords[0]+rad and particle_coords[1]-rad <= self.y <= particle_coords[1]+rad:
            self.collected = True
            return True



def findLaunchAngle(start_x, start_y, mouse_pos):

    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]

    if mouse_x == start_x:
        if mouse_y < start_y:
            return 90
        else:
            return 270

    elif mouse_y == start_y:
        if mouse_x < start_x:
            return 180
        else:
            return 0

    else:
        angle = math.atan((start_y - mouse_y) / (start_x - mouse_x))

    if start_x > mouse_x and mouse_y > start_y:
        # bottom left quad
        angle = math.pi + abs(angle)

    elif start_x > mouse_x and start_y > mouse_y:
        # top left quad
        angle = abs(math.pi - angle)

    elif mouse_x > start_x and mouse_y > start_y:
        # bottom right quad
        angle = abs((math.pi * 2) - angle)

    elif mouse_x > start_x and start_y > mouse_y:
        # top right quad
        angle = abs(angle)

    return abs(angle * (180 / math.pi))



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

pygame.init()


class Game():
    def __init__(self):


        self.points = [Point(), Point(), Point(), Point(), Point(), Point(), Point(), Point(), Point(), Point()]


        self.particle = Particle(wScreen / 2, hScreen / 2, 10)
        #obstacle = Obstacle((randint(0,wScreen),hScreen),(wScreen,randint(0,hScreen)))

        self.projected = False
        self.clock = pygame.time.Clock()
        self.launch_angle = 0
        self.time = 0
        self.bounces = 0
        self.score = 0
        self.launches = len(self.points)//2

        self.myfont = pygame.font.SysFont('Ariel', 30)


    def redrawWindow(self):

        window.fill(GREY)

        #if launches < 0:
            #global running
            #running = False

        self.particle.create()

        for point in self.points:
            if not point.collected:
                point.create()
            else:
                self.points.remove(point)
                self.points.append(Point())
                self.score += 1

        #obstacle.create()
        self.particle.trail.plot()
        drawArrow((self.particle.x, self.particle.y), pygame.mouse.get_pos(), 15)

        score_surface = self.myfont.render(f'Score = {self.score}', False, (0, 0, 0))
        velocity_surface = self.myfont.render(f'Current Velocity = {self.particle.vel:.3f}', False, (0, 0, 0))
        angle_surface = self.myfont.render(f'Launch Angle = {self.launch_angle:.2f}', False, (0, 0, 0))
        bounce_surface = self.myfont.render(f'Num of Bounces = {self.bounces}', False, (0, 0, 0))
        launch_surface = self.myfont.render(f'Launches remaining = {self.launches}', False, (0, 0, 0))

        window.blit(velocity_surface, (100, 100))
        window.blit(angle_surface, (100, 120))
        window.blit(bounce_surface, (100, 140))
        window.blit(score_surface, (100,180))
        window.blit(launch_surface, (100,160))

        pygame.display.update()

    def run(self):
        running = True

        while running:
            ground = hScreen - self.particle.radius
            self.clock.tick(400)

            self.launch_angle = [findLaunchAngle(self.particle.x, self.particle.y, pygame.mouse.get_pos()) if self.projected else self.launch_angle][0]

            if self.projected:
                for point in self.points:
                    if point.collides((self.particle.x, self.particle.y), self.particle.radius):
                        self.score += 1

                if self.bounces < self.max_bounces:

                    self.time += 0.05
                    '''
                    if obstacle.check_collision((particle.x+particle.radius, particle.y+particle.radius)):
                        x, y = particle.x, particle.y-2
    
                        if particle.uX > 0:
                            particle.uY = e * particle.vY
                            particle.uX = -e * particle.vX
                            time = 0
                            bounces += 1
    
                        else:
                            particle.uY = -e * particle.vY
                            particle.uX = e * particle.vX
                            time = 0
                            bounces += 1
                            '''

                    if self.particle.x <= self.particle.radius:
                        x, y = self.particle.x + self.particle.radius, self.particle.y
                        self.time = 0
                        self.bounces += 1
                        self.particle.uY = e * self.particle.vY
                        self.particle.uX = -e * self.particle.vX

                    if self.particle.x >= wScreen - self.particle.radius:
                        x, y = self.particle.x - self.particle.radius, self.particle.y
                        self.time = 0
                        self.bounces += 1
                        self.particle.uY = e * self.particle.vY
                        self.particle.uX = -e * self.particle.vX

                    if self.particle.y <= self.particle.radius:
                        x, y = self.particle.x, self.particle.y + self.particle.radius
                        self.time = 0
                        self.bounces += 1
                        self.particle.uY = -e * self.particle.vY
                        self.particle.uX = e * self.particle.vX

                    if self.particle.y >= hScreen - self.particle.radius + 1:
                        x, y = self.particle.x, self.particle.y - self.particle.radius
                        self.time = 0
                        self.bounces += 1
                        self.particle.uX = e * self.particle.vX
                        self.particle.uY = -e * self.particle.vY

                    self.particle.path(x, y, self.time)
                    self.particle.trail.update((self.particle.x, self.particle.y))

                else:
                    self.projected = False
                    self.particle.vel = 0.0
                    self.particle.y = y + self.particle.radius - 1
                    self.particle.x = x
                    # for content in particle_trail.contents:
                    # particle_trail.contents.pop(0)

            self.redrawWindow()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if not self.projected:
                        x = self.particle.x
                        y = self.particle.y
                        self.particle.findInitVel()
                        self.bounces = 0
                        self.max_bounces = self.particle.findBounces()
                        self.launches -= 1
                        self.projected = True
                        # checks that particle isn't already being projected. if not, then particle is projected.

if __name__ == "__main__":
    game = Game()
    game.run()




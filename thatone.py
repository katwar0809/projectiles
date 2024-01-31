import pygame
import math
from random import randint

e = 0.7
# coefficient of restitution

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (64, 64, 64)
YELLOW = (255, 255, 0)

wScreen = 1440
hScreen = 800


class Particle(object):
    def __init__(self, game, x, y, radius):
        # self.init_vel = None
        self.game = game
        self.x = x
        self.y = y
        self.radius = radius
        self.uX = 0
        self.uY = 0
        self.vX = 0
        self.vY = 0
        self.acc = -9.81
        self.vel = 0.0

    def draw_particle(self):
        # changed name from draw to create, so I wouldn't get confused w the pygame draw function
        pygame.draw.circle(self.game.window, BLACK, (self.x, self.y), self.radius)

    def findInitVel(self):
        line_length = pygame.mouse.get_pos()[0] - self.game.particle.x
        line_height = self.game.particle.y - pygame.mouse.get_pos()[1]

        self.uX = line_length / 5
        self.uY = line_height / 5

    def findBounces(self):
        bounce_num = math.log(2 / abs(self.uY), e)
        return bounce_num

    def path(self, initX, initY, t):

        if t == 0:
            self.vX, self.vY = self.uX, self.vY
            self.x, self.y = initX, initY

        else:
            sX = self.uX * t
            sY = (self.uY * t) + (0.5 * self.acc * (t ** 2))
            self.vX = self.uX
            self.vY = self.uY + self.acc * t
            self.x, self.y = initX + sX, initY - sY

        self.vel = math.sqrt(self.vX ** 2 + self.vY ** 2)


class Trail(object):
    def __init__(self, game: 'Game'):
        self.contents = []
        self.game = game

    def update(self, coord):
        self.contents.append(coord)
        if len(self.contents) > 1000:
            self.contents.pop(0)

    def plot(self):
        if self.contents:
            for coord in self.contents:
                pygame.draw.circle(self.game.window, WHITE, coord, 1)
            # self.contents.pop(0)


class Obstacle(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def create(self):
        pygame.draw.line(game.window, WHITE, self.start, self.end)

    def check_collision(self, particle_pos):
        line_m = (self.end[1] - self.start[1]) / (self.end[0] - self.start[0])
        c = self.start[1] - line_m * self.start[0]

        if particle_pos[1] > line_m * particle_pos[0] + c + 1:
            return True


class Point(object):
    def __init__(self):
        self.x = randint(10, wScreen - 10)
        self.y = randint(10, hScreen - 10)
        self.collected = False

    def draw_point(self):
        pygame.draw.circle(game.window, YELLOW, (self.x, self.y), 5)

    def collides(self, particle_coords, rad):
        if particle_coords[0] - rad <= self.x <= particle_coords[0] + rad and particle_coords[1] - rad <= self.y <= \
                particle_coords[1] + rad:
            self.collected = True
            return True


def findLaunchAngle(mouse_pos):
    if not game.projected:

        start_x = game.particle.x
        start_y = game.particle.y
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

    else:
        return game.launch_angle


def drawArrow(particle_pos, mouse_pos, arrowhead_length):
    pygame.draw.line(game.window, WHITE, particle_pos, mouse_pos, 1)

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

    pygame.draw.line(game.window, WHITE, mouse_pos, arrowhead_points[1], 1)
    pygame.draw.line(game.window, WHITE, mouse_pos, arrowhead_points[2], 1)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CORE CODE: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((wScreen, hScreen))
        self.clock = pygame.time.Clock()
        self.myfont = pygame.font.SysFont('Ariel', 30)

        self.particle = Particle(self, wScreen / 2, hScreen / 2, 10)
        self.particle_trail = Trail(self)
        self.points = [Point(), Point(), Point(), Point(), Point(), Point(), Point(), Point(), Point(), Point()]
        # self.obstacle = Obstacle((randint(0,wScreen),hScreen),(wScreen,randint(0,hScreen)))

        self.time = 0
        self.bounces = 0
        self.max_bounces = None

        self.score = 0
        self.launches = len(self.points) // 2
        self.launch_angle = 0

        self.projected = False
        self.running = True

    def checkStatus(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if not self.projected:
                    self.launch_angle = findLaunchAngle(pygame.mouse.get_pos())
                    self.particle.findInitVel()
                    self.bounces = 0
                    self.max_bounces = self.particle.findBounces()
                    self.launches -= 1
                    self.projected = True
                    # checks that particle isn't already being projected. if not, then particle is projected.

    def redrawWindow(self):
        self.window.fill(GREY)

        if self.launches < 0:
            self.running = False

        self.particle.draw_particle()

        for point in self.points:
            if not point.collected:
                point.draw_point()
            else:
                self.points.remove(point)
                self.points.append(Point())
                self.launches += 1
        # obstacle.create()
        self.particle_trail.plot()
        drawArrow((self.particle.x, self.particle.y), pygame.mouse.get_pos(), 15)

        score_surface = self.myfont.render(f'Score = {self.score}', False, (0, 0, 0))
        velocity_surface = self.myfont.render(f'Current Velocity = {self.particle.vel:.3f}', False, (0, 0, 0))
        angle_surface = self.myfont.render(f'Launch Angle = {self.launch_angle:.2f}', False, (0, 0, 0))
        bounce_surface = self.myfont.render(f'Num of Bounces = {self.bounces}', False, (0, 0, 0))
        launch_surface = self.myfont.render(f'Launches remaining = {self.launches}', False, (0, 0, 0))

        self.window.blit(velocity_surface, (100, 100))
        self.window.blit(angle_surface, (100, 120))
        self.window.blit(bounce_surface, (100, 140))
        self.window.blit(score_surface, (100, 180))
        self.window.blit(launch_surface, (100, 160))

        pygame.display.update()

    def update(self):
        # self.clock.tick(400)
        # self.launch_angle = findLaunchAngle(pygame.mouse.get_pos())

        x = self.particle.x
        y = self.particle.y

        if self.projected:
            for point in self.points:
                if point.collides((self.particle.x, self.particle.y), self.particle.radius):
                    self.score += 1

            if self.bounces < self.max_bounces:

                self.time += 0.0025
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
                x, y = self.particle.x, self.particle.y

                self.particle.path(x, y, self.time)
                x, y = self.particle.x, self.particle.y

                if self.particle.x <= self.particle.radius:
                    # x, y = self.particle.x + self.particle.radius, self.particle.y
                    x, y = self.particle.radius, self.particle.y
                    self.time = 0
                    # self.bounces += 1
                    # self.particle.uY = e * self.particle.vY
                    self.particle.uX = -e * self.particle.vX

                elif self.particle.x >= wScreen - self.particle.radius:
                    # x, y = self.particle.x - self.particle.radius, self.particle.y
                    x, y = wScreen - self.particle.radius, self.particle.y
                    self.time = 0
                    # self.bounces += 1
                    # self.particle.uY = e * self.particle.vY
                    self.particle.uX = -e * self.particle.vX

                elif self.particle.y <= self.particle.radius:
                    # x, y = self.particle.x, self.particle.y + self.particle.radius
                    x, y = self.particle.x, self.particle.radius
                    self.time = 0
                    # self.bounces += 1
                    self.particle.uY = -e * self.particle.vY
                    # self.particle.uX = e * self.particle.vX

                elif self.particle.y >= hScreen - self.particle.radius:
                    # x, y = self.particle.x, self.particle.y - self.particle.radius
                    x, y = self.particle.x, hScreen - self.particle.radius
                    self.time = 0
                    self.bounces += 1
                    # self.particle.uX = e * self.particle.vX
                    self.particle.uY = -e * self.particle.vY

                self.particle.x, self.particle.y = x, y

                self.particle_trail.update((self.particle.x, self.particle.y))


            else:
                self.projected = False
                self.particle.vel = 0.0
                self.particle.y = y
                self.particle.x = x
                # for content in particle_trail.contents:
                # particle_trail.contents.pop(0)

    def run(self):
        while self.running:
            self.update()
            self.redrawWindow()
            self.checkStatus()

        pygame.quit()


if __name__ == "__main__":
    game = Game()

    game.run()

import user_inputs
import pygame
import math
from random import randint
pygame.init()


class Particle(object):
    """
    A class to represent a particle.

    ...

    Attributes
    ----------
    x,y : int
        x and y coordinates of the particle
    radius : float
        radius of the particle
    uX,uY : float
        initial x and y components of the particle's velocity
    vX,vY : float
        final x and y components of the particle's velocity
    acc : float
        value for the acceleration of the particle
    t : float
        the time elapsed in the current projection
    vel : float
        the overall velocity of the particle
    coeff_rest : float
        the value for the coefficient of restitution between the particle and walls
    trail : Trail
        an instance of the Trail class that stores the past coordinates of the particle
    launch_arrow : Arrow
        an instance of the Arrow class that creates an arrow from the particle to the cursor
    velx_arrow, vely_arrow : Arrow
        instances of Arrow class that create arrows for the x and y components of the particle's velocity
    projected : Bool
        a boolean value for whether the particle is mid-projection or not


    Methods
    -------
    create():
        draws the particle as a circle on the window
    findInitVel():
        finds the initial x and y components of the velocity of the particle
    findBounces():
        calculates the number of times the particle will bounce before its velocity approximates zero
    findPath(initX, initY, t):
        calculates the path of the particle by finding its new coordinates using SUVAT equations
    bounce(bounce_type):
        finds the velocity and coordinates of the particle after it bounces
    """

    def __init__(self, x, y, radius):
        """
        Initialises all the attributes of the Particle class

        Parameters
        ----------
        x : int
            x coordinate of the particle
        y : int
            y coordinate of the particle
        radius : int
            radius of the particle
        """

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
        """
        Draws the particle as a circle on the window
        """

        pygame.draw.circle(user_inputs.window, user_inputs.BLACK, (self.x, self.y), self.radius)

    def findInitVel(self):
        """
        Finds the initial x and y components of the velocity of the particle
        """

        line_length = pygame.mouse.get_pos()[0] - self.x
        line_height = self.y - pygame.mouse.get_pos()[1]

        self.uX = line_length / 5
        self.uY = line_height / 5

    def findBounces(self):
        """
        Calculates the number of times the particle will bounce before its velocity approximates zero

        Returns
        -------
        bounce_num : int
            the maximum number of times the particle will bounce
        """

        bounce_num = math.log(1 / abs(self.uY), self.coeff_rest) if self.coeff_rest > 0 else 1
        return bounce_num

    def findPath(self, initX, initY, t):
        """
        Calculates the path of the particle by finding its new coordinates using SUVAT equations

        Parameters
        ----------
        initX : int
            the initial x coordinate of the particle
        initY : int
            the initial y coordinate of the particle
        t : float
            the current time elapsed in the projection
        """

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

    def bounce(self, bounce_type):
        """
        Finds the velocity and coordinates of the particle after it bounces

        Parameters
        ----------
        bounce_type : str
            value that specifies if the bounce is horizontal or vertical so the right velocity components are changed

        Returns
        -------
        x,y : int
            new x and y coordinates of the particle
        """

        x_sign = -1 if self.vX > 0 else 1
        y_sign = -1 if self.vY > 0 else 1

        if bounce_type == 'horizontal':
            self.uY = self.coeff_rest * self.vY
            self.uX = -self.coeff_rest * self.vX
            x, y = self.x + x_sign * self.radius, self.y
            return x, y

        elif bounce_type == 'vertical':
            self.uY = -self.coeff_rest * self.vY
            self.uX = self.coeff_rest * self.vX
            x, y = self.x, self.y - y_sign * self.radius
            return x, y


class Trail(object):
    """
    A class to represent a trail for a particle.

    ...

    Attributes
    ----------
    contents : list
        a list of (past) coordinates

    Methods
    -------
    update(coord):
        adds the given coordinate to the contents of the trail and makes sure trail isn't too long
    plot():
        draws the coordinates in the trail onto the window as dots
    """

    def __init__(self):
        """
        Initialises all the attributes of the Trail class
        """

        self.contents = []

    def update(self, coord):
        """
        Adds the given coordinate to the contents of the trail and makes sure trail isn't too long

        Parameters
        ----------
        coord : tuple
            the coordinate to be added to the trail
        """

        if len(self.contents) > 1000:
            self.contents.pop(0)
            self.update(coord)
        else:
            self.contents.append(coord)

    def plot(self):
        """
        Draws the coordinates in the trail onto the window as dots
        """

        if self.contents:
            for coord in self.contents:
                pygame.draw.circle(user_inputs.window, user_inputs.WHITE, coord, 1)
            self.contents.pop(0)


class Point(object):
    """
        A class to represent a point in the game aspect of the simulation

        ...

        Attributes
        ----------
        x,y : int
            the x and y coordinates of the point
        collected : Bool
            a boolean value representing whether the point has been collected or not

        Methods
        -------
        create():
            draws the point on the window as a small yellow circle
        collides(coords, rad):
            returns whether the particle hits the point
        """

    def __init__(self):
        """
        Initialises all the attributes of the Point class
        """
        self.x = randint(10, user_inputs.wScreen - 10)
        self.y = randint(10, user_inputs.hScreen - 10)
        self.collected = False

    def create(self):
        """
        Draws the point on the window as a small yellow circle
        """
        pygame.draw.circle(user_inputs.window, user_inputs.YELLOW, (self.x, self.y), 5)

    def collides(self, coords, rad):
        """
        Returns whether the particle hits the point

        Parameters
        ----------
        coords : tuple
            the coordinates of the particle
        rad : float
            the radius of the particle

        Returns
        -------
        True if the point is hit
        """

        if coords[0]-rad <= self.x <= coords[0]+rad and coords[1]-rad <= self.y <= coords[1]+rad:
            self.collected = True
            return True


class Obstacle(object):
    """
        A class to represent an obstacle

        ...

        Attributes
        ----------
        x,y : int
            the x and y coordinates of the top left corner of the obstacle
        width : int
            the width of the obstacle
        height : int
            the height of the obstacle
        shape : Rect
            the Rect representation of the obstacle's shape

        Methods
        -------
        draw():
            draws the obstacle on the window
        checkCollision():
            checks whether the particle hits the obstacle
        """

    def __init__(self, r):
        """
        Initialises all the attributes of the Obstacle class

        Parameters
        ----------
        r : radius of the particle
        """

        self.x = randint(0, user_inputs.wScreen/2 - r - 50) or randint(user_inputs.wScreen/2 + r, user_inputs.wScreen - 50)
        self.y = randint(0, user_inputs.hScreen - 50)
        self.width = 50
        self.height = user_inputs.hScreen - self.y
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        """
        Draws the obstacle on the window
        """
        pygame.draw.rect(user_inputs.window, user_inputs.BLUE, self.shape)

    def checkCollision(self, coords, rad):
        """
        Checks whether the particle hits the obstacle

        Parameters
        ----------
        coords : the current coordinates of the particle
        rad : the radius of the particle

        Returns
        -------
        True if the particle hits the obstacle
        """

        x, y = coords[0], coords[1]

        if self.shape.left-rad <= x <= self.shape.right+rad:
            if y > self.shape.top:
                return True


class MovingObstacle(Obstacle):
    """
    Inherits from the Obstacle class to create an obstacle that moves

    ...

    Attributes
    ----------
    initial_x : int
        the obstacle's starting x coordinate
    speed : float
        the speed the obstacle moves at
    range : int
        the range of the obstacle's movement
    direction : int
        +1 or -1 depending on the direction of the obstacle's movement


    Methods
    -------
    update():
        moves the obstacle to its new position
    """

    def __init__(self, r):
        """
        Initialises all the attributes of the Moving Obstacle class

        Parameters
        ----------
        r : the radius of the particle
        """

        super().__init__(r)
        self.initial_x = self.x
        self.speed = randint(1,5)/10
        self.range = randint(100,400)
        self.direction = 1

    def update(self):
        """
        Moves the obstacle to its new position
        """

        self.x += self.speed*self.direction
        self.shape.x = self.x

        if self.x >= self.initial_x+self.range or self.x <= self.initial_x-self.range:
            self.direction *= -1


class Arrow(object):
    """
    A class to represent an Arrow.

    ...

    Attributes
    ----------
    thickness : int
        a value for the thickness of the arrow
    colour : tuple
        an RGB value for the colour of the arrow
    start, end : tuple
        the coordinates of the arrow's points/ends


    Methods
    -------
    draw():
        draws the arrow on the window
    """

    def __init__(self, thickness, colour):
        """
        Initialises all the attributes of the Arrow class

        Parameters
        ----------
        thickness : int
            a value for the thickness of the arrow
        colour : tuple
            an RGB value for the colour of the arrow
        """

        self.thickness = thickness
        self.colour = colour
        self.start = None
        self.end = None

    def draw(self):
        """
        Draws the arrow on the window
        """

        pygame.draw.line(user_inputs.window, self.colour, self.start, self.end, self.thickness)

        horizontal = self.end[0] - self.start[0]
        vertical = self.end[1] - self.start[1]
        angle = math.atan2(vertical, horizontal)

        arrowhead_points = [
            self.end,
            (self.end[0] + 15 * math.cos(angle + math.pi * 5 / 6),
             self.end[1] + 15 * math.sin(angle + math.pi * 5 / 6)),

            (self.end[0] + 15 * math.cos(angle - math.pi * 5 / 6),
             self.end[1] + 15 * math.sin(angle - math.pi * 5 / 6))
        ]

        pygame.draw.line(user_inputs.window, self.colour, self.end, arrowhead_points[1], self.thickness)
        pygame.draw.line(user_inputs.window, self.colour, self.end, arrowhead_points[2], self.thickness)


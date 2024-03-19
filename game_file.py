import user_inputs
import game_objects

import pygame
import sys
import math
pygame.init()
pygame.display.set_caption('Projectile Simulation')


class Game(object):
    """
    A class to represent the whole Game

    ...

    Attributes
    ----------
    running : Bool
        a boolean value for whether the simulation is running or not
    particle : Particle
        the particle that will be projected
    launch_angle : float
        the initial launch angle of the particle
    time : float
        the current time elapsed in the projection
    max_bounces : int
        the number of times the particle will bounce before its velocity approximates zero
    bounces : int
        the current number of times the particle has bounced vertically
    displayed_bounces : int
        the particle's total number of bounces
    launches : int
        the number of times the particle has been launched
    score : int
        the current score based on how many points have been collected
    points : list
        a list of Point instances to represent the total collectable points on the window
    obstacles : list
        a list of Obstacle instances to represent the obstacles on the window
    trail_shown : Bool
        a boolean value for whether the particle trail is shown in the simulation
    velocity_shown : Bool
        a boolean value for whether the particle's velocity arrows are shown in the simulation
    obstacles_shown : Bool
        a boolean value for whether there are obstacles in the simulation
    reset_button : MainButton
        an instance of the MainButton class to represent a button that resets the simulation


    Methods
    -------
    initialise():
        sets up the initial menu window where the user can input initial projection values
    redrawWindow():
        creates and displays the current projection frame on the window
    findLaunchAngle(start_x, start_y, mouse_pos):
        static method that finds the particle's initial launch angle
    run():
        runs the projection
    """

    def __init__(self):
        """
        Initialises all the attributes of the Game class
        """

        self.running = None
        self.particle = game_objects.Particle(user_inputs.wScreen / 2, user_inputs.hScreen / 2, 10)

        self.launch_angle = 0
        self.time = 0
        self.max_bounces = None
        self.bounces = 0
        self.displayed_bounces = 0
        self.launches = None
        self.score = 0
        self.points = []
        self.obstacles = []

        self.trail_shown = False
        self.velocity_shown = False
        self.obstacles_shown = False

        self.reset_button = user_inputs.MainButton(1300, 30, user_inputs.BLACK, 'RESET')

    def initialise(self):
        """
        Sets up the initial menu window where the user can input initial projection values
        """

        self.launches = 10
        self.particle.x, self.particle.y = user_inputs.wScreen / 2 , user_inputs.hScreen / 2
        self.points = [game_objects.Point() for i in range(10)]
        self.obstacles = [game_objects.Obstacle(self.particle.radius), game_objects.Obstacle(self.particle.radius), game_objects.MovingObstacle(self.particle.radius)]

        run_button = user_inputs.MainButton(600, 200, user_inputs.BLACK, 'Play!')
        trail_button = user_inputs.Button(200, 100, None, 'Show Ball Trail')
        velocity_button = user_inputs.Button(200, 200, None, 'Show Velocities')
        obstacle_button = user_inputs.Button(200, 300, None, 'Show Obstacles ')

        input_buttons = [run_button, trail_button,velocity_button,obstacle_button]

        restitution_slider = user_inputs.Slider(0.0, 0.9, 1000, 100, 'Restitution')
        size_slider = user_inputs.Slider(10, 50, 1000, 200, 'Ball Size')
        grav_slider = user_inputs.Slider(0.0, 30, 1000, 300, 'Gravity')

        input_sliders = [restitution_slider, size_slider, grav_slider]

        while not run_button.pressed:
            user_inputs.window.fill(user_inputs.GREY)
            for button in input_buttons:
                button.draw()
            for slider in input_sliders:
                slider.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in input_buttons:
                        button.isPressed(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    for slider in input_sliders:
                        slider.isUsed(event.buttons[0], event.pos)

            pygame.display.update()

        self.trail_shown = trail_button.pressed
        self.velocity_shown = velocity_button.pressed
        self.obstacles_shown = obstacle_button.pressed

        self.particle.radius = size_slider.slider_val
        self.particle.coeff_rest = restitution_slider.slider_val
        self.particle.acc = -grav_slider.slider_val

        self.run()

    def redrawWindow(self):
        """
        Creates and displays the current projection frame on the window
        """

        user_inputs.window.fill(user_inputs.SKYBLUE)

        self.reset_button.draw()

        if self.launches < 0:
            self.initialise()

        self.particle.create()
        self.particle.launch_arrow.start, self.particle.launch_arrow.end = (self.particle.x, self.particle.y), pygame.mouse.get_pos()
        self.particle.launch_arrow.draw()

        for point in self.points:
            if not point.collected:
                point.create()
            else:
                self.points.remove(point)
                self.points.append(game_objects.Point())

        if self.trail_shown:
            self.particle.trail.plot()

        if self.velocity_shown:
            self.particle.velx_arrow.start, self.particle.velx_arrow.end = ((self.particle.x, self.particle.y), (self.particle.x+self.particle.vX, self.particle.y))
            self.particle.vely_arrow.start, self.particle.vely_arrow.end = ((self.particle.x, self.particle.y), (self.particle.x, self.particle.y-self.particle.vY))
            self.particle.velx_arrow.draw()
            self.particle.vely_arrow.draw()

        if self.obstacles_shown:
            for obstacle in self.obstacles:
                obstacle.draw()
                if type(obstacle) == game_objects.MovingObstacle:
                    obstacle.update()

        score_surface = user_inputs.font.render(f'Score = {self.score}', False, user_inputs.WHITE)
        velocity_surface = user_inputs.font.render(f'Current Velocity = {self.particle.vel:.3f}', False, user_inputs.WHITE)
        angle_surface = user_inputs.font.render(f'Launch Angle = {self.launch_angle:.2f}', False, user_inputs.WHITE)
        bounce_surface = user_inputs.font.render(f'Num of Bounces = {self.displayed_bounces}', False, user_inputs.WHITE)
        launch_surface = user_inputs.font.render(f'Launches remaining = {self.launches}', False, user_inputs.WHITE)

        user_inputs.window.blit(velocity_surface, (100, 100))
        user_inputs.window.blit(angle_surface, (100, 120))
        user_inputs.window.blit(bounce_surface, (100, 140))
        user_inputs.window.blit(score_surface, (100, 180))
        user_inputs.window.blit(launch_surface, (100, 160))

        pygame.display.update()

    @staticmethod
    def findLaunchAngle(start_x, start_y, mouse_pos):
        """
        Static method that finds the particle's initial launch angle

        Parameters
        ----------
        start_x : int
            the particle's initial x coordinate
        start_y : int
            the particle's initial y coordinate
        mouse_pos : tuple
            the current coordinates of the cursor

        Returns
        -------
        An integer value representing the launch angle
        """

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

    def run(self):
        """
        Runs the projection
        """

        running = True
        x, y = self.particle.x,self.particle.y

        while running:

            self.launch_angle = self.findLaunchAngle(x, y, pygame.mouse.get_pos()) if not self.particle.projected else self.launch_angle

            if self.particle.projected:

                for point in self.points:
                    if point.collides((self.particle.x, self.particle.y), self.particle.radius):
                        self.score += 1

                if self.bounces < self.max_bounces:
                    self.particle.trail.update((self.particle.x, self.particle.y))
                    self.time += 0.05

                    if self.obstacles_shown:
                        for obstacle in self.obstacles:
                            if obstacle.checkCollision((self.particle.x, self.particle.y), self.particle.radius):
                                x, y = self.particle.bounce('horizontal')

                                self.time = 0
                                self.displayed_bounces += 1

                    if self.particle.x <= self.particle.radius or self.particle.x >= user_inputs.wScreen - self.particle.radius:

                        x, y = self.particle.bounce('horizontal')

                        self.time = 0
                        self.displayed_bounces += 1

                    if self.particle.y <= self.particle.radius or self.particle.y >= user_inputs.hScreen - self.particle.radius:
                        x, y = self.particle.bounce('vertical')
                        self.time = 0
                        self.displayed_bounces += 1
                        self.bounces += 1

                    self.particle.findPath(x, y, self.time)

                else:
                    self.particle.projected = False
                    self.particle.vel = 0.0
                    self.particle.y = y + self.particle.radius - 1
                    self.particle.x = x

            self.redrawWindow()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.reset_button.isPressed(event.pos):
                        self.running = False

                        self.initialise()

                    else:

                        if not self.particle.projected:
                            self.particle.findInitVel()
                            self.bounces = 0
                            self.displayed_bounces = 0
                            self.max_bounces = self.particle.findBounces()
                            self.launches -= 1
                            self.particle.projected = True


def startGame():
    """
    Creates and initialises an instance of the Game class
    """

    if __name__ == "__main__":
        game = Game()
        game.initialise()


startGame()


'''
problems:
- if reset button is pressed mid-launch, it crashes
- launch angle needs to be big for big balls
- if ball big it spawns on obstacles so it crashes
- bouncing on top of obstacles doesn't work
- doesn't close when on main menu

thoughts:
- in eval: should make game optional cos distracting
'''
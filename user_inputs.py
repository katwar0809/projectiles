import pygame
pygame.init()

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREY = 64, 64, 64
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
SKYBLUE = 120, 190, 255
YELLOW = 255, 255, 0

wScreen = 1440
hScreen = 800
window = pygame.display.set_mode((wScreen, hScreen))
font = pygame.font.SysFont('Ariel', 30)


class Button(object):
    """
    A class to represent a button.

    ...

    Attributes
    ----------
    x,y : int
        coordinates of the top left corner of the button
    pressed : Bool
        a boolean value for whether the button is toggled
    start_colour : tuple
        RGB value for the initial colour of the button, ie, when it hasn't been pressed
    colour : tuple
        RGB value for the current colour of the button
    text : str
        the text that will be displayed on the button
    length : int
        the length of the text, which will determine the length of the button itself
    shape : Rect
        the Rect representation of the button's shape


    Methods
    -------
    isPressed(pos):
        Determines whether the button has been pressed
    draw():
        Draws the button on the window
    """

    def __init__(self, x, y, colour, text):
        """
        Initialises all the attributes of the Button class

        Parameters
        ----------
        x : int
            x coordinate of top left corner of button
        y : int
            y coordinate of top left corner of button
        colour : tuple
            initial button colour
        text : str
            text displayed on the button
        """

        self.x = x
        self.y = y
        self.pressed = False
        self.start_colour = colour if colour else RED
        self.colour = self.start_colour
        self.text = font.render(f"{text.upper()}", True, (255, 255, 255))
        self.length = len(text)
        self.shape = pygame.Rect(x, y, self.length*15, 50)


    def isPressed(self, pos):
        """
        Determines whether the button has been pressed

        Parameters
        ----------
        pos : tuple
            current coordinates of the cursor
        """

        if self.shape.collidepoint(pos):
            self.pressed = not self.pressed
            if self.pressed:
                self.colour = GREEN
            else:
                self.colour = self.start_colour

    def draw(self):
        """
        Draws the button on the window
        """

        pygame.draw.rect(window, self.colour, self.shape)
        window.blit(self.text, (self.x + self.length, self.y + 15))


class MainButton(Button):
    """
    Inherits from the Button class to create a button that returns a value when pressed

    """

    def isPressed(self, pos):
        """
        Determines whether button has been pressed and returns a Boolean value accordingly

        Parameters
        ----------
        pos : tuple
            current coordinates of the cursor

        Returns
        -------
        True if button is pressed
        """

        if self.shape.collidepoint(pos):
            self.pressed = True
            return True


class Slider(object):
    """
    A class to represent a slider.

    ...

    Attributes
    ----------
    x,y : int
        coordinates of the top left corner of the slider
    min, max : int
        the minimum and maximum values the slider can display
    name : str
        the name of the simulation feature controlled by the slider
    increment : int
        the amount by which the slider value changes when it is moved by one pixel
    slider_val : int
        the current value displayed by the slider
    slider_shape : Rect
        the Rect representation of the slider's shape
    track_shape : Rect
        the Rect representation of the slider track's shape


    Methods
    -------
    isUsed(pos):
        Determines whether the slider has been dragged/used
    draw():
        Draws the slider and track on the window, as well as its current value
    """

    def __init__(self, minimum, maximum, x, y, name):
        """
        Initialises all the attributes of the Slider class

        Parameters
        ----------
        minimum : int
            the minimum value of the slider
        maximum : int
            the maximum value of the slider
        x : int
            x coordinate of the top left corner of the slider
        y : int
            y coordinate of the top left corner of the slider
        name : str
            simulation feature represented by the slider
        """

        self.x = x
        self.y = y
        self.min = minimum
        self.max = maximum
        self.name = name + ':'
        self.increment = (self.max-self.min)/300
        self.slider_val = self.min
        self.slider_shape = pygame.Rect(x, y, 20, 50)
        self.track_shape = pygame.Rect(x, y + 25, 300, 5)

    def isUsed(self, clicked, pos):
        """
        Determines whether the slider has been dragged/used

        Parameters
        ----------
        clicked : int
            integer value showing which mouse button has been pressed (1 = primary button, ie, normal left click)
        pos : tuple
            current coordinates of the cursor
        """

        if clicked == 1 and self.slider_shape.collidepoint(pos):
            if pos[0] - 10 < self.x:
                self.slider_shape.x = self.x
            elif pos[0] - 10 > self.x + 300:
                self.slider_shape.x = self.x + 300
            else:
                self.slider_shape.x = pos[0] - 10

            self.slider_val = round((self.min + (self.slider_shape.x - self.x) * self.increment), 1)

    def draw(self):
        """
        Draws the slider and track on the window, as well as its current value
        """

        pygame.draw.rect(window, WHITE, self.track_shape)
        pygame.draw.rect(window, RED, self.slider_shape)
        window.blit((font.render(f"{self.name}", True, BLACK)), (self.x-125, self.y+15))
        window.blit((font.render(f"{self.slider_val}", True, BLACK)), (self.slider_shape.x, self.y - 30))

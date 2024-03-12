import pygame
import sys

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




class Button():
    def __init__(self, x, y, colour, text):
        self.x = x
        self.y = y
        self.pressed = False
        self.start_colour = colour if colour else RED
        self.colour = self.start_colour
        self.text = text
        self.length = len(text)
        self.shape = pygame.Rect(x, y, self.length*15, 50)
        self.text = font.render(f"{text.upper()}", True, (255, 255, 255))


    def is_pressed(self, pos):

        if self.shape.collidepoint(pos):
            self.pressed = not self.pressed
            if self.pressed:
                self.colour = GREEN
            else:
                self.colour = self.start_colour

    def draw(self):
        pygame.draw.rect(window, self.colour, self.shape)
        window.blit(self.text, (self.x +self.length, self.y + 15))

class MainButton(Button):

    def is_pressed(self, pos):

        if self.shape.collidepoint(pos):
            self.pressed = True
            return True


class Slider():
    def __init__(self, minimum, maximum, x, y, name):
        self.x = x
        self.y = y
        self.min = minimum
        self.max = maximum
        self.name = name + ':'
        self.increment = (self.max-self.min)/300
        self.sliderval = self.min
        self.slidershape = pygame.Rect(x,y,20,50)
        self.trackshape = pygame.Rect(x,y+25,300,5)

    def isUsed(self, clicked, pos):
        if clicked == 1 and self.slidershape.collidepoint(pos):
            if pos[0] - 10 < self.x:
                self.slidershape.x = self.x
            elif pos[0] - 10 > self.x +300:
                self.slidershape.x = self.x+300
            else:
                self.slidershape.x = pos[0] - 10

            self.sliderval = round((self.min + (self.slidershape.x-self.x)*self.increment),1)

    def draw(self):
        pygame.draw.rect(window, WHITE, self.trackshape)
        pygame.draw.rect(window, RED, self.slidershape)
        window.blit((font.render(f"{self.name}", True, BLACK)), (self.x-125, self.y+15))
        window.blit((font.render(f"{self.sliderval}", True, BLACK)), (self.slidershape.x, self.y-30))
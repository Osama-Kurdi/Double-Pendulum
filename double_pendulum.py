import pygame
import numpy
from math import cos, sin, pi, radians

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("sound.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)
font_ = pygame.font.SysFont('Comic Sans MS', 15)
display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


class Pendulum:
    def __init__(self, a1, a2, color):
        self.run = True
        self.g = 1
        self.m1 = 40
        self.m2 = 20
        self.a1 = a1
        self.a2 = a2
        self.a1_v = 0
        self.a2_v = 0
        self.a1_a = 0
        self.a2_a = 0
        self.r1 = 200
        self.r2 = 200
        self.o0 = (700, 200)
        self.path = []
        self.color = color
        self.line_color = self.color
        self.clock = pygame.time.Clock()
        self.t = 0

    def move(self):
        num1 = -self.g * (2 * self.m1 + self.m2) * sin(self.a1)
        num2 = -self.m2 * self.g * sin(self.a1-2*self.a2)
        num3 = -2*sin(self.a1-self.a2)*self.m2
        num4 = self.a2_v*self.a2_v*self.r2+self.a1_v*self.a1_v*self.r1*cos(self.a1-self.a2)
        den = self.r1 * (2 * self.m1 + self.m2 - self.m2 * cos(2*self.a1-2*self.a2))
        self.a1_a = (num1 + num2 + num3 * num4) / den

        num1 = 2 * sin(self.a1 - self.a2)
        num2 = (self.a1_v * self.a1_v * self.r1 * (self.m1 + self.m2))
        num3 = self.g * (self.m1 + self.m2) * cos(self.a1)
        num4 = self.a2_v * self.a2_v * self.r2 * self.m2 * cos(self.a1 - self.a2)
        den = self.r2 * (2 * self.m1 + self.m2 - self.m2 * cos(2*self.a1-2*self.a2))
        self.a2_a = (num1*(num2 + num3 + num4)) / den

        self.a1_v += self.a1_a
        self.a2_v += self.a2_a
        self.a1 += self.a1_v
        self.a2 += self.a2_v

        #self.a1_v *= 0.01
        #self.a2_v *= 0.01
        
        x1 = self.r1 * sin(self.a1)
        y1 = self.r1 * cos(self.a1)

        x2 = x1 + self.r2 * sin(self.a2)
        y2 = y1 + self.r2 * cos(self.a2)
        try:
            self.pos1 = (int(self.o0[0] + x1), int(self.o0[1] + y1))
        except:
            print(self.o0[0], x1, self.o0[1], y1)
            print(self.a1, self.a2, self.r1)
        self.pos2 = (int(self.o0[0] + x2), int(self.o0[1] + y2))

        self.path.append(self.pos2)
        if len(self.path) > 150:
           self.path.remove(self.path[0])
        self.t += self.clock.get_time() / 1000
        self.clock.tick(70)

    def draw(self):
        global display
        if self.t <= 20:
            pygame.draw.line(display, (255, 255, 255), self.o0, self.pos1)
            pygame.draw.line(display, (255, 255, 255), self.pos1, self.pos2)
            pygame.draw.circle(display, self.color, self.pos1, 10)
        pygame.draw.circle(display, self.color, self.pos2, 10)
        pygame.draw.circle(display, (255, 255, 255), self.o0, 3)
        pygame.draw.line(display, (255, 255, 255), (self.o0[0] - 30, self.o0[1]), (self.o0[0] + 30, self.o0[1]))

        if len(self.path) > 0:
            for x, y in self.path:
                #(0, 252, 59)
                #pygame.draw.circle(display, self.line_color, (int(x), int(y)), 2)
                display.set_at((int(x), int(y)), self.line_color)

        text = font.render('Mass 1 = {}'.format(int(self.m1/10)), False, (255, 255, 255))
        display.blit(text,(100,150))
        text = font.render('Mass 2 = {}'.format(int(self.m2/10)), False, (255, 255, 255))
        display.blit(text,(100,200))
        text = font_.render('Click escape to exit', False, (255, 255, 255))
        display.blit(text,(100,370))
        text = font_.render('Made by MHD Usama Kurdi', False, (255, 255, 255))
        display.blit(text,(100,400))


class App:
    def __init__(self):
        self.running = False
        self.pendulums = []
        self.pendulums.append(Pendulum(radians(90),radians(90), (0, 46, 252)))
        self.pendulums.append(Pendulum(radians(90.000001),radians(90.000001), (206, 66, 245)))
        self.pendulums.append(Pendulum(radians(90.000002),radians(90.000002), (218, 252, 0)))
        self.pendulums.append(Pendulum(radians(90.000003),radians(90.000003), (0, 252, 59)))
        

    def run(self):
        self.running = True
        while self.running:
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                    self.running = False
                    break
            for pendulum in self.pendulums:
                pendulum.move()
            self.draw()

    def draw(self):
        display.fill((0, 0, 0))
        for pendulum in self.pendulums:
            pendulum.draw()
        pygame.display.flip()


app = App()
app.run()

pygame.quit()

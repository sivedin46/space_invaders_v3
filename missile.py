from constants import *
import time
from turtle import Turtle
import pygame


pygame.mixer.init()
fire_sound = pygame.mixer.Sound(FIRE_SOUND)


class Missile(Turtle):
    def __init__(self):
        super().__init__()
        self.missiles = []
        self.last_time = 0
        self.missile_speed = MISSILE_MOVE_STEP
        self.missile_create_time = MISSILE_CREATE_TIME
        self.screen = self.getscreen()

    def control_missile(self, fighter):
        new_time = time.time()
        elapsed_time = new_time - self.last_time
        if elapsed_time > self.missile_create_time:
            self.create_missile(fighter)

    def create_missile(self, fighter):
        new_missile = Turtle()
        new_missile.setheading(90)
        new_missile.hideturtle()
        new_missile.shape("square")
        new_missile.color("white")
        new_missile.shapesize(0.05, 0.3, 1)
        new_missile.penup()
        new_missile.goto(fighter.xcor(), fighter.ycor())
        new_missile.showturtle()
        fire_sound.play()
        self.missiles.append(new_missile)
        self.last_time = time.time()

    def move_missiles(self):
        for missile in self.missiles:
            missile.forward(self.missile_speed)

    def speed_up_missiles(self, dt):
        self.missile_speed += MISSILE_MOVE_STEP * dt
        self.missile_create_time *= 0.7

    def missile_delete(self, index):
        removed_missile = self.missiles.pop(index)
        removed_missile.hideturtle()
        removed_missile.clear()
        del removed_missile

    def delete_all_missiles(self):
        for missile in self.missiles:
            missile.hideturtle()
            missile.clear()
            del missile
        self.missiles.clear()

    def check_missiles_status(self):
        for number, missile in enumerate(self.missiles):
            if missile.ycor() > 290:
                self.missile_delete(number)

from constants import *
import random
import time
import turtle


class Bonus(turtle.Turtle):
    def __init__(self, shape_bonus):
        super().__init__()
        self.bonus_shape = shape_bonus
        self.bonus_l = []
        self.life_time = BONUS_LIFE_TIME
        self.create = True
        self.screen = turtle.getscreen()
        self.screen.tracer(0)

    def create_new_bonus(self):
        random_chance = random.randint(1, 300)
        if random_chance == 1 and self.create:
            self.create_time = time.time()
            bonus = turtle.Turtle()
            bonus.setheading(270)
            bonus.hideturtle()
            bonus.shape(self.bonus_shape)
            bonus.color("white")
            bonus.shapesize(1, 1, 1)
            bonus.penup()
            random_x = random.randint(-220, 220)
            random_y = random.randint(-200, -150)
            bonus.goto(random_x, random_y)
            bonus.showturtle()
            self.bonus_l.append(bonus)
            self.bonus_delete(self.create_time, bonus, False)
            self.create = False

    def bonus_delete(self, create_time, bonus, del_now):
        now = time.time()
        if (now - create_time >= self.life_time) or del_now:
            if self.bonus_l:
                removed_bonus = self.bonus_l.pop(0)
                removed_bonus.hideturtle()
                removed_bonus.clear()
                del removed_bonus
                self.create = True
        else:
            turtle.Turtle().screen.ontimer(lambda: self.bonus_delete(create_time, bonus, False), 100)

    

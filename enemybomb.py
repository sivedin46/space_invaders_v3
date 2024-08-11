from constants import *
import random
import turtle


class EnemyBomb(turtle.Turtle):
    def __init__(self, bomb_shape):
        super().__init__()
        self.bomb_shape = bomb_shape
        self.end = CREATE_BOMB_INDEX  # increases probability if this decrease
        self.bomb_speed = BOMB_MOVE_STEP
        self.bombs = []
        self.screen = turtle.getscreen()
        self.screen.tracer(0)

    def create_new_bomb(self, enemies):
        random_chance = random.randint(1, self.end)
        if random_chance == 1:
            new_bomb = turtle.Turtle()
            new_bomb.setheading(270)
            new_bomb.hideturtle()
            new_bomb.shape(self.bomb_shape)
            new_bomb.color("white")
            new_bomb.shapesize(0.1, 0.5, 1)
            new_bomb.penup()
            random_pos = random.choice(enemies).pos()
            new_bomb.goto(random_pos)
            new_bomb.showturtle()
            self.bombs.append(new_bomb)

    def move_bombs(self, dt, level):
        for bomb in self.bombs:
            speed = self.bomb_speed * dt * level  # set speed for bomb move
            bomb.forward(self.bomb_speed+speed)

    def speed_up_bombs(self, dt):  # speed up bomb for level update
        self.bomb_speed += BOMB_MOVE_STEP
        if self.end > 1:
            self.end = round(self.end * 0.7)

    def bomb_delete(self, index):
        removed_bomb = self.bombs.pop(index)
        removed_bomb.hideturtle()
        removed_bomb.clear()
        del removed_bomb

    def check_bomb_status(self):  # check for all boms if they are in or out of screen
        for num, bomb in enumerate(self.bombs):
            if bomb.ycor() < -290:
                self.bomb_delete(num)

    def delete_all_bombs(self):
        for bomb in self.bombs:
            bomb.hideturtle()
            bomb.clear()
            del bomb
        self.bombs.clear()

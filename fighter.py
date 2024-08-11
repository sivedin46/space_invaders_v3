from constants import *
import turtle


class Fighter(turtle.Turtle):
    def __init__(self, fighter_shape):
        super().__init__()
        self.fighter = turtle.Turtle()
        self.fighter.hideturtle()
        self.fighter.shape(fighter_shape)
        self.fighter.color("white")
        self.fighter.penup()
        self.fighter.shapesize(stretch_wid=1, stretch_len=1, outline=0)
        self.fighter.goto(0, -270)
        self.fighter.showturtle()
        self.screen = turtle.getscreen()
        self.screen.tracer(0)
    def fighter_go_right(self):
        if self.fighter.xcor() < 220 - (FIGHTER_MOVE_STEP / 2):
            new_x = self.fighter.xcor() + FIGHTER_MOVE_STEP
            self.fighter.goto(new_x, self.fighter.ycor())

    def fighter_go_left(self):
        if self.fighter.xcor() > -220 + (FIGHTER_MOVE_STEP / 2):
            new_x = self.fighter.xcor() - FIGHTER_MOVE_STEP
            self.fighter.goto(new_x, self.fighter.ycor())

    def fighter_go_up(self):
        if self.fighter.ycor() < -150 - (FIGHTER_MOVE_STEP / 2):
            new_y = self.fighter.ycor() + FIGHTER_MOVE_STEP
            self.fighter.goto(self.fighter.xcor(), new_y)

    def fighter_go_down(self):
        if self.fighter.ycor() >= -270 + (FIGHTER_MOVE_STEP / 2):
            new_y = self.fighter.ycor() - FIGHTER_MOVE_STEP
            self.fighter.goto(self.fighter.xcor(), new_y)

    def fighter_reset_pos(self):
        self.fighter.goto(0, -270)

    def delete_fighter(self):
        if self.fighter:
            self.fighter.hideturtle()
            self.fighter.clear()
            del self.fighter

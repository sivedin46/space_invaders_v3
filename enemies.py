from constants import *
import turtle


class Enemies(turtle.Turtle):
    def __init__(self, enemy_shape):
        super().__init__()
        self.enemies = []  # creates alist of enemies object for usage in methods of game
        self.moving_right = True
        self.enemy_shape = enemy_shape
        self.enemy_counter = 0  # counter used for adding new enemy's color and y position  in level 2 and level 3
        self.create_new_enemy(4)
        self.screen = turtle.getscreen()
        self.screen.tracer(0)

    def create_new_enemy(self, row):
        for index in range(row):  # ıf you want more enemies increase COLOR[],Y_POSITIONS  and range
            x_position = -120  # start point for first enemy's center position
            while x_position <= 120:  # limit for last enemy's center position
                new_enemy = turtle.Turtle()
                new_enemy.shape(self.enemy_shape)
                # new_enemy.color(COLORS[(index + self.enemy_counter) % len(COLORS)]) #if use instead of shape
                new_enemy.shapesize(0.3, 0.3, 0)
                new_enemy.penup()
                new_enemy.goto(x_position, ENEMY_Y_POSITIONS[(index + self.enemy_counter) % len(ENEMY_Y_POSITIONS)])
                self.enemies.append(new_enemy)
                x_position = new_enemy.xcor() + 40
        self.enemy_counter += row

    def enemy_delete(self, index):
        removed_enemy = self.enemies.pop(index)
        removed_enemy.hideturtle()
        del removed_enemy

    def delete_all_enemies(self):
        for enemy in self.enemies:
            enemy.hideturtle()
            enemy.clear()
            del enemy
        self.enemies.clear()
        self.moving_right = True
        self.enemy_counter = 0

    def move_enemies(self, dt):
        move_step = ENEMY_X_MOVE_STEP * dt
        boundary_reached = False
        for enemy in self.enemies:
                if self.moving_right:
                    if enemy.xcor() >= X_MAX:
                        self.moving_right = False
                        boundary_reached = True
                        break
                else:
                    if  enemy.xcor() <= X_MIN:
                        self.moving_right = True
                        boundary_reached = True
                        break
        for enemy in self.enemies:
            if self.moving_right:
                enemy.setx(enemy.xcor() + move_step)
            else:
                enemy.setx(enemy.xcor() - move_step)

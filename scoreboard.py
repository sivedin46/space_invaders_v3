from constants import *
import time
from turtle import Turtle, Screen
import pygame


pygame.mixer.init()
level_sound = pygame.mixer.Sound(LEVEL_SOUND)


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("green")
        self.penup()
        self.hideturtle()
        self.reset_scoreboard()
        self.life_pos = (-360, 270)
        self.fps_pos = (-250, 270)
        self.level_pos = (-100, 270)
        self.speed_pos = (0, 270)
        self.record_pos = (200, 270)
        self.score_pos = (340, 270)
        self.font = BOARD_FONT
        self.read_record()
        self.screen = self.getscreen()
        self.screen.tracer(0)
        self.update_scoreboard()
        self.screen = Screen()

    def reset_scoreboard(self):
        self.clear()
        self.score = 0
        self.record_s = 0
        self.level = 1
        self.speed_inc_time = GAME_INC_TIME
        self.life_count = LIFE_COUNT
        self.speed = 1
        self.fps = 30

    def update_fps(self, fps):
        self.fps = round(fps)
        self.update_scoreboard()

    def update_scoreboard(self, ):
        self.clear()
        self.goto(self.life_pos)
        self.write(self.life_count, align="center", font=self.font, )
        self.goto(self.fps_pos)
        self.write(f"FPS: {self.fps}", align="center", font=self.font, )
        self.goto(self.level_pos)
        self.write(f"Level: {self.level}", align="center", font=self.font, )
        self.goto(self.speed_pos)
        self.write(f"Speed: {self.speed}", align="center", font=self.font, )
        self.goto(self.record_pos)
        self.write(f"Record: {self.record_s}", align="center", font=self.font)
        self.goto(self.score_pos)
        self.write(f"Score: {self.score}", align="center", font=self.font)

    def read_record(self):
        try:
            with open("records.txt", 'r', encoding='utf-8') as file:
                self.record_s = int(file.readline().strip())
                self.record_s = int(self.record_s) if self.record_s else 0
        except FileNotFoundError:
            self.record_s = 0
        except ValueError:
            self.record_s = 0

    def check_record(self):
        if self.score > self.record_s:
            self.record_s = self.score
            with open("records.txt", 'w', encoding='utf-8') as file:
                file.write(f"{self.record_s}")
            self.update_scoreboard()

    def calculate_score(self, obj):
        if obj == HIT_ENEMY:
            self.score += round(4 * len(self.life_count) * self.level / self.speed)
        elif obj == HIT_BOMB:
            self.score += 1
        elif obj == HIT_BONUS:
            self.score += 20
        self.update_scoreboard()
        return self.score

    def game_over(self):
        self.check_record()
        self.clear()
        self.goto(self.score_pos)
        self.write(f"Score: {self.score}", align="center", font=self.font)
        self.goto(0, 0)
        if self.life_count == "":
            pygame.mixer.music.load(GAME_OVER_SOUND)
            pygame.mixer.music.play()
            self.write("Game Over", align="center", font=("courier", 80, "normal"))
        else:
            pygame.mixer.music.load(WIN_SOUND)
            pygame.mixer.music.play()
            self.write("You Win'''", align="center", font=("courier", 80, "normal"))
        self.screen.update()
        time.sleep(3)
        pygame.mixer.music.stop()

    def game_level_check(self):
        level_sound.play()
        self.level += 1
        self.update_scoreboard()
        return self.level

    def game_speed_reset(self):
        self.speed_inc_time = GAME_INC_TIME
        self.speed = 1

    def game_speed_control(self, start_time):
        end_time = time.time()
        time_elapsed = int(end_time - start_time)  # elapsed time
        if time_elapsed > self.speed_inc_time and self.speed <= 6:
            self.speed_inc_time += GAME_INC_TIME
            self.speed += 1
            self.update_scoreboard()
        return self.speed

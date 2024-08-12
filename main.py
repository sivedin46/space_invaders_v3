from constants import *
import time
import sys
import tkinter as tk
from tkinter import simpledialog
from turtle import Screen
import pygame
from collision import detect_enemies, detect_fighter, detect_missile_bomb, detect_bonus
from enemies import Enemies
from enemybomb import EnemyBomb
from fighter import Fighter
from missile import Missile
from scoreboard import Scoreboard
from bonus import Bonus
from scalene import scalene_profiler
import os
import threading


class SpaceInvaders:
    def __init__(self):  # first initialize
        self.fps = GAME_FPS
        self.start_up_init()

    def start_up_init(self):
        self.play_music()
        self.screen = Screen()
        self.setup_screen()
        self.bring_window_to_front()
        self.level_check = 1
        self.real_fps = self.fps
        self.prev_time = time.perf_counter()
        self.current_time = time.time()
        self.step_time = 1 / self.fps
        self.dt = self.step_time
        self.count = 0
        self.accum = 0
        self.speed_factor = 1
        self.time_start = time.time()
        self.game_on = True
        self.fighter = Fighter(shape_path_fighter)
        self.enemies = Enemies(shape_path_enemy)
        self.missile = Missile()
        self.enemy_bomb = EnemyBomb(shape_enemy_bomb)
        self.scoreboard = Scoreboard()
        self.bonus = Bonus(shape_bonus)
        self.lock = threading.Lock()
        self.setup_events()
        self.main_loop()

    def bring_window_to_front(self):
        # This method will bring the window to the front
        root = self.screen.getcanvas().winfo_toplevel()
        root.lift()
        root.focus_force()

    def setup_screen(self):
        # Setup Main Screen
        self.screen.setup(width=820, height=620)  # self.screensize 800x600 (print(self.screen.self.screensize)
        self.screen.setworldcoordinates(-400, -300, 400, 300)
        self.screen.bgpic(shape_path_background)
        self.screen.title(SCREEN_TITLE)
        self.create_buttons()
        self.screen.register_shape(shape_path_fighter)
        self.screen.register_shape(shape_path_enemy)
        self.screen.register_shape(shape_enemy_bomb)
        self.screen.register_shape(shape_bonus)
        self.screen.tracer(0)

    def create_buttons(self):
        # Create Control Buttons
        self.canvas = self.screen.getcanvas()
        self.restart_button = tk.Button(self.canvas.master, text="Restart", command=self.restart_game)
        self.canvas.create_window(-360, 270, window=self.restart_button)
        self.fps_button = tk.Button(self.canvas.master, text="SetFPS", command=self.set_fps)
        self.canvas.create_window(-310, 270, window=self.fps_button)
        self.quit_button = tk.Button(self.canvas.master, text="Quit", command=self.quit_game)
        self.canvas.create_window(-268, 270, window=self.quit_button)

    def setup_events(self):
        # Setup Keys for gameplay
        self.screen.listen()
        self.screen.onkeypress(self.fighter.fighter_go_right, "Right")
        self.screen.onkeypress(self.fighter.fighter_go_left, "Left")
        self.screen.onkeypress(self.fighter.fighter_go_up, "Up")
        self.screen.onkeypress(self.fighter.fighter_go_down, "Down")
        self.screen.onkeypress(lambda: self.missile.control_missile(self.fighter.fighter), "space")

    def set_fps(self):
        # takes input from user and sets new target FPS
        fps_input = tk.simpledialog.askinteger("FPS SELECT", "Enter Fps", initialvalue=30, minvalue=5,
                                               maxvalue=120)
        self.fps = fps_input
        self.step_time = 1 / self.fps

    @staticmethod
    def play_music():
        pygame.mixer.init()
        pygame.mixer.music.load(GAME_SOUND)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)

    def restart_game(self):
        # Restarts game if user presses Restart button
        self.scoreboard.check_record()
        self.scoreboard.reset_scoreboard()
        self.enemies.delete_all_enemies()
        self.missile.delete_all_missiles()
        self.enemy_bomb.delete_all_bombs()
        self.fighter.delete_fighter()
        self.time_start = time.time()
        self.bonus.bonus_delete(self.time_start, self.bonus.bonus_l, True)
        self.start_up_init()
        self.scoreboard.update_scoreboard()

    def quit_game(self):
        # exit and close window if user presses quit button
        self.scoreboard.check_record()
        self.game_on = False
        pygame.quit()
        sys.exit()

    def game_reset(self):
        # clears screen and restarts some modules if user lost a life or level up
        self.enemy_bomb.delete_all_bombs()
        self.missile.delete_all_missiles()
        self.fighter.fighter_reset_pos()
        self.time_start = time.time()
        self.scoreboard.game_speed_control(self.time_start)
        self.scoreboard.update_scoreboard()

    def check_missile_collision(self):
        # Checks if user hit an enemy or not
        for fb_num, bomb in enumerate(self.missile.missiles):
            for index, enemy in enumerate(self.enemies.enemies):
                if detect_enemies(enemy, bomb):  # control for all enemies for fight bomb collision
                    self.missile.missile_delete(fb_num)
                    self.scoreboard.calculate_score(HIT_ENEMY)
                    self.enemies.enemy_delete(index)

    def check_bomb_collision(self):
        # Checks if enemies hit the user or not
        for eb_num, bomb in enumerate(self.enemy_bomb.bombs):
            if detect_fighter(self.fighter.fighter, bomb):  # control for fighter for enemy bomb collision
                self.scoreboard.life_count = self.scoreboard.life_count[:-1]
                self.game_reset()

    def check_missile_bomb_collision(self):
        # checks missile enemy bomb collision
        for eb_num, bomb in enumerate(self.enemy_bomb.bombs):
            for index, missile in enumerate(self.missile.missiles):
                if detect_missile_bomb(missile, bomb):  # control for fighter for enemy bomb collision
                    self.scoreboard.calculate_score(HIT_BOMB)
                    self.missile.missile_delete(index)
                    self.enemy_bomb.bomb_delete(eb_num)

    def check_bonus_collision(self):
        # checks whether user takes bonus or not
        for bonus in self.bonus.bonus_l:
            if detect_bonus(self.fighter.fighter, bonus):
                self.scoreboard.calculate_score(HIT_BONUS)
                create_time = time.time()
                self.bonus.bonus_delete(create_time, bonus, True)

    def bomb_cleanup(self):
        # checks and deletes if the bombs and missiles go out of screen
        self.enemy_bomb.check_bomb_status()
        self.missile.check_missiles_status()

    def game_startup(self):
        # normal game run procedures
        self.scoreboard.game_speed_control(self.time_start)
        self.enemies.move_enemies(self.speed_factor)
        self.bonus.create_new_bonus()
        self.missile.move_missiles()
        self.enemy_bomb.create_new_bomb(self.enemies.enemies)
        self.enemy_bomb.move_bombs(self.speed_factor, self.level_check)
        self.check_missile_collision()
        self.check_bomb_collision()
        self.check_missile_bomb_collision()
        self.check_bonus_collision()
        self.bomb_cleanup()

    def next_level(self):
        # checks the new level
        self.level_check = self.scoreboard.game_level_check()
        if self.level_check > 3:
            self.scoreboard.level = 3
            self.game_over()
        else:
            if self.level_check == 2:
                self.enemies.create_new_enemy(5)
            elif self.level_check == 3:
                self.enemies.create_new_enemy(6)
            self.scoreboard.game_speed_reset()
            self.game_reset()
            self.missile.speed_up_missiles(self.speed_factor)
            self.enemy_bomb.speed_up_bombs(self.speed_factor)
            self.enemies.enemy_counter = 0

    def game_over(self):
        self.scoreboard.game_over()
        self.game_on = False

    def game_logic(self):
        if self.scoreboard.life_count != "":  # check life of player
            if len(self.enemies.enemies):  # check is there any enemy
                self.game_startup()  # starts all needed
            else:
                self.next_level()  # destroyed all enemies, initialize game for next level
        else:
            self.game_over()  # player has no life

    def main_loop(self):
        while self.game_on:
            start_time = time.perf_counter()

            self.game_logic()
            while (time.perf_counter() - start_time) < self.step_time:
                pass
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            sleep_time = max(0, self.step_time - elapsed_time)
            # if sleep_time > 0:
            #     time.sleep(sleep_time)
            self.real_fps = 1 / (elapsed_time + sleep_time)
            self.scoreboard.update_fps(self.real_fps)
            self.speed_factor = min(max(self.scoreboard.speed * self.dt, 0.01), 10)

            self.screen.update()
        self.screen.mainloop()


if __name__ == "__main__":
    SpaceInvaders()

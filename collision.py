from constants import *
import pygame

pygame.mixer.init()
fighter_sound = pygame.mixer.Sound(FIGHTER_SOUND)
enemy_sound = pygame.mixer.Sound(ENEMY_SOUND)
bonus_sound = pygame.mixer.Sound(BONUS_SOUND)


def detect_enemies(enemy, fighter_missile):  # calculates distance and checks is there a collision if player hit enemy
    enemy_x = enemy.xcor()
    missile_x = fighter_missile.xcor()

    enemy_y = enemy.ycor()
    missile_y = fighter_missile.ycor()

    enemy_w = 24
    enemy_h = 24
    left = enemy_x - enemy_w / 2
    right = enemy_x + enemy_w / 2
    top = enemy_y + enemy_h / 2
    bottom = enemy_y - enemy_h / 2

    missile_w = 3
    missile_h = 16
    missile_left = missile_x - missile_w / 2
    missile_right = missile_x + missile_w / 2
    missile_top = missile_y + missile_h / 2
    missile_bottom = missile_y - missile_h / 2
    collision = (left < missile_right and right > missile_left and top > missile_bottom and bottom < missile_top)
    if collision:
        enemy_sound.play()
    return collision


def detect_fighter(fighter, enemy_bomb):
    fighter_x = fighter.xcor()
    bomb_x = enemy_bomb.xcor()

    fighter_y = fighter.ycor()
    bomb_y = enemy_bomb.ycor()

    fighter_w = 32
    fighter_h = 32
    left = fighter_x - fighter_w / 2
    right = fighter_x + fighter_w / 2
    top = fighter_y + fighter_h / 2
    bottom = fighter_y - fighter_h / 2

    bomb_w = 2
    bomb_h = 5
    bomb_left = bomb_x - bomb_w / 2
    bomb_right = bomb_x + bomb_w / 2
    bomb_top = bomb_y + bomb_h / 2
    bomb_bottom = bomb_y - bomb_h / 2
    collision = (left < bomb_right and right > bomb_left and top > bomb_bottom and bottom < bomb_top)
    if collision:
        fighter_sound.play()
    return collision


def detect_bonus(fighter, bonus):
    if bonus:
        fighter_x = fighter.xcor()
        bonus_x = bonus.xcor()

        fighter_y = fighter.ycor()
        bonus_y = bonus.ycor()

        fighter_w = 32
        fighter_h = 32
        left = fighter_x - fighter_w / 2
        right = fighter_x + fighter_w / 2
        top = fighter_y + fighter_h / 2
        bottom = fighter_y - fighter_h / 2

        bonus_w = 14
        bonus_h = 13
        bonus_left = bonus_x - bonus_w / 2
        bonus_right = bonus_x + bonus_w / 2
        bonus_top = bonus_y + bonus_h / 2
        bonus_bottom = bonus_y - bonus_h / 2
        collision = (left < bonus_right and right > bonus_left and top > bonus_bottom and bottom < bonus_top)
        if collision:
            bonus_sound.play()
        return collision
    else:
        return False


def detect_missile_bomb(missile, bomb):
    missile_x = missile.xcor()
    bomb_x = bomb.xcor()

    missile_y = missile.ycor()
    bomb_y = bomb.ycor()

    missile_w = 3
    missile_h = 16
    missile_left = missile_x - missile_w / 2
    missile_right = missile_x + missile_w / 2
    missile_top = missile_y + missile_h / 2
    missile_bottom = missile_y - missile_h / 2

    bomb_w = 4
    bomb_h = 5
    bomb_left = bomb_x - bomb_w / 2
    bomb_right = bomb_x + bomb_w / 2
    bomb_top = bomb_y + bomb_h / 2
    bomb_bottom = bomb_y - bomb_h / 2
    collision = (missile_left < bomb_right and missile_right > bomb_left
                 and missile_top > bomb_bottom and missile_bottom < bomb_top)
    return collision

################  Game Description:   #########################
* It has 3 levels and 7 speeds level
* Player has 3 lives
* Player can set desired gameplay FPS, quit game or restart game by buttons
* It gives user life count, current fps value, Level, Speed, Record and current Score Information


################       Score:   #########################
# self.score += round(4 * len(self.life_count) * self.level / self.speed)
* If you hit enemy you gain points depends on game level, users life count and speed.
Finishing fast in a level gives you more points
* If you hit bombs you gain 1 point
* If you get a bonus you gain 20 points
* It writes record to records.txt and checks

################       Level:   #########################
* Every level adds a new row of enemies
* Missiles moving speed increases
* Time delay between creation of missiles decreases
* Creation of bombs probability increases
* Speed of enemy bomb increases.

################    Speed Level:   #########################
* Every 20 seconds speed of enemy move  speed and  enemybomb speed increases
also

#################    Bonus     #########################
It creates arbitrary bonus object and it disappears after 3 seconds. If you take you gain 20 points

################   WARNING   ##############################
* If your fps value on screen  is variable, set fps a lower value.
Playing at right FPS value is important for collision detection

import pygame
from pygame import mixer
import math
import random

# initialize pygame
pygame.init()

# create the screen                width-x height-y top left corner is the x-0 y-0
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")

# Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# title And Display
pygame.display.set_caption("Space invaders")
# to insert a png file to this goto users>user>pycharm projects>copy it to this
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("Player.png")
PLayerX = 370
PLayerY = 480
PLayerX_change = 0
PLayerY_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(40)

# bullet

# Ready = you cant see the bullet on the screen
# Fire = the bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font("RustlerBarter.otf", 32)
# to download a new font go to bookmark on chrome and paste the font file in this py file
textX = 10
textY = 10

# Game over text
gameover_text = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = gameover_text.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))



def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
runnning = True
while runnning:

    # RGB = Red Green Blue
    screen.fill((0, 0, 0))
    # background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnning = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # if your putting a background change 0.3 to a higher value like 5 (do this for enemy and player @ blalal_change(in up and here))
                PLayerX_change = -5

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                PLayerX_change = 5

        # i am not going to put up and down if you want to go up and down PlayerY_change =0.5
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                PLayerY_change = 0

        # also in here
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                PLayerY_change = 0  # <- here.

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    # get the current X coordinate of the spaceship
                    bulletX = PLayerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PLayerX_change = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                PLayerY_change = 0

    # Meka + hari - hari kamaknaa
    # Passe therum ganna.
    PLayerY += PLayerY_change
    PLayerX += PLayerX_change

    # checking for boundaries of space ship so it doesn't get out.
    if PLayerX <= 0:
        PLayerX = 0

    elif PLayerX >= 736:
        PLayerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]
        # hari giye natham elif line ekata yatin danna
        # collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(PLayerX, PLayerY)
    show_score(textX, textY)
    pygame.display.update()

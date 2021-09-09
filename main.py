import pygame, sys
import random
import math

from pygame import mixer

"""
    pygame learning project.
    note the coordinates of the display are always [0,0] in the top left corner of the window
"""

# initialize pygame
pygame.init()

# display the screen
screen_Size = 800, 600  # width, height
screen = pygame.display.set_mode(screen_Size)

# Background
background = pygame.image.load(r'./assets/background_small.jpg')

# Background sound
mixer.music.load(r'.\assets\background.wav')
mixer.music.play(-1)

# Title and Icon
# change the caption name on window
pygame.display.set_caption("Space Invaders")
# load in an asset and assign the surface to a variable
icon = pygame.image.load(r"./assets/spaceship.png")
# change the icon that is displayed by window
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load(r"./assets/player.png")
playerImgSzX = playerImg.get_size()[0]
playerImgSzY = playerImg.get_size()[1]
# the image itself also has a zero index at the top left corner; translate half its pixels to center it
playerX = (0.5 * screen_Size[0]) - playerImgSzX / 2
playerY = (0.9 * screen_Size[1]) - playerImgSzY / 2
playerXChange = 0

# Enemy
enemyImg = []
enemyImgSzX = []
enemyImgSzY = []
enemyX = []
enemyY = []
enemySpeedX = []
enemySpeedY = []
enemyXChange = []
enemyYChange = []
numOfEnemies = 6

for i in range(numOfEnemies):
    enemyImg.append(pygame.image.load(r"./assets/ufo-003.png"))
    enemyImgSzX.append(enemyImg[i].get_size()[0])
    enemyImgSzY.append(enemyImg[i].get_size()[1])
    # the image itself also has a zero index at the top left corner; translate half its pixels to center it
    enemyX.append(random.randint(0, screen_Size[0] - enemyImgSzX[i]))
    enemyY.append(random.randint(0, 0.5 * screen_Size[1] - enemyImgSzY[i]))
    enemySpeedX.append(0.2)
    enemySpeedY.append(40)

enemyXChange = enemySpeedX
enemyYChange = enemySpeedY

# Bullet
BulletImg = pygame.image.load(r"./assets/bullet.png")
BulletImgSzX = BulletImg.get_size()[0]
BulletImgSzY = BulletImg.get_size()[1]
# the image itself also has a zero index at the top left corner; translate half its pixels to center it
BulletX = (0.5 * screen_Size[0]) - playerImgSzX / 2
BulletY = 0.9 * screen_Size[1] - playerImgSzY * 0.5
BulletSpeedX = 0.2
BulletSpeedY = 0.4
BulletXChange = BulletSpeedX
BulletYChange = BulletSpeedY
# ready = can't see the bullet on the screen
# fire = the bullet is currently moving
BulletState = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10 # maybe change these to be proportional to screen size
textY = 10

# Game over text
gg_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("score: " + str(score_value), True, (255,255,255)) #typcast score_value variable into string
    screen.blit(score, (x, y))

def game_over_text():
    gg_text = gg_font.render("Game Over", True, (255,255,255))
    screen.blit(gg_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def Enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def FireBullet(x, y):
    global BulletState  # use global to access he Bulletstate variable which is outside the name space of the function
    BulletState = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))


def isCollision(EnemyX, EnemyY, BulletX, BulletY):
    distance = math.sqrt(math.pow(EnemyX - BulletX, 2) + math.pow(EnemyY - BulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
while True:

    # Establish background
    # Red, Green, Blue
    color = 0, 0, 0
    # drawing background first then objects on top (otherwise objects will be underneath background)
    screen.fill(color)
    # load background image in each frame
    screen.blit(background, (0, 0))

    ''' Gather Keyboard Events
    This dictates the players controls'''
    for event in pygame.event.get():
        # if exit button is clicked then exit game
        if event.type == pygame.QUIT:
            sys.exit()

        # originally I defined playerX as an Int type, therefore I was unable to increment it by a decimal amount?
        # if this were true then setting the amount to 10 would have updated continuously. therefore not true
        # so why was the ship unable to continuously move with the key down?
        # TODO need to fixe the bug where the ship stops moving when changing directions quickly
        if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_LEFT and pygame.K_RIGHT:
            #     pass
            if event.key == pygame.K_LEFT:
                playerXChange = -0.3
            if event.key == pygame.K_RIGHT:
                playerXChange = 0.3
            if event.key == pygame.K_SPACE:
                if BulletState == "ready":
                    bullet_sound = mixer.Sound(r'.\assets\laser.wav')
                    bullet_sound.play()
                    BulletX = playerX
                    FireBullet(BulletX, BulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0

    '''Checking for boundries'''
    # Player movement
    playerX += playerXChange

    # Boundry check
    if playerX <= 0:
        playerX = 0
    elif playerX >= 800 - playerImgSzX:  # use the full length of the image because the zero index is in the top left corner
        playerX = 800 - playerImgSzX

    # enemyX = [enemyX[i] + enemyXChange[i] for i in range(numOfEnemies)]
    for i in range(numOfEnemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            game_over_text()
            break

        # Enemey Movement
        enemyX[i] += enemyXChange[i]

        # Boundry Check
        if enemyX[i] <= 0:  # TODO this section is not working after an enemey is hit by a bullet
            ''' Solved: The enemySpeed[i] method to alter the enemy speed, changed somehow and 
            became a negative when it wasn't supposed to? 
            The issue was i was not changing the sign back at the left boundary, placing a - in front of here as well
             solves the issue'''
            enemyXChange[i] = - enemySpeedX[i]
            enemyY[i] += enemyYChange[i]

        elif enemyX[i] >= 800 - playerImgSzX:  # use the full length of the image because the zero index is in TL
            enemyXChange[i] = -enemySpeedX[i]
            # print(enemySpeedX[i])
            enemyY[i] += enemyYChange[i]
        # collision
        collision = isCollision(enemyX[i], enemyY[i], BulletX, BulletY)
        if collision:
            collision_sound = mixer.Sound(r'.\assets\explosion.wav')
            collision_sound.play()
            BulletY = 0.9 * screen_Size[1] - playerImgSzY * 0.5
            BulletState = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 100)
        # Enemy Image Rendering
        Enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if BulletY <= 0:
        BulletY = 480
        BulletState = "ready"
    if BulletState == "fire":
        FireBullet(BulletX, BulletY)
        BulletY -= BulletYChange

    ''' Render Images'''
    # Player
    player(playerX, playerY)
    ''' show score '''
    show_score(textX, textY)
    ''' Update the Frame '''
    pygame.display.update()  # update the window

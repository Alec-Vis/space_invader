import sys, pygame
pygame.init()

size = width, height = 700, 700
speed = [2.22, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballrect = ballrect.move(speed) #update the coordinates of where the ball is on the screen
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top <0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black) # erase the current image with a black background, otherwise would have a trail of balls on the screen
    screen.blit(ball, ballrect) # copy previous image and reassign new coordinates
    pygame.display.flip() # update the visible display to make what we have drawn visible (by buffering the window?)

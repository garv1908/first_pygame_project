import pygame
import os
import math
from math import sqrt
import random

pygame.init()

screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

def random_position():
    """generates and returns a random x and y within the screen"""
    x = random.randint(0, screen.get_width())
    y = random.randint(0, screen.get_height())
    return x, y

def detect_collision(circle_center, circle_radius, ball_rect):
    ball_center = (ball_rect.centerx, ball_rect.centery)
    distance = sqrt((circle_center[0] - ball_center[0])**2 + (circle_center[1] - ball_center[1])**2)
    combined_radius = (circle_radius + ball_rect.width/2)
    return distance <= (combined_radius - ball_rect.width)

def load_png(name):
    """loads image and return image object"""
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(str(pygame.get_error()))
    return image, image.get_rect()

def stayOnScreen(posX, posY, radius):
    """function allowing relocation of objects when they move
        outside the screen.

        their x, y, and radius as input parameters

        returns a new x and y position if parameters go
        outside criteria"""
    if posX - radius > screen.get_width():
        posX = (posX - radius*2) - screen.get_width()
    if posX + radius < 0:
        posX = (posX + radius*2) + screen.get_width()
    if posY - radius > screen.get_height():
        posY = (posY - radius*2) - screen.get_height()
    if posY + radius < 0:
        posY = (posY + radius*2) + screen.get_height()
    return (posX, posY)

class Ball(pygame.sprite.Sprite):
    """A ball that will move across the screen
    Returns: ball object
    Functions: calcnewpos
    Attributes: area,"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('ball.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        xandy = random_position()
        self.rect.centerx = xandy[0]
        self.rect.centery = xandy[1]

    def calcnewpos(self, rect, vector):
        (angle, z) = vector
        (dx, dy) = (z * math.cos(angle), z * math.sin(angle))
        return rect.move(dx,dy)
    
def print_points(points):
    font = pygame.font.Font(None, 36)
    text = font.render("Points: {}".format(points), True, (255, 255, 255))
    screen.blit(text, (10, 10))

def main():
    global player_pos
    global running
    running = True
    dt = 0
    radius = 40

    points = 0

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    
    ball = Ball()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("purple")

        pygame.draw.circle(screen, "red", player_pos, radius)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            player_pos.y += 300 * dt
        if keys[pygame.K_a]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            player_pos.x += 300 * dt

        circlePos = stayOnScreen(player_pos.x, player_pos.y, radius)
        player_pos.x = circlePos[0]
        player_pos.y = circlePos[1]

        if detect_collision(circlePos, radius, ball.rect):
            print("Collision detected!")
            points += 1
            ball.kill()
            pygame.mixer.Sound(os.path.join('sounds', 'metal-hit-26-193292.mp3')).play()
            ball = Ball()
            
            if points % 10 == 0:
                radius += 5
            if points % 25 == 0:
                pygame.mixer.Sound(os.path.join('sounds', '8-bit-video-game-win-level-sound-version-1-145827.mp3')).play()
            if points % 100 == 0:
                print("You win!!!!!!!!!!")
                pygame.mixer.Sound(os.path.join('sounds', 'celebration.mp3')).play()
        
        screen.blit(ball.image, ball.rect)
        print_points(points)

        pygame.display.flip()
        dt = clock.tick(60) / 1000
    pygame.quit()

main()
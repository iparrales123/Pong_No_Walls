import pygame
import sys
import time
from random import randint
from pygame.locals import *

pygame.init()
# Set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
Some = (0, 255, 0)
Gold = (255, 215, 0, 255)
# Set the window
windowWidth = 800
windowHeight = 400
windowSurface = pygame.display.set_mode((windowWidth, windowHeight), 0, 32)
surface_rect = windowSurface.get_rect()
pygame.display.set_caption('Pong')

# Fonts that will be used on screen
font = pygame.font.SysFont("comicsansms", 30)
big_font = pygame.font.SysFont("comicsanms", 70)
small_font = pygame.font.SysFont("comicsansms", 50)

# For the key events later on
up = False
down = False
left = False
right = False
hit_sound = pygame.mixer.Sound("sound.wav")
win_sound = pygame.mixer.Sound("winning.wav")
lose_sound = pygame.mixer.Sound("losing.wav")
pygame.mixer.music.load("Temple_Of_Time.mp3")
pygame.mixer.music.play(-1, 0.0)


# ---------------------------------    Paddle     ---------------------------------------------------------------------
class Paddle(pygame.sprite.Sprite):
    def __init__(self, player_type):
        pygame.sprite.Sprite.__init__(self)
        self.player_type = player_type
        self.image = pygame.image.load('ex.png') if self.player_type < 10 else pygame.image.load('ex2.png')
        self.rect = self.image.get_rect()
        self.speed = 8

        if self.player_type == 1:
            self.rect.centerx = windowSurface.get_rect().right
            self.rect.centerx -= 20
            self.rect.centery = windowSurface.get_rect().centery
        elif self.player_type == 11:
            self.rect.centery = windowSurface.get_rect().top
            self.rect.centery += 10
            self.rect.centerx = windowSurface.get_rect().right - windowSurface.get_rect().centerx / 2
        elif self.player_type == 12:
            self.rect.centery = windowSurface.get_rect().bottom
            self.rect.centery -= 10
            self.rect.centerx = windowSurface.get_rect().right - windowSurface.get_rect().centerx / 2
        elif self.player_type == 2:
            self.rect.centerx = windowSurface.get_rect().left
            self.rect.centerx += 20
            self.rect.centery = windowSurface.get_rect().centery
        elif self.player_type == 21:
            self.rect.centery = windowSurface.get_rect().top
            self.rect.centery += 10
            self.rect.centerx = windowSurface.get_rect().left + windowSurface.get_rect().centerx / 2
        elif self.player_type == 22:
            self.rect.centery = windowSurface.get_rect().bottom
            self.rect.centery -= 10
            self.rect.centerx = windowSurface.get_rect().left + windowSurface.get_rect().centerx / 2

    def move(self):
        if self.player_type == 1:
            if (up is True) and (self.rect.y > 5):
                self.rect.y -= self.speed
            elif (down is True) and (self.rect.bottom < windowHeight - 5):
                self.rect.y += self.speed
        elif (self.player_type == 11) or (self.player_type == 12):
            if (left is True) and (self.rect.x > windowSurface.get_rect().centerx):
                self.rect.x -= self.speed
            elif (right is True) and (self.rect.right < windowWidth - 20):
                self.rect.x += self.speed

    def cpu_movexl(self, pix):
        self.rect.x -= pix
        if self.rect.x < 0:
            self.rect.x = 0

    def cpu_movexr(self, pix):
        self.rect.x += pix
        if self.rect.x > 400:
            self.rect.x = 400

    def cpu_moveu(self, pixel):
        self.rect.y -= pixel
        if self.rect.y < 0:
            self.rect.y = 0

    def cpu_moved(self, pixel):
        self.rect.y += pixel
        if self.rect.y > 400:
            self.rect.y = 400


# Create the paddles
paddle1a = Paddle(1)
paddle1b = Paddle(11)
paddle1c = Paddle(12)
paddle2a = Paddle(2)
paddle2b = Paddle(21)
paddle2c = Paddle(22)


# ---------------------------------  Ball   ---------------------------------------------------------------------------
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('final.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = surface_rect.centerx
        self.rect.centery = surface_rect.centery
        self.velocity = [randint(3, 5), randint(-5, 5)]

    def move(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]


# ---------------------------------------------------------------------------------------------------------------------
# Create thr ball and render all items to screen
ball = Ball()
all_sprites = pygame.sprite.RenderPlain(paddle1a, paddle1b, paddle1c, paddle2a, paddle2b, paddle2c, ball)

# Scores for the players
player_score = 0
cpu_score = 0
player_games = 0
cpu_games = 0


# Collisions
def hit():
    if pygame.sprite.collide_rect(ball, paddle1a) or pygame.sprite.collide_rect(ball, paddle2a):
        ball.velocity[0] = -ball.velocity[0]
        ball.velocity[1] = randint(-8, 8)
        hit_sound.play()
    elif pygame.sprite.collide_rect(ball, paddle1b) or pygame.sprite.collide_rect(ball, paddle2b):
        ball.velocity[0] = randint(4, 8)
        ball.velocity[1] = -ball.velocity[1]
        hit_sound.play()
    elif pygame.sprite.collide_rect(ball, paddle1c) or pygame.sprite.collide_rect(ball, paddle2c):
        ball.velocity[0] = randint(4, 8)
        ball.velocity[1] = -ball.velocity[1]
        hit_sound.play()


# ------------------------------- Run the game loop ------------------------------------------------------------------
while True:
    if ball.rect.x > windowWidth:
        ball.rect.centerx = surface_rect.centerx
        ball.rect.centery = surface_rect.centery
        ball.velocity = [randint(3, 6), randint(-5, 5)]
        cpu_score += 1
    elif ball.rect.x < 0:
        ball.rect.centerx = surface_rect.centerx
        ball.rect.centery = surface_rect.centery
        ball.velocity = [randint(3, 5), randint(-5, 5)]
        player_score += 1

    if player_score == 1:
        player_games += 1
        player_score = 0
    elif cpu_score == 11 and cpu_score >= player_score + 2:
        cpu_games += 1
        cpu_score = 0

    if player_games == 3:
        text = font.render(str("YOU WIN"), 1, BLACK)
        windowSurface.blit(text, (300, 300))
        win_sound.play()
    elif cpu_games == 3:
        text = font.render(str("YOU LOSE"), 1, BLACK)
        windowSurface.blit(text, (300, 300))
        win_sound.play()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                up = True
                down = False
            elif event.key == K_DOWN:
                up = False
                down = True
            elif event.key == K_RIGHT:
                right = True
                left = False
            elif event.key == K_LEFT:
                left = True
                right = False
        elif event.type == KEYUP:
            up = False
            down = False
            left = False
            right = False

        if ball.velocity[0] < 0 and ball.velocity[1] > 0:
            paddle2a.cpu_moved(10)
        if ball.velocity[0] < 0 and ball.velocity[1] < 0:
            paddle2a.cpu_moveu(10)
        if ball.velocity[0] < 0 and ball.velocity[1] > 0:
            paddle2b.cpu_movexr(10)
            paddle2c.cpu_movexr(10)
        if ball.velocity[0] < 0 and ball.velocity[1] < 0:
            paddle2b.cpu_movexl(10)
            paddle2c.cpu_movexl(10)

# Display the scores on the board
    score = font.render(str(cpu_score) + "               " + str(player_score), True, WHITE, Some)
    score_rect = score.get_rect()
    score_rect.centerx = surface_rect.centerx
    score_rect.y = 10
    games = font.render(str(cpu_games) + "               " + str(player_games), True, WHITE, Some)
    games_rect = games.get_rect()
    games_rect.centerx = surface_rect.centerx
    games_rect.y = 50

    windowSurface.fill(WHITE)
    windowSurface.blit(score, score_rect), windowSurface.blit(games, games_rect)

# Draws the net down the middle
    net_center = surface_rect.centerx

    net_rect0 = pygame.Rect(net_center, 0, 5, 5)
    net_rect1 = pygame.Rect(net_center, 60, 5, 5)
    net_rect2 = pygame.Rect(net_center, 120, 5, 5)
    net_rect3 = pygame.Rect(net_center, 180, 5, 5)
    net_rect4 = pygame.Rect(net_center, 240, 5, 5)
    net_rect5 = pygame.Rect(net_center, 300, 5, 5)
    net_rect6 = pygame.Rect(net_center, 360, 5, 5)
    net_rect7 = pygame.Rect(net_center, 395, 5, 5)

    pygame.draw.rect(windowSurface, Gold, (net_rect0.left, net_rect0.top, net_rect0.width, net_rect0.height))
    pygame.draw.rect(windowSurface, Gold, (net_rect1.left, net_rect1.top, net_rect1.width, net_rect1.height))
    pygame.draw.rect(windowSurface, Gold, (net_rect2.left, net_rect2.top, net_rect2.width, net_rect2.height))
    pygame.draw.rect(windowSurface, Gold, (net_rect3.left, net_rect3.top, net_rect3.width, net_rect3.height))
    pygame.draw.rect(windowSurface, Gold, (net_rect4.left, net_rect4.top, net_rect4.width, net_rect4.height))
    pygame.draw.rect(windowSurface, Gold, (net_rect5.left, net_rect5.top, net_rect5.width, net_rect5.height))
    pygame.draw.rect(windowSurface, Gold, (net_rect6.left, net_rect6.top, net_rect6.width, net_rect6.height))

    all_sprites.draw(windowSurface)
    paddle1a.move(), paddle1b.move(), paddle1c.move()
    ball.move()
    hit()

    pygame.display.update()
    time.sleep(0.02)

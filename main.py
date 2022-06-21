import pygame
from pygame.locals import *
import random

class Platform:
    image = pygame.image.load("platforma.png")
    counter = 0

    def __init__(self, x, y, ):

        self.x = x
        self.y = y
        self.image = pygame.image.load("platforma.png")
        self.rect = Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        Platform.counter += 1
        if Platform.counter % 10 == 0:
            self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, self.image.get_height()))
            self.x = 0

        self.rect = Rect(self.x, self.y, self.image.get_width(), self.image.get_height() / 3)

    def draw(self):
        screen.blit(self.image, (self.x + offsetX, self.y + offsetY))

# Rozpoczyna działanie PyGame
pygame.init()

# Dzięki tym dwóm linijkom mamy stałe 60 klatek na sekundę;
clock = pygame.time.Clock()
fps = 60


# ZMIENNE GRACZA:

# # Zmienne przechowujące pozycje gracza:
playerX = 100
playerY = 539

# # Zmienne przechowujące prędkość gracza:
playerVelocityX = 0
playerVelocityY = 0

# Wymiary okna gry przechowywane w postaci dwóch zmiennych:
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
canJump = False
# screen - Okienko gry (oraz wybranie rozdzielczości ekranu;
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Nazwa okienka
pygame.display.set_caption('Gierka')


# Wczytanie obrazka do obiektu
hero = pygame.image.load('ludzik.png')

# Platform
platformList = []
for i in range(100):
    posX = random.randint(0, SCREEN_WIDTH - 300)
    posY = 600 - 180 * i
    platformList.append(Platform(posX, posY))


offsetX = 0
offsetY = 0

playerRect = Rect(playerX, playerY, hero.get_width(), hero.get_height())

run = True
while run:
    # Zegar gry - pilnuje, żeby gra działała w 60-ciu FPS-ach.
    clock.tick(fps)

    # LOGIKA GRY:

    # Przechwytywanie klawiszy gry:
    keys = pygame.key.get_pressed()
    if keys[K_UP] and canJump:
        playerVelocityY -= 10 + 0.7 * abs(playerVelocityX)
        canJump = False
    if keys[K_LEFT]:
        playerVelocityX -= 1
    if keys[K_RIGHT]:
        playerVelocityX += 1

    if keys[K_w]:
        offsetY += 1
    if keys[K_s]:
        offsetY -= 5
    # Dodanie siły grawitacji do gry;
    playerVelocityY += 0.3

    # Dodanie siły oporu:
    playerVelocityX *= 0.98
    playerVelocityY *= 0.98


    playerX += playerVelocityX
    playerY += playerVelocityY



    # Sprawdzanie, czy gracz nie wyszedł poza ekran;
    if playerX < 0:
        playerX = 0
        playerVelocityX *= -1
    if playerX > SCREEN_WIDTH - hero.get_width():
        playerX = SCREEN_WIDTH - hero.get_width()
        playerVelocityX *= -1

    # if playerY < 0:
    #     playerY = 0
    #     playerVelocityY = 0

    if playerY > SCREEN_HEIGHT - hero.get_height():
        playerY = SCREEN_HEIGHT - hero.get_height()
        playerVelocityY = 0
        canJump = True

    playerRect = Rect(playerX, playerY, hero.get_width(), hero.get_height())
    for platform in platformList:
        if platform.rect.colliderect(playerRect) and playerVelocityY > 0:
            playerY = platform.y - hero.get_height()
            playerVelocityY = 0
            canJump = True


    offsetY += 1
    # if (playerY - 600 + hero.get_height()) > -offsetY:
    #     offsetY = abs(playerY - 600 + hero.get_height())

    if playerY + offsetY < 250:
        offsetY += abs(playerY + offsetY - 250)/30
    if playerY + offsetY > SCREEN_HEIGHT:
        run = False


    # RYSOWANIE OBIEKTÓW W GRZE:

    # Wypełnienie ekranu gry:
    screen.fill((180, 255, 255))

    # Rysowane obiektów na ekranie
    screen.blit(hero, (playerX, playerY + offsetY))
    for platform in platformList:
        platform.draw()


    # To jest TURBOWAŻNE I NIE USUWAJ TEGO!!!
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # To tworzy nową klatkę gry;
    pygame.display.update()
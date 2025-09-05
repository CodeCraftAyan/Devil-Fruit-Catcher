import pygame
from pygame import mixer
import random

# Initialize
pygame.init()
mixer.init()

# Screen
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Devil Fruits Catcher - (ONE PIECE)")
logo_icon = pygame.image.load('img/logo.png')
pygame.display.set_icon(logo_icon)
background = pygame.transform.scale(pygame.image.load('img/background.jpg'), (900, 600))

# Fonts
font = pygame.font.Font("txt/PixelifySans-Regular.ttf", 20)
big_font = pygame.font.Font("txt/PixelifySans-Regular.ttf", 38)
ultra_big = pygame.font.Font("txt/PixelifySans-Regular.ttf", 125)

# Sounds
mixer.music.load('sounds/we_are_background.mp3')
mixer.music.set_volume(0.6)
mixer.music.play(-1)
touch_sound = mixer.Sound('sounds/touch.mp3')

# Playerss
shipImg = pygame.transform.scale(pygame.image.load('img/ship.webp'), (100, 100))
shipX, shipY = 400, 480
shipX_change = 0

def player(x, y):
    screen.blit(shipImg, (x, y))

# Fruits
fruit_images = [
    pygame.transform.scale(pygame.image.load('img/hito_hito_nomi_nika.webp'), (64, 64)),
    pygame.transform.scale(pygame.image.load('img/tori_tori_nomi.webp'), (64, 64)),
    pygame.transform.scale(pygame.image.load('img/mera_mera_nomi.webp'), (64, 64)),
    pygame.transform.scale(pygame.image.load('img/uo_uo_nomi.png'), (40, 64)),
    pygame.transform.scale(pygame.image.load('img/hana_hana_nomi.png'), (64, 64))
]

fruitX = random.randint(0, 836)
fruitY = random.randint(15, 100)
currentFruitImg = random.choice(fruit_images)

def devilFruit(x, y, image):
    screen.blit(image, (x, y))

# Score
score = 0

def showScore():
    scoreText = font.render(f"Fruits Point {score}", True, (0,110,255))
    screen.blit(scoreText, (740, 15))

def is_collision(x1, y1, x2, y2):
    return pygame.Rect(x1, y1, 100, 100).colliderect(pygame.Rect(x2, y2, 64, 64))

def showGameOver():
    screen.fill((0, 0, 0))
    start_bg = pygame.transform.scale(pygame.image.load('img/start_bg.webp'), (900, 600))

    over_text = ultra_big.render("GAME OVER", True, (239, 35, 60))
    score_text = font.render(f"You Collected {score} Devil Fruits.", True, (0, 0, 0))
    screen.blit(start_bg, (0, 0))
    screen.blit(over_text, (130, 200))
    screen.blit(score_text, (320, 320))
    pygame.display.update()
    pygame.time.wait(6000)

def showStartText():
    screen.fill((243, 213, 181))
    title = big_font.render("Press Any Key to Start", True, (255, 255, 255))
    created = font.render("Created by Ayan Mandal", True, (255, 255, 255))
    one_piece_img = pygame.transform.scale(pygame.image.load('img/one_piece.png'), (400, 200))
    start_bg = pygame.transform.scale(pygame.image.load('img/start_bg.jpg'), (900, 600))

    screen.blit(start_bg, (0, 0))
    screen.blit(title, (230, 500))
    screen.blit(one_piece_img, (240, 150))
    screen.blit(created, (330, 570))

    pygame.display.update()

# Wait for any key to start
waiting = True
while waiting:
    showStartText()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            waiting = False
            start_time = pygame.time.get_ticks()

# Game timer
time_limit = 60000  # 60 sec

# Game Loop
running = True
while running:
    screen.fill("skyblue")
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shipX_change = -0.7
            if event.key == pygame.K_RIGHT:
                shipX_change = 0.7
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                shipX_change = 0

    # Timer check
    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time >= time_limit:
        showGameOver()
        break

    shipX += shipX_change
    shipX = max(0, min(shipX, 800))
    player(shipX, shipY)

    fruitY += 0.5
    devilFruit(fruitX, fruitY, currentFruitImg)

    if is_collision(shipX, shipY, fruitX, fruitY):
        touch_sound.play()
        score += 1
        fruitX = random.randint(0, 836)
        fruitY = random.randint(10, 200)
        currentFruitImg = random.choice(fruit_images)

    if fruitY > 600:
        fruitX = random.randint(0, 836)
        fruitY = random.randint(10, 200)
        currentFruitImg = random.choice(fruit_images)

    showScore()

    # Timer display
    remaining_time = max(0, (time_limit - elapsed_time) // 1000)
    time_text = font.render(f"Time Left {remaining_time}s", True, (239, 35, 60))
    screen.blit(time_text, (30, 10))

    pygame.display.update()

pygame.quit()
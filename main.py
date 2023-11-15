import pygame
import random

from pygame import mixer

# Initialize Pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("images/background.jpg")

# BGM
mixer.music.load("sounds/bgm.wav")
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("First game")
icon = pygame.image.load("ico.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load("images/ship.png")
player_x = 370
player_y = 480
player_x_delta = 0
player_y_delta = 0

# Score
score_value = 0
font = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 32)
text_x = 10
text_y = 10

# Game over
go_font = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 64)
go_sound = mixer.Sound("sounds/go.wav")

# Enemy
num_enemies = 10
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_delta = []
enemy_y_delta = []
enemy_explosion_sound = mixer.Sound("sounds/boom.wav")

for _ in range(num_enemies):
    enemy_img.append(pygame.image.load("images/enemy.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(0, 150))
    enemy_x_delta.append(0.15)
    enemy_y_delta.append(64)

# Bullet
bullet_img = pygame.image.load("images/bullet.png")
bullet_x = 0
bullet_y = 480
bullet_y_delta = 0.6
bullet_state = "ready"
bullet_sound = mixer.Sound("sounds/shot.wav")


def show_score(x: int, y: int) -> None:
    score = font.render(
        f"Score  {str(score_value)}",
        True,
        (255, 255, 255)
    )
    screen.blit(score, (x, y))


# Loads player and enemy pngs at initial coordinates
def player(x: int | float, y: int | float) -> None:
    screen.blit(player_img, (x, y))


def enemy(x: int | float, y: int | float, i: int) -> None:
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x: int | float, y: int | float) -> None:
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y - 24))
    bullet_sound.play()


def collision(x_one, x_two, y_one, y_two):
    distance = round((((x_one - x_two) ** 2) + ((y_one - y_two) ** 2)) ** 0.5, 2)
    if distance < 27:
        return True
    return False


def game_over() -> None:
    game_over_text = go_font.render(
        f"GAME OVER",
        True,
        (255, 255, 255)
    )
    screen.blit(game_over_text, (270, 250))
    go_sound.play(1)


# Game loop
running = True
while running:

    # Load bg image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_delta = - 0.3
            if event.key == pygame.K_RIGHT:
                player_x_delta = 0.3
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_delta = 0

    # Player movement
    player_x += player_x_delta

    # Player boundaries
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Enemy movement
    for i in range(num_enemies):

        # Game over
        if enemy_y[i] > 440:
            for j in range(num_enemies):
                enemy_y[j] = 2000
            game_over()
            break

        enemy_x[i] += enemy_x_delta[i]
        if enemy_x[i] <= 0:
            enemy_x_delta[i] = 0.15
            enemy_y[i] += enemy_y_delta[i]
        elif enemy_x[i] >= 736:
            enemy_x_delta[i] = - 0.15
            enemy_y[i] += enemy_y_delta[i]

        collision_state = collision(enemy_x[i], bullet_x, enemy_y[i], bullet_y)
        if collision_state:
            enemy_explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(0, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_delta

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()

import pygame
import sys
import random

def spawn_enemy():
    return pygame.Rect(random.randint(0, WIDTH - 50), random.randint(-50, 0), 50, 50)

def start_new_level():
    global level
    level += 1

def show_menu():
    play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
    pygame.draw.rect(screen, (44, 62, 80), play_button)  
    
    font_menu = pygame.font.Font(None, 36)
    play_text = font_menu.render("PLAY", True, (255, 255, 255))
    text_rect = play_text.get_rect(center=play_button.center)
    screen.blit(play_text, text_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.collidepoint(event.pos):
                    return

def show_loss_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 48)
    text = font.render("You Lost", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)
    
    play_again_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 25, 200, 50)
    pygame.draw.rect(screen, (44, 62, 80), play_again_button)
    play_again_text = font.render("Play Again", True, (255, 255, 255))
    play_again_rect = play_again_text.get_rect(center=play_again_button.center)
    screen.blit(play_again_text, play_again_rect)
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_again_button.collidepoint(event.pos):
                    return True

pygame.init()

WIDTH, HEIGHT = 350, 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Shooting Game")

background_img = pygame.image.load("bg.png") 
background_img = pygame.transform.scale(background_img, (350, 600))

player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
bullet_img = pygame.image.load("bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (20, 40))

player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 70, 50, 50)

enemies = []
player_bullets = []
enemy_bullets = []

clock = pygame.time.Clock()

score = 0
level = 1
font = pygame.font.Font(None, 18)

shoot_interval = 10 
shoot_counter = 0

spawn_interval = 60  
spawn_timer = 0

pygame.mixer.music.load("backgroundmusic.mp3") 
pygame.mixer.music.play(-1) 

show_menu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.left > 0:
        player.x -= 5
    if keys[pygame.K_d] and player.right < WIDTH:
        player.x += 5
    if keys[pygame.K_w] and player.top > 0:
        player.y -= 5
    if keys[pygame.K_s] and player.bottom < HEIGHT:
        player.y += 5

    if shoot_counter == 0:
        player_bullet = pygame.Rect(player.centerx - 5, player.top, 10, 30)
        player_bullets.append(player_bullet)
        shoot_counter = shoot_interval
    else:
        shoot_counter -= 1

    player_bullets = [bullet for bullet in player_bullets if bullet.move_ip(0, -10)]

    spawn_timer += 3
    if spawn_timer >= spawn_interval:
        enemies.append(spawn_enemy())
        spawn_timer = 0

    for enemy in enemies[:]:  
        enemy.move_ip(0, 2)
        if enemy.top > HEIGHT:
            enemies.remove(enemy)
            continue
        for player_bullet in player_bullets[:]:  
            if player_bullet.colliderect(enemy):
                player_bullets.remove(player_bullet)
                enemies.remove(enemy)
                score += 20
        if player.colliderect(enemy):  
            if show_loss_screen():  
                player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 70, 50, 50)  
                enemies.clear()  
                player_bullets.clear()  
                score = 0  
                level = 1  

    screen.blit(background_img, (0, 0))

    screen.blit(player_img, player)

    for enemy in enemies:
        screen.blit(enemy_img, enemy)

    for player_bullet in player_bullets:
        screen.blit(bullet_img, player_bullet)

    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    clock.tick(FPS)

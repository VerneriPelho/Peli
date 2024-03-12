import pygame
import sys
import random

def spawn_enemy():
    return pygame.Rect(random.randint(0, WIDTH - 50), random.randint(-50, 0), 50, 50)

def start_new_level():
    global level
    level += 1

def show_menu():
    title_font = pygame.font.Font(None, 64)
    title_text = title_font.render("Space Invader", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    
    # Blur the background image
    blurred_background = pygame.transform.smoothscale(background_img, (WIDTH // 4, HEIGHT // 4))
    blurred_background = pygame.transform.smoothscale(blurred_background, (WIDTH, HEIGHT))

    screen.blit(blurred_background, (0, 0))
    screen.blit(title_text, title_rect)
    
    play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT * 2 // 3, 200, 50)
    pygame.draw.rect(screen, (0, 128, 128), play_button)  # Change the button color
    
    play_font = pygame.font.Font(None, 36)
    play_text = play_font.render("PLAY", True, (255, 255, 255))
    play_rect = play_text.get_rect(center=play_button.center)
    
    screen.blit(play_text, play_rect)

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
    pygame.mouse.set_visible(True)  # Show the cursor
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 48)
    text = font.render("You Lost", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)
    
    # Blur background image
    blurred_background = pygame.transform.smoothscale(background_img, (WIDTH // 4, HEIGHT // 4))
    blurred_background = pygame.transform.smoothscale(blurred_background, (WIDTH, HEIGHT))

    screen.blit(blurred_background, (0, 0))
    
    play_again_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 25, 200, 50)
    pygame.draw.rect(screen, (0, 128, 128), play_again_button)  # Change the button color
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
                    pygame.mouse.set_visible(False)  # Hide the cursor
                    return True

pygame.init()

WIDTH, HEIGHT = 338, 600  # Set the screen size
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Shooting Game")

background_img = pygame.image.load("bg.png").convert_alpha()
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
bullet_img = pygame.image.load("bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (20, 40))

class Player:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.shoot_delay = 0
        self.shoot_cooldown = 10

    def draw(self, win):
        win.blit(player_img, self.rect.topleft)

    def move(self, x, y):
        self.rect.move_ip(x, y)

    def shoot(self):
        if self.shoot_delay == 0:
            bullet = Bullet(self.rect.centerx - 5, self.rect.top)
            bullets.append(bullet)
            self.shoot_delay = self.shoot_cooldown
        else:
            self.shoot_delay -= 1

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, bullet_img.get_width(), bullet_img.get_height())

    def draw(self, win):
        win.blit(bullet_img, self.rect.topleft)

    def move(self, vel):
        self.rect.y -= vel
        return self.rect.y > 0  # Return True if bullet is still on screen

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, enemy_img.get_width(), enemy_img.get_height())

    def draw(self, win):
        win.blit(enemy_img, self.rect.topleft)

    def move_ip(self, x, y):
        self.rect.move_ip(x, y)

player = Player(WIDTH // 2 - 25, HEIGHT - 70, 50, 50)
enemies = []
bullets = []

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

pygame.mouse.set_visible(False)  # Hide the cursor initially

def handle_shooting():
    # Check for shooting
    if pygame.mouse.get_pressed()[0]:  # Check left mouse button
        player.shoot()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Move player towards the mouse
    player.rect.centerx = mouse_x
    player.rect.centery = mouse_y

    handle_shooting()

    # Move bullets
    bullets = [bullet for bullet in bullets if bullet.move(10)]

    spawn_timer += 2
    if spawn_timer >= spawn_interval:
        enemies.append(Enemy(*spawn_enemy().topleft))
        spawn_timer = 0

    for enemy in enemies[:]:  
        enemy.move_ip(0, 2)
        if enemy.rect.top > HEIGHT:
            enemies.remove(enemy)
            continue
        for bullet in bullets[:]:  
            if bullet.rect.colliderect(enemy.rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 20
        if player.rect.colliderect(enemy.rect):  
            if show_loss_screen():  
                player = Player(WIDTH // 2 - 25, HEIGHT - 70, 50, 50)  
                enemies.clear()  
                bullets.clear()  
                score = 0  
                level = 1  

    screen.blit(background_img, (0, 0))

    for enemy in enemies:
        enemy.draw(screen)

    player.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)

    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    clock.tick(FPS)

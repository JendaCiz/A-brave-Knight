import pygame
import random

# Inicializace pygame
pygame.init()

# Nastavení obrazovky
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drak Hra")

# Barvy
WHITE = (255, 255, 255)

# Načtení obrázků
bg = pygame.image.load('img/battleback1.png')  # Předpokládáme, že máte pozadí hry
player_img = pygame.image.load('img/player.png')
dragon_img = pygame.image.load('img/dragon.png')

player_pos = [WIDTH/2, HEIGHT - player_img.get_height() - 10]
player_speed = 5
dragons = []

def spawn_dragon():
    """Vytvoří nového draka na náhodné pozici na horním okraji obrazovky."""
    x = random.randint(0, WIDTH - dragon_img.get_width())
    y = 0 - dragon_img.get_height()
    speed = random.randint(2, 6)
    dragons.append([x, y, speed])

clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)
    screen.blit(bg, (0, 0))
    screen.blit(player_img, player_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] - player_speed > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] + player_speed < WIDTH - player_img.get_width():
        player_pos[0] += player_speed

    if random.random() < 0.03:  # 3% šance na spawn draka každý frame
        spawn_dragon()

    for dragon in dragons[:]:
        dragon[1] += dragon[2]
        screen.blit(dragon_img, (dragon[0], dragon[1]))
        if dragon[1] > HEIGHT:
            dragons.remove(dragon)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

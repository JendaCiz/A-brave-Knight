import pygame
import random

# Inicializace pygame
pygame.init()

# Konstanty
width, height = 800, 600
gravity = 1
player_fall_speed = 0
player_jump_power = -15
bg_color = (135, 206, 235)

# Nastavení okna
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Skákání po mracích")

# Načtení obrázků
player_image = pygame.image.load("img/player2.png")
player_image_rect = player_image.get_rect(topleft=(width // 2, height // 2))

cloud_images = [
    pygame.image.load("img/cloud1.png"),
    pygame.image.load("img/cloud2.png"),
]

clouds = [(random.randint(0, width-100), random.randint(0, height-100)) for _ in range(5)]

# Hlavní smyčka
running = True
while running:
    screen.fill(bg_color)
    
    player_on_cloud = False
    for cloud_x, cloud_y in clouds:
        screen.blit(random.choice(cloud_images), (cloud_x, cloud_y))
        
        cloud_rect = pygame.Rect(cloud_x, cloud_y, cloud_images[0].get_width(), cloud_images[0].get_height())
        if player_image_rect.colliderect(cloud_rect):
            player_on_cloud = True

    if player_on_cloud:
        player_fall_speed = 0
    elif player_image_rect.bottom < height:
        player_fall_speed += gravity
        player_image_rect.y += player_fall_speed
    else:
        player_fall_speed = 0
        player_image_rect.y = height - player_image.get_height()

    screen.blit(player_image, player_image_rect.topleft)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_on_cloud:
                player_fall_speed = player_jump_power

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

import pygame
pygame.init()

width = 900
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("The Tales Of Brave Knight")

# Nastaveni parametru pohybu
distance = 5
fps = 60
clock = pygame.time.Clock()

# Background
background_image = pygame.image.load("img/battleback1.png")
background_image_rect = background_image.get_rect()
background_image_rect.center = (width // 2, height // 2)

# Player
player_image = pygame.image.load("img/player2.png")
player_image_rect = player_image.get_rect()
player_image_rect.center = (width // 8, height // 2)


# Nacteni snimku portalu do seznamu
portal_frames = []
for i in range(4):
    portal_frame = pygame.image.load(f"img/portal{i}.png")
    portal_frames.append(portal_frame)

frame_index = 0
animation_speed = 200  # Casovy interval mezi snimky (v milisekundach)
last_update_time = 0

# Nacteni snimku pavouka do seznamu
spider_frames = []
for i in range(2):
    spider_frame = pygame.image.load(f"img/spider{i}.png")
    spider_frames.append(spider_frame)

frame_index_spider = 0
spider_animation_speed = 500  # Casovy interval mezi snimky (v milisekundach)
spider_last_update_time = 0

# Pocatecni hodnoty pro pohyb pavouka
spider_y = height // 2  # Pocatecni vertikalni pozice pavouka
spider_speed = 1  # Rychlost pohybu pavouka


# Font
custom_font = pygame.font.Font("fonts/medieval_font.ttf", 35)

# Vypsani nazvu hry
custom_text = custom_font.render("The Tales Of Brave Knight", True, "Gray")
custom_text_rect = custom_text.get_rect()
custom_text_rect.center = (width // 2, 35)

# Hudba v pozadi
pygame.mixer.music.load("media/background_music.mp3")
# Prehrani hudby v pozadi
pygame.mixer.music.play(-1)


############################################################################
# Hlavni cyklus
game_over = False  # Stav hry - False znamena, ze hra bezi normalne
lets_continue = True
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False

    # Pridani pohybu na sipkach a vymezeni pohybu mimo obrazovku
    if not game_over:
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_image_rect.top > 0:
            player_image_rect.y -= distance
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_image_rect.bottom < height:
            player_image_rect.y += distance
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_image_rect.left > 0:
            player_image_rect.x -= distance
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_image_rect.right < width:
            player_image_rect.x += distance

    # Aktualizace pozice pavouka, pokud není stav "Game Over"
    if not game_over:
        spider_y += spider_speed

        # Otoceni smeru, kdyz pavouk dosahne horni nebo dolni hranice okna
        if spider_y <= 0 or spider_y + spider_frames[frame_index_spider].get_height() - 10 >= height:
            spider_speed *= -1
            

    # Vytvorení obdélníků pro hráče a pavouka pro kolizní detekci
    player_collision_rect = player_image.get_rect(topleft=player_image_rect.topleft)
    spider_collision_rect = spider_frames[frame_index_spider].get_rect(topleft=(width - spider_frames[frame_index_spider].get_width() - 150, spider_y))

    # Nastaveni parametru kolize hrace a pavouka
    player_collision_rect = pygame.Rect(player_image_rect.x + 20, player_image_rect.y + 10, player_image_rect.width - 40, player_image_rect.height - 20)
    spider_collision_rect = pygame.Rect(width - spider_frames[frame_index_spider].get_width() - 150 + 20, spider_y + 10, spider_frames[frame_index_spider].get_width() - 40, spider_frames[frame_index_spider].get_height() - 20)

    # Vyplneni obrazovky obrazky apod.
    screen.blit(background_image, background_image_rect)  # Pozadi
    screen.blit(player_image, player_image_rect)  # Player
    screen.blit(custom_text, custom_text_rect)  # Text hry / nadpis.... nwm jak to pojmenovat

    # Portal
    screen.blit(portal_frames[frame_index], (width - 40 - portal_frames[frame_index].get_width() // 2, height // 2 - portal_frames[frame_index].get_height() // 2))
    
    # Pavouk
    if not game_over:
        screen.blit(spider_frames[frame_index_spider], (width - spider_frames[frame_index_spider].get_width() - 150, spider_y))

    # Animace - zmena snimku portálu po uplynuti casoveho intervalu
    current_time = pygame.time.get_ticks()
    if current_time - last_update_time > animation_speed:
        frame_index = (frame_index + 1) % len(portal_frames)
        last_update_time = current_time

    current_time = pygame.time.get_ticks()
    if current_time - spider_last_update_time > spider_animation_speed and not game_over:
        frame_index_spider = (frame_index_spider + 1) % len(spider_frames)
        spider_last_update_time = current_time

    # Zkontrolujeme kolizi pouze pokud stav hry neni "Game Over"
    if not game_over:
        # Kontrola kolize a zobrazeni "Game Over"
        if player_collision_rect.colliderect(spider_collision_rect):
            # Nastavime stav "Game Over"
            game_over = True
            # Zastavime pohyb pavouka po kolizi
            spider_speed = 0

    # Pokud je stav hry "Game Over", zobrazime "Game Over" text a moznost restartovat hru
    if game_over:
        screen.blit(spider_frames[frame_index_spider], (width - spider_frames[frame_index_spider].get_width() - 150, spider_y))  # Pavouk zustane na miste po kolizi

        game_over_text = custom_font.render("Game Over - Press 'R' to Restart", True, "Red")
        game_over_text_rect = game_over_text.get_rect(center=(width // 2, height // 2))
        screen.blit(game_over_text, game_over_text_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Pokud hrac stiskne klavesu 'R', resetujeme hru
            game_over = False
            player_image_rect.center = (width // 8, height // 2)
            spider_y = height // 2
            spider_speed = 1

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
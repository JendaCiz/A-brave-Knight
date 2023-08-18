import pygame
pygame.init()

width = 900
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("The Tales Of Brave Knight")

#Nastaveni parametru pohybu
distance = 5
fps = 60
clock = pygame.time.Clock()

#Backrougnd 
background_image = pygame.image.load("img/battleback1.png")
background_image_rect = background_image.get_rect()
background_image_rect.center = (width//2, height//2)

#PLayer
player_image = pygame.image.load("img/player.png")
player_image_rect = player_image.get_rect()
player_image_rect.center = (width//8, height//2)

#Portal
portal_img = pygame.image.load("img/portal1.png")
portal_img_rect = portal_img.get_rect()
portal_img_rect.center = (width -40, height//2)

#Fotnts
custom_font = pygame.font.Font("fonts/medieval_font.ttf", 35)

#Vypsani nazvu hry
custom_text = custom_font. render("The Tales Of Brave Knight", True, "Gray")
custom_text_rect = custom_text.get_rect()
custom_text_rect.center = (width//2, 35)

#Hudba v pozadi
pygame.mixer.music.load("media/background_music.mp3")
#Prehrani hudby v pozadi
pygame.mixer.music.play(-1)


############################################################################
#Hlavni cyklus
lets_continue = True
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False
############################################################################
# Pridani pohybu na sipkach  a vymezeni pohybu mimo obrazovku
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_image_rect.top > 0:
        player_image_rect.y -= distance
    elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_image_rect.bottom < height:
        player_image_rect.y += distance
    elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_image_rect.left > 0:
        player_image_rect.x -= distance
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_image_rect.right < width:
        player_image_rect.x += distance

    # Vyplneni obrazovky obrazky apod..
    screen.blit(background_image, background_image_rect)  #Pozadi
    screen.blit(player_image, player_image_rect)          #Player  
    screen.blit(custom_text, custom_text_rect)            #Text hry / nadpis.... nwm jak to pojmenovat
    screen.blit(portal_img, portal_img_rect)              #Portal

    pygame.display.update()

    #Tikani hodin
    clock.tick(fps)


pygame.quit()
import pygame
import random

pygame.init()

width = 900
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("The Tales Of Brave Knight")

distance = 5
fps = 60
clock = pygame.time.Clock()

background_images = [pygame.image.load(f"img/battleback{i}.png") for i in range(1, 10)]

player_image = pygame.image.load("img/player2.png")
player_image_rect = player_image.get_rect()
player_image_rect.center = (width // 8, height // 2)

portal_frames = [pygame.image.load(f"img/portal{i}.png") for i in range(4)]

spider_frames = [pygame.image.load(f"img/spider{i}.png") for i in range(2)]
spider_y = height // 2
spider_speed = 1

yellow_ball_image = pygame.image.load("img/yellow_ball.png")
yellow_balls = []

dragon_image = pygame.image.load("img/dragon.png")
dragons = []

math_font = pygame.font.Font("fonts/medieval_font.ttf", 50)
level_font = pygame.font.Font("fonts/medieval_font.ttf", 40)
input_box_font = pygame.font.Font(None, 48)

input_box = pygame.Rect(width // 2 - 70, height // 2 + 60, 140, 48)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
a = random.randint(1, 10)
b = random.randint(1, 10)
answer = a + b
correct_answer = False

level = 1
game_over = False

def spawn_dragon():
    dragon_x = random.randint(0, width - dragon_image.get_width())
    dragons.append([dragon_x, 0])


def play_background_music():
    pygame.mixer.music.load("media/background_music.mp3")
    pygame.mixer.music.play(-1)

play_background_music()

def spawn_ball():
    ball_x = random.randint(0, width - yellow_ball_image.get_width())
    yellow_balls.append([ball_x, 0])

while True:
    screen.blit(background_images[level - 1], (0, 0))
    portal_frame = portal_frames[int(pygame.time.get_ticks() / 200) % len(portal_frames)]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if level == 3 and not correct_answer:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if text == str(answer):
                            correct_answer = True
                            text = "You may pass"
                        else:
                            text = "Try again"
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

    if not game_over:
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_image_rect.top > 0:
            player_image_rect.y -= distance
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_image_rect.bottom < height:
            player_image_rect.y += distance
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_image_rect.left > 0:
            player_image_rect.x -= distance
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_image_rect.right < width:
            player_image_rect.x += distance

        if level == 4: # Předpokládám, že chcete draky na úrovni 4
            if random.random() < 0.03:  # 3% šance na spawn draka každý frame
                spawn_dragon()

            for dragon in dragons:
                dragon[1] += 5  # Pohyb draka dolů, můžete upravit rychlost
                if dragon[1] > height:
                    dragons.remove(dragon)
                elif player_image_rect.colliderect(pygame.Rect(dragon[0], dragon[1], dragon_image.get_width(), dragon_image.get_height())):
                    game_over = True

        if level == 1:
            spider_frame = spider_frames[int(pygame.time.get_ticks() / 200) % len(spider_frames)]
            spider_rect = spider_frame.get_rect()
            spider_rect.center = (width - 150, spider_y)
            screen.blit(spider_frame, spider_rect.topleft)

            if spider_y <= 0 or spider_y >= height:
                spider_speed *= -1
            spider_y += spider_speed

            if player_image_rect.colliderect(spider_rect):
                game_over = True

        elif level == 2:
            if random.random() < 0.02:
                spawn_ball()

            for ball in yellow_balls:
                ball[1] += 5
                if ball[1] > height:
                    yellow_balls.remove(ball)
                elif player_image_rect.colliderect(pygame.Rect(ball[0], ball[1], yellow_ball_image.get_width(), yellow_ball_image.get_height())):
                    game_over = True
        
        elif level == 3:
            if not correct_answer:
                math_question = math_font.render(f"What is {a} + {b}?", True, (255, 0, 0))
                screen.blit(math_question, (width // 2 - math_question.get_width() // 2, height // 2 - math_question.get_height()))

                txt_surface = input_box_font.render(text, True, color)
                width_txt = max(200, txt_surface.get_width() + 10)
                input_box.w = width_txt
                screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
                pygame.draw.rect(screen, color, input_box, 2)

        if player_image_rect.colliderect(width - 100, height // 2 - 50, 100, 100):
            if level == 3 and not correct_answer:
                pass
            elif level < 10:
                level += 1
                correct_answer = False
                player_image_rect.topleft = (50, height // 2)
                yellow_balls = []
                a = random.randint(1, 10)
                b = random.randint(1, 10)
                answer = a + b
                text = ''


    for ball in yellow_balls:
        screen.blit(yellow_ball_image, ball)

    for dragon in dragons:
        screen.blit(dragon_image, dragon)

    screen.blit(player_image, player_image_rect)
    screen.blit(portal_frame, (width - 100, height // 2 - 50))

    level_text = level_font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(level_text, (10, 10))

    if game_over:
        game_over_text = math_font.render("Game Over, Press R For Restart", True, (255, 0, 0))
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            level = 1
            player_image_rect.center = (width // 8, height // 2)
            yellow_balls = []
            spider_y = height // 2
            game_over = False
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            answer = a + b
            text = ""
            correct_answer = False
            dragons = []  # Toto resetuje seznam draků



    pygame.display.flip()
    clock.tick(fps)

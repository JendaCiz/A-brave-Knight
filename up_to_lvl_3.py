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

custom_font = pygame.font.Font("fonts/medieval_font.ttf", 35)
level_font = pygame.font.Font("fonts/medieval_font.ttf", 40)

pygame.mixer.music.load("media/background_music.mp3")
pygame.mixer.music.play(-1)

level = 1
game_over = False
question_correct = False

def generate_question():
    global question, answer
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    question = f"{a} + {b} = ?"
    answer = str(a + b)

def spawn_ball():
    ball_x = random.randint(0, width - yellow_ball_image.get_width())
    yellow_balls.append([ball_x, 0])

# Initial math question for level 3
question = None
answer = None
input_text = ""
generate_question()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Handling input for math question
        if level == 3:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if input_text == answer:
                        question_correct = True
                        question = None
                        answer = None
                        input_text = ""
                    else:
                        game_over = True
                elif event.unicode.isdigit():
                    input_text += event.unicode

    screen.blit(background_images[level - 1], (0, 0))
    portal_frame = portal_frames[int(pygame.time.get_ticks() / 200) % len(portal_frames)]

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

        elif level == 3 and not question_correct:
            question_surface = custom_font.render(question, True, (255, 255, 255))
            input_surface = custom_font.render(input_text, True, (255, 255, 255))

            screen.blit(question_surface, (width // 2 - question_surface.get_width() // 2, height // 4))
            screen.blit(input_surface, (width // 2 - input_surface.get_width() // 2, height // 2))

        if player_image_rect.colliderect(width - 100, height // 2 - 50, 100, 100) and level < 10:
            if level == 3 and not question_correct:
                # Prevent player from moving to next level if the math question is not answered correctly
                pass
            else:
                level += 1
                player_image_rect.topleft = (50, height // 2)
                yellow_balls = []
                if level == 3:
                    question_correct = False
                    generate_question()

    for ball in yellow_balls:
        screen.blit(yellow_ball_image, ball)

    screen.blit(player_image, player_image_rect)
    screen.blit(portal_frame, (width - 100, height // 2 - 50))

    level_text = level_font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(level_text, (10, 10))

    if game_over:
        game_over_text = custom_font.render("Game Over, Press R For Restart", True, "Red")
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            level = 1
            player_image_rect.center = (width // 8, height // 2)
            yellow_balls = []
            spider_y = height // 2
            game_over = False
            question_correct = False
            generate_question()

    pygame.display.flip()
    clock.tick(fps)

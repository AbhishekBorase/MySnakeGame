import pygame
import random
import os

pygame.init()
pygame.mixer.init()

width = 900
height = 600

gameWindow = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Snake Game")
clock = pygame.time.Clock()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 250, 0)
blue = (0, 0, 255)
if not os.path.exists("hiscore.txt"):
    with open("hiscore.txt", 'w') as f:
        f.write("0")

with open("hiscore.txt", 'r+') as f:
    high_score = f.read()


def text_screen(text, color, x, y, size):
    font = pygame.font.SysFont(None, size)
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, (x, y))


def plot_snake(gameWindow, color, snk_list, snake_L):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, white, [x, y, snake_L, snake_L])


def welcome():
    wel_img = pygame.image.load("Image/well.jpg").convert()
    wel_img = pygame.transform.scale(wel_img, (width, height)).convert_alpha()
    gameWindow.fill(black)
    gameWindow.blit(wel_img, (0, 0))
    text_screen("Enter Space to Start", blue, 305, 500, 40)
    pygame.display.update()
    pygame.mixer.music.load("Sounds/Starting.mp3")
    pygame.mixer.music.play()
    exit_game = False
    while not exit_game:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                exit_game = True
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_SPACE:
                    gameloop()

def gameloop():
    global high_score
    exit_game = False
    game_over = False
    snake_L = 15
    snake_x = random.randint(0, width)
    snake_y = random.randint(0, height)
    food_x = random.randint(0, (width - 50))
    food_y = random.randint(0, (height - 50))
    food_size = 15
    vel_x = 0
    vel_y = 0
    vel = 5
    fps = 60
    score = 0
    snk_list = []
    snk_len = 1
    bgimg = pygame.image.load("Image/Background.jpg").convert()
    bgimg = pygame.transform.scale(bgimg, (width, height)).convert_alpha()
    endimg = pygame.image.load("Image/End.jpg").convert()
    endimg = pygame.transform.scale(endimg, (width, height)).convert_alpha()
    while not exit_game:
        if game_over:
            gameWindow.fill(black)
            gameWindow.blit(endimg, (0,0))
            text_screen("Game Over !!!", red, 255, 205, 100)
            text_screen("Press Enter to Continue", red, 260, 305, 55)
            your_score = int(score)
            if your_score > int(high_score):
                high_score = your_score
                with open("hiscore.txt", 'w+') as f:
                    f.write(str(high_score))
            text_screen("Your Score :" + str(your_score), red, 240, 350, 40)
            text_screen("High Score :" + str(high_score), red, 520, 350, 40)
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    exit_game = True
                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_RETURN:
                        gameloop()
        else:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    exit_game = True
                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_RIGHT:
                        vel_x = vel
                        vel_y = 0
                    if events.key == pygame.K_UP:
                        vel_y = -vel
                        vel_x = 0
                    if events.key == pygame.K_LEFT:
                        vel_x = -vel
                        vel_y = 0
                    if events.key == pygame.K_DOWN:
                        vel_y = vel
                        vel_x = 0
            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                pygame.mixer.music.load("Sounds/eat.mp3")
                pygame.mixer.music.play()
                score += 10
                food_x = random.randint(0, (width - 50))
                food_y = random.randint(0, (height - 50))
                snk_len += 5
            if snake_x > width:
                snake_x = 0
            if snake_x < 0:
                snake_x = width
            if snake_y > height:
                snake_y = 0
            if snake_y < 0:
                snake_y = height

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_len:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load("Sounds/out.mp3")
                pygame.mixer.music.play()

            snake_x += vel_x
            snake_y += vel_y
            gameWindow.fill(black)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score :" + str(score), red, 5, 5, 55)
            pygame.draw.rect(gameWindow, green, [food_x, food_y, food_size, food_size])
            plot_snake(gameWindow, white, snk_list, snake_L)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()


welcome()

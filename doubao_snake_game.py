import pygame
import random

# 初始化 Pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# 定义游戏窗口大小
dis_width = 800
dis_height = 600

# 创建游戏窗口
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('贪吃蛇游戏')

# 定义时钟对象
clock = pygame.time.Clock()

# 定义蛇的初始大小
snake_block = 10
snake_speed = 15

# 定义字体样式
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def Your_score(score):
    value = score_font.render("得分: " + str(score), True, YELLOW)
    dis.blit(value, [0, 0])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, GREEN, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


# 难度设置
difficulty_levels = {
    "简单": {"speed": 10, "score_coefficient": 1},
    "普通": {"speed": 15, "score_coefficient": 2},
    "困难": {"speed": 20, "score_coefficient": 3}
}


def show_start_menu():
    while True:
        dis.fill(BLUE)
        message("选择难度: 简单/普通/困难", WHITE)
        message("使用方向键控制蛇移动", WHITE)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "简单"
                elif event.key == pygame.K_2:
                    return "普通"
                elif event.key == pygame.K_3:
                    return "困难"


def show_pause_menu():
    pause_surface = pygame.Surface((dis_width, dis_height), pygame.SRCALPHA)
    pause_surface.fill((0, 0, 0, 128))
    dis.blit(pause_surface, (0, 0))
    message("游戏暂停，按任意键继续", WHITE)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                return


def show_end_menu(score):
    while True:
        dis.fill(BLUE)
        message("游戏结束! 最终得分: " + str(score), RED)
        message("按 R 重启，按 Q 退出", WHITE)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()


def gameLoop():
    difficulty = show_start_menu()
    snake_speed = difficulty_levels[difficulty]["speed"]
    score_coefficient = difficulty_levels[difficulty]["score_coefficient"]

    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            if show_end_menu(Length_of_snake - 1 * score_coefficient):
                gameLoop()
            else:
                game_over = True
                game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    show_pause_menu()

        # 判断是否撞墙
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(BLUE)
        pygame.draw.rect(dis, RED, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 判断是否撞到自己
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score((Length_of_snake - 1) * score_coefficient)
        value = score_font.render("难度: " + difficulty, True, YELLOW)
        dis.blit(value, [0, 30])

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
    
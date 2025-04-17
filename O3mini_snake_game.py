import pygame
import sys
import random

# 初始化 Pygame
pygame.init()

# 游戏窗口配置
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20  # 网格单元尺寸（蛇与食物均以此为步长）
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("贪吃蛇游戏")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TRANSPARENT_BLACK = (0, 0, 0, 150)

# 定义游戏状态
MENU = 'menu'
PLAYING = 'playing'
PAUSE = 'pause'
GAME_OVER = 'game_over'

# 定义难度参数（速度/基础得分）
difficulty_config = {
    'Easy': {
        'speed': 8,       # 每秒帧数
        'score': 10,
    },
    'Normal': {
        'speed': 12,
        'score': 20,
    },
    'Hard': {
        'speed': 16,
        'score': 30,
    }
}

# 设置默认难度
current_difficulty = 'Easy'
snake_speed = difficulty_config[current_difficulty]['speed']
food_score = difficulty_config[current_difficulty]['score']

# 定义字体
font_small = pygame.font.SysFont("arial", 20)
font_medium = pygame.font.SysFont("arial", 28)
font_large = pygame.font.SysFont("arial", 48)

clock = pygame.time.Clock()

# 辅助函数 --- 绘制文本
def draw_text(text, font, color, surface, x, y, center=False):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# 定义随机生成食物的位置函数
def random_food_position(snake):
    # 根据网格计算，确保食物位置不在蛇身上
    cols = SCREEN_WIDTH // CELL_SIZE
    rows = SCREEN_HEIGHT // CELL_SIZE
    while True:
        x = random.randint(0, cols - 1) * CELL_SIZE
        y = random.randint(0, rows - 1) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)

# 重置游戏数据
def reset_game():
    start_x = SCREEN_WIDTH // 2
    start_y = SCREEN_HEIGHT // 2
    snake = [(start_x, start_y)]
    # 默认向右移动
    direction = (CELL_SIZE, 0)
    food = random_food_position(snake)
    score = 0
    return snake, direction, food, score

# 绘制网格（可选）
def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (SCREEN_WIDTH, y))

# 绘制当前游戏状态信息（得分、难度）
def draw_info(surface, score, difficulty):
    info = f"Score: {score}   Difficulty: {difficulty}"
    draw_text(info, font_small, WHITE, surface, 10, 10)

# 绘制蛇和食物
def draw_game(surface, snake, food):
    # 绘制蛇身
    for segment in snake:
        pygame.draw.rect(surface, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    # 绘制食物
    pygame.draw.rect(surface, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

# 主菜单界面
def menu_screen():
    global current_difficulty, snake_speed, food_score
    while True:
        screen.fill(BLACK)
        draw_text("贪吃蛇游戏", font_large, GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, center=True)
        draw_text("选择难度：", font_medium, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30, center=True)
        draw_text("1 - Easy   2 - Normal   3 - Hard", font_medium, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10, center=True)
        draw_text("按 Q 键退出", font_small, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4, center=True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_1:
                    current_difficulty = 'Easy'
                elif event.key == pygame.K_2:
                    current_difficulty = 'Normal'
                elif event.key == pygame.K_3:
                    current_difficulty = 'Hard'
                else:
                    continue

                # 根据选择更新难度参数
                snake_speed = difficulty_config[current_difficulty]['speed']
                food_score = difficulty_config[current_difficulty]['score']
                return  # 开始游戏

# 游戏暂停界面（半透明覆盖）
def pause_screen(surface):
    pause_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    pause_overlay.fill(TRANSPARENT_BLACK)
    surface.blit(pause_overlay, (0, 0))
    draw_text("游戏已暂停", font_large, WHITE, surface, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30, center=True)
    draw_text("按 P 键继续", font_medium, WHITE, surface, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, center=True)
    pygame.display.flip()

# 游戏结束界面
def game_over_screen(surface, score):
    while True:
        screen.fill(BLACK)
        draw_text("游戏结束", font_large, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, center=True)
        draw_text(f"最终得分: {score}", font_medium, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, center=True)
        draw_text("重新开始: R    退出: Q", font_medium, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, center=True)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    return

# 主游戏循环
def main_game():
    global snake_speed

    snake, direction, food, score = reset_game()
    # 设置一个初始事件定时器，用于定时更新蛇的位置
    MOVE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVE_EVENT, int(1000 / snake_speed))

    current_state = PLAYING
    while True:
        # 根据当前游戏状态执行不同逻辑
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 游戏状态为正在进行时处理按键事件
            elif event.type == pygame.KEYDOWN and current_state == PLAYING:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)
                elif event.key == pygame.K_p:
                    current_state = PAUSE
                    pause_screen(screen)
            elif event.type == pygame.KEYDOWN and current_state == PAUSE:
                if event.key == pygame.K_p:
                    current_state = PLAYING
            elif event.type == MOVE_EVENT and current_state == PLAYING:
                # 根据方向更新蛇头位置
                head_x, head_y = snake[0]
                new_head = (head_x + direction[0], head_y + direction[1])
                
                # 边界检测
                if (new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or 
                    new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT):
                    current_state = GAME_OVER
                    break

                # 自己身体碰撞检测
                if new_head in snake:
                    current_state = GAME_OVER
                    break

                snake.insert(0, new_head)

                # 检测是否吃到食物
                if new_head == food:
                    score += food_score
                    food = random_food_position(snake)
                else:
                    snake.pop()  # 移除蛇尾

        if current_state == GAME_OVER:
            game_over_screen(screen, score)
            # 重置参数重新开始
            snake, direction, food, score = reset_game()
            current_state = PLAYING
            pygame.time.set_timer(MOVE_EVENT, int(1000 / snake_speed))

        # 绘制每一帧游戏画面
        screen.fill(BLACK)
        # 如果需要显示网格，可以取消下面一行的注释
        # draw_grid(screen)
        draw_game(screen, snake, food)
        draw_info(screen, score, current_difficulty)
        if current_state == PAUSE:
            pause_screen(screen)
        pygame.display.flip()
        clock.tick(60)  # 控制整体帧率

if __name__ == "__main__":
    while True:
        menu_screen()
        main_game()
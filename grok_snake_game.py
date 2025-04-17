import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 颜色定义
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

# 游戏窗口设置
BLOCK_SIZE = 20
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_WIDTH = WINDOW_WIDTH // BLOCK_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // BLOCK_SIZE
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("贪吃蛇")

# 难度配置
DIFFICULTY_CONFIG = {
    "easy": {"speed": 10, "score_multiplier": 1},
    "normal": {"speed": 15, "score_multiplier": 2},
    "hard": {"speed": 25, "score_multiplier": 3}
}

# 字体
font = pygame.font.SysFont("simhei", 36)  # 使用支持中文的字体

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.length = 1

    def move(self):
        head_x, head_y = self.positions[0]
        if self.direction == "UP":
            head_y -= 1
        elif self.direction == "DOWN":
            head_y += 1
        elif self.direction == "LEFT":
            head_x -= 1
        elif self.direction == "RIGHT":
            head_x += 1
        self.positions.insert(0, (head_x, head_y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def grow(self):
        self.length += 1

    def check_collision(self):
        head = self.positions[0]
        # 边界碰撞
        if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True
        # 自碰检测
        if head in self.positions[1:]:
            return True
        return False

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self, snake_positions=None):
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if snake_positions is None or self.position not in snake_positions:
                break

def draw_text(text, pos, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

def main_menu():
    selected_difficulty = "normal"
    while True:
        screen.fill(BLACK)
        draw_text("贪吃蛇", (WINDOW_WIDTH // 2 - 50, 100))
        draw_text("选择难度：", (WINDOW_WIDTH // 2 - 100, 200))
        draw_text("1. 简单", (WINDOW_WIDTH // 2 - 100, 250), GREEN if selected_difficulty == "easy" else WHITE)
        draw_text("2. 普通", (WINDOW_WIDTH // 2 - 100, 300), GREEN if selected_difficulty == "normal" else WHITE)
        draw_text("3. 困难", (WINDOW_WIDTH // 2 - 100, 350), GREEN if selected_difficulty == "hard" else WHITE)
        draw_text("按 Enter 开始", (WINDOW_WIDTH // 2 - 100, 450))
        draw_text("方向键控制，P 暂停", (WINDOW_WIDTH // 2 - 100, 500))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_difficulty = "easy"
                elif event.key == pygame.K_2:
                    selected_difficulty = "normal"
                elif event.key == pygame.K_3:
                    selected_difficulty = "hard"
                elif event.key == pygame.K_RETURN:
                    return selected_difficulty

        pygame.display.flip()

def pause_menu():
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # 半透明黑色遮罩
    screen.blit(overlay, (0, 0))
    draw_text("暂停", (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 - 50))
    draw_text("按 P 继续", (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 10))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                return

def game_over(score):
    while True:
        screen.fill(BLACK)
        draw_text(f"游戏结束！得分: {score}", (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 50))
        draw_text("按 R 重启，按 Q 退出", (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    clock = pygame.time.Clock()
    while True:
        difficulty = main_menu()
        snake = Snake()
        food = Food()
        score = 0
        game_speed = DIFFICULTY_CONFIG[difficulty]["speed"]
        score_multiplier = DIFFICULTY_CONFIG[difficulty]["score_multiplier"]
        paused = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake.direction != "DOWN":
                        snake.direction = "UP"
                    elif event.key == pygame.K_DOWN and snake.direction != "UP":
                        snake.direction = "DOWN"
                    elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                        snake.direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                        snake.direction = "RIGHT"
                    elif event.key == pygame.K_p:
                        paused = not paused
                        if paused:
                            pause_menu()

            if not paused:
                snake.move()
                if snake.positions[0] == food.position:
                    snake.grow()
                    score += 10 * score_multiplier
                    food.randomize_position(snake.positions)
                if snake.check_collision():
                    if game_over(score):
                        break

                screen.fill(BLACK)
                for pos in snake.positions:
                    pygame.draw.rect(screen, GREEN, (pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, RED, (food.position[0] * BLOCK_SIZE, food.position[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                draw_text(f"得分: {score}  难度: {difficulty}", (10, 10))
                pygame.display.flip()
                clock.tick(game_speed)

if __name__ == "__main__":
    main()
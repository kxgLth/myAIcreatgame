import pygame
import random
import sys

# 初始化Pygame
pygame.init()
pygame.font.init()

# 游戏窗口设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("贪吃蛇 - 难度增强版")

# 颜色定义
COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "gold": (255, 215, 0)
}

# 字体设置
font_large = pygame.font.SysFont("simhei", 72)
font_medium = pygame.font.SysFont("simhei", 36)
font_small = pygame.font.SysFont("simhei", 24)

class Game:
    def __init__(self):
        self.game_state = "start_menu"
        self.difficulty = "normal"
        self.reset_game()

    def reset_game(self):
        difficulties = {
            "easy": {"speed": 8, "food_score": 1},
            "normal": {"speed": 12, "food_score": 2},
            "hard": {"speed": 20, "food_score": 3}
        }
        cfg = difficulties[self.difficulty]
        self.snake = [[SCREEN_WIDTH//2, SCREEN_HEIGHT//2]]
        self.direction = "RIGHT"
        self.score = 0
        self.snake_speed = cfg["speed"]
        self.food_score = cfg["food_score"]
        self.food = self.generate_food()
        self.clock = pygame.time.Clock()

    def generate_food(self):
        return [
            random.randint(0, SCREEN_WIDTH - 20),
            random.randint(0, SCREEN_HEIGHT - 20)
        ]

    def draw_text(self, text, font, color, position):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, position)

    def draw_start_menu(self):
        screen.fill(COLORS["black"])
        self.draw_text("贪吃蛇", font_large, COLORS["gold"], (330, 150))
        self.draw_text("选择难度:", font_medium, COLORS["white"], (320, 300))
        self.draw_text("1. 简单", font_small, COLORS["green"], (350, 350))
        self.draw_text("2. 普通", font_small, COLORS["gold"], (350, 400))
        self.draw_text("3. 困难", font_small, COLORS["red"], (350, 450))
        self.draw_text("按空格键开始", font_medium, COLORS["white"], (300, 550))

    def draw_pause_menu(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        self.draw_text("游戏暂停", font_large, COLORS["gold"], (300, 250))
        self.draw_text("按ESC继续游戏", font_medium, COLORS["white"], (310, 350))

    def draw_game_over(self):
        screen.fill(COLORS["black"])
        self.draw_text("游戏结束!", font_large, COLORS["red"], (300, 200))
        self.draw_text(f"得分: {self.score}", font_medium, COLORS["white"], (350, 300))
        self.draw_text("按R重新开始  按Q退出", font_medium, COLORS["white"], (250, 400))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.game_state == "start_menu":
                if event.key == pygame.K_SPACE:
                    self.game_state = "running"
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    self.difficulty = ["easy", "normal", "hard"][event.key - pygame.K_1]
                    self.reset_game()

            elif self.game_state == "running":
                if event.key == pygame.K_ESCAPE:
                    self.game_state = "paused"
                else:
                    if event.key == pygame.K_LEFT and self.direction != "RIGHT":
                        self.direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                        self.direction = "RIGHT"
                    elif event.key == pygame.K_UP and self.direction != "DOWN":
                        self.direction = "UP"
                    elif event.key == pygame.K_DOWN and self.direction != "UP":
                        self.direction = "DOWN"

            elif self.game_state == "paused" and event.key == pygame.K_ESCAPE:
                self.game_state = "running"

            elif self.game_state == "game_over":
                if event.key == pygame.K_r:
                    self.reset_game()
                    self.game_state = "running"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

    def update_game(self):
        head = [self.snake[0][0], self.snake[0][1]]
        if self.direction == "RIGHT":
            head[0] += 20
        elif self.direction == "LEFT":
            head[0] -= 20
        elif self.direction == "UP":
            head[1] -= 20
        elif self.direction == "DOWN":
            head[1] += 20

        if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            self.game_state = "game_over"
            return

        if head in self.snake[1:]:
            self.game_state = "game_over"
            return

        if (head[0] < self.food[0]+20 and head[0]+20 > self.food[0] and
            head[1] < self.food[1]+20 and head[1]+20 > self.food[1]):
            self.score += self.food_score
            self.food = self.generate_food()
        else:
            self.snake.pop()

        self.snake.insert(0, head)

    def draw_game(self):
        screen.fill(COLORS["black"])
        pygame.draw.rect(screen, COLORS["red"], (*self.food, 20, 20))
        for seg in self.snake:
            pygame.draw.rect(screen, COLORS["green"], (*seg, 20, 20))
        self.draw_text(f"得分: {self.score}", font_small, COLORS["white"], (10, 10))
        self.draw_text(f"难度: {self.difficulty}", font_small, COLORS["white"], (10, 40))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_input(event)

            if self.game_state == "running":
                self.update_game()

            if self.game_state == "start_menu":
                self.draw_start_menu()
            elif self.game_state == "running":
                self.draw_game()
            elif self.game_state == "paused":
                self.draw_game()
                self.draw_pause_menu()
            elif self.game_state == "game_over":
                self.draw_game_over()

            pygame.display.update()
            self.clock.tick(self.snake_speed)

if __name__ == "__main__":
    game = Game()
    game.run()
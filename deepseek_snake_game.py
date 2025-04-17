import pygame
import random
import sys

# 初始化配置
pygame.init()
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
FPS = 60
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'gray': (128, 128, 128),
    'transparent': (0, 0, 0, 100)
}

# 难度配置字典
DIFFICULTIES = {
    'easy': {'speed': 5, 'score_multiplier': 1},
    'normal': {'speed': 10, 'score_multiplier': 2},
    'hard': {'speed': 15, 'score_multiplier': 3}
}

# 游戏状态常量
MENU = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("贪吃蛇大作战")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # 游戏状态
        self.game_state = MENU
        self.current_diff = 'normal'
        self.score = 0
        self.snake = []
        self.direction = (0, 0)
        self.food = None
        self.last_move_time = 0
        
        self.init_game()
    
    def init_game(self):
        # 初始化蛇的位置
        start_x = WIDTH//2 // CELL_SIZE * CELL_SIZE
        start_y = HEIGHT//2 // CELL_SIZE * CELL_SIZE
        self.snake = [
            (start_x, start_y),
            (start_x - CELL_SIZE, start_y),
            (start_x - CELL_SIZE*2, start_y)
        ]
        self.direction = (CELL_SIZE, 0)  # 初始向右移动
        self.score = 0
        self.generate_food()
    
    def generate_food(self):
        while True:
            x = random.randrange(0, WIDTH-CELL_SIZE, CELL_SIZE)
            y = random.randrange(0, HEIGHT-CELL_SIZE, CELL_SIZE)
            self.food = (x, y)
            # 确保食物不在蛇身上
            if self.food not in self.snake:
                break
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.game_state == MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.current_diff = list(DIFFICULTIES.keys())[
                            (list(DIFFICULTIES.keys()).index(self.current_diff)-1) % 3
                        ]
                    elif event.key == pygame.K_DOWN:
                        self.current_diff = list(DIFFICULTIES.keys())[
                            (list(DIFFICULTIES.keys()).index(self.current_diff)+1) % 3
                        ]
                    elif event.key == pygame.K_RETURN:
                        self.game_state = PLAYING
            
            elif self.game_state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != (0, CELL_SIZE):
                        self.direction = (0, -CELL_SIZE)
                    elif event.key == pygame.K_DOWN and self.direction != (0, -CELL_SIZE):
                        self.direction = (0, CELL_SIZE)
                    elif event.key == pygame.K_LEFT and self.direction != (CELL_SIZE, 0):
                        self.direction = (-CELL_SIZE, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (-CELL_SIZE, 0):
                        self.direction = (CELL_SIZE, 0)
                    elif event.key == pygame.K_p:
                        self.game_state = PAUSED
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = MENU
            
            elif self.game_state == PAUSED:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.game_state = PLAYING
            
            elif self.game_state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.init_game()
                        self.game_state = PLAYING
                    elif event.key == pygame.K_q:
                        self.game_state = MENU
    
    def move_snake(self):
        now = pygame.time.get_ticks()
        if now - self.last_move_time > 1000 // DIFFICULTIES[self.current_diff]['speed']:
            self.last_move_time = now
            
            # 计算新头部位置
            new_head = (
                (self.snake[0][0] + self.direction[0]) % WIDTH,
                (self.snake[0][1] + self.direction[1]) % HEIGHT
            )
            
            # 碰撞检测
            if new_head in self.snake:
                self.game_state = GAME_OVER
                return
            
            self.snake.insert(0, new_head)
            
            # 吃食物检测
            if new_head == self.food:
                self.score += 10 * DIFFICULTIES[self.current_diff]['score_multiplier']
                self.generate_food()
            else:
                self.snake.pop()
    
    def draw_interface(self):
        self.screen.fill(COLORS['black'])
        
        if self.game_state == MENU:
            # 绘制菜单界面
            title = self.font.render("贪吃蛇大作战", True, COLORS['green'])
            diff_text = self.font.render(
                f"当前难度: {self.current_diff.capitalize()}",
                True, COLORS['white']
            )
            help_text = [
                "使用 ↑↓ 选择难度",
                "按 Enter 开始游戏",
                "按 ESC 返回菜单",
                "游戏时按 P 暂停"
            ]
            
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
            self.screen.blit(diff_text, (WIDTH//2 - diff_text.get_width()//2, 200))
            
            for i, text in enumerate(help_text):
                surf = self.font.render(text, True, COLORS['white'])
                self.screen.blit(surf, (WIDTH//2 - surf.get_width()//2, 300 + i*40))
        
        elif self.game_state in [PLAYING, PAUSED]:
            # 绘制游戏界面
            # 绘制蛇身
            for segment in self.snake:
                pygame.draw.rect(self.screen, COLORS['green'],
                               (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
            
            # 绘制食物
            pygame.draw.rect(self.screen, COLORS['red'],
                            (self.food[0], self.food[1], CELL_SIZE, CELL_SIZE))
            
            # 绘制游戏数据
            score_text = self.font.render(
                f"Score: {self.score} | Difficulty: {self.current_diff}",
                True, COLORS['white']
            )
            self.screen.blit(score_text, (10, 10))
            
            if self.game_state == PAUSED:
                # 绘制暂停遮罩
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill(COLORS['transparent'])
                self.screen.blit(overlay, (0, 0))
                
                pause_text = self.font.render("游戏暂停 - 按 P 继续", True, COLORS['white'])
                self.screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2))
        
        elif self.game_state == GAME_OVER:
            # 绘制结束界面
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(COLORS['transparent'])
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("游戏结束！", True, COLORS['red'])
            score_text = self.font.render(
                f"最终得分: {self.score}", True, COLORS['white'])
            restart_text = self.font.render("按 R 重新开始", True, COLORS['white'])
            quit_text = self.font.render("按 Q 返回菜单", True, COLORS['white'])
            
            texts = [game_over_text, score_text, restart_text, quit_text]
            for i, text in enumerate(texts):
                self.screen.blit(text, (WIDTH//2 - text.get_width()//2, 200 + i*50))
    
    def run(self):
        while True:
            self.handle_input()
            
            if self.game_state == PLAYING:
                self.move_snake()
            
            self.draw_interface()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
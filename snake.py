import pygame, sys, random, time
from pygame.math import Vector2

class Fruit:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(sized_apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x,self.y)

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen,("Black"),block_rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.fruits_eaten = 0
        self.timer_interval = 150 
        self.level = 1

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_level()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.fruits_eaten += 1  
            if self.fruits_eaten % 4 == 0 and self.timer_interval >=45:  
                self.decrease_timer_interval()
                self.level+=1 

    def decrease_timer_interval(self):
        self.timer_interval -= 15
        pygame.time.set_timer(SCREEN_UPDATE, self.timer_interval)
    
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    def game_over(self):
        time.sleep(1.2)
        pygame.quit()
        sys.exit()
    
    def draw_grass(self):
        grass_color = (167,209,61)
        for row in range(cell_number):
            if row%2 == 0:
                for column in range(cell_number):
                    if column%2 == 0:
                        grass_rect = pygame.Rect(column*cell_size,row*cell_size , cell_size,cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for column in range(cell_number):
                    if column%2 == 1:
                        grass_rect = pygame.Rect(column*cell_size,row*cell_size , cell_size,cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True , (56,74,12))
        score_x = int(cell_size*cell_number-60)
        score_y = int(cell_size*cell_number-40)
        score_rect = score_surface.get_rect(center=(score_x,score_y))
        apple_rect = sized_apple.get_rect(midright = (score_rect.left, score_rect.centery))
        screen.blit(score_surface,score_rect)
        screen.blit(sized_apple, apple_rect)

    def draw_level(self):
        level_text = 'Level: ' + str(self.level)
        level_surface = game_font.render(level_text, True , (56,74,12))
        level_x = int(cell_size*cell_number-60)
        level_y = int(cell_size*cell_number-640)
        level_rect = level_surface.get_rect(center=(level_x,level_y))
        screen.blit(level_surface,level_rect)

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size))
fps = pygame.time.Clock()
apple = pygame.image.load(r"C:\Users\user\Desktop\Lab-8\pngwing.com (2).png").convert_alpha()
sized_apple = pygame.transform.scale(apple, (40, 40))
game_font = pygame.font.Font(None, 40)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)
main_game = Main()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and  main_game.snake.direction.y != 1:
                main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1,0)

    screen.fill((175,215,70))
    main_game.draw_elements()
    pygame.display.update()
    fps.tick(120)
import pygame
import numpy as np
import time

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('SNAKE GAME')
font = pygame.font.SysFont(None, 36)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
done = False

def draw_border():
    pygame.draw.rect(screen, white, (0, 30, 600, 570), 2)

snake = []

class coordinate:
    x: int
    y: int

    def right(self):
        self.x += 15

    def left(self):
        self.x -= 15

    def down(self):
        self.y += 15

    def up(self):
        self.y -= 15

    def __init__(self, x, y):
        self.x = x * 15
        self.y = y * 15 + 30  # Offset for score row

def randomize():
    while True:
        x = np.random.randint(0, 40)
        y = np.random.randint(0, 38)  # 38 rows below score row
        food = coordinate(x, y)
        if food not in snake:
            pygame.draw.rect(screen, green, (food.x, food.y, 15, 15))
            return food

def showScreen(snake, mainFood, score):
    screen.fill((0, 0, 0))
    # Draw score row
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, 600, 30))
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 2))
    draw_border()
    for i in snake:
        pygame.draw.rect(screen, blue, (i.x, i.y, 15, 15))
    pygame.draw.rect(screen, green, (mainFood.x, mainFood.y, 15, 15))

def is_out_of_bounds(coord):
    return not (0 <= coord.x < 600 and 30 <= coord.y < 600)

lastMoveMade = 'e'
snake.append(coordinate(25, 30 - 2))
snake.append(coordinate(24, 30 - 2))
snake.append(coordinate(23, 30 - 2))
snake.append(coordinate(22, 30 - 2))
mainFood = randomize()
score = 0
speed = 0.10 

game_over = False

while not done:
    showScreen(snake, mainFood, score)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        key = pygame.key.get_pressed()
        headx, heady = snake[0].x, snake[0].y
        headx, heady = headx // 15, (heady - 30) // 15
        headAfterTheChance = coordinate(headx, heady)
        if event.type == pygame.KEYDOWN:
            if key[pygame.K_LEFT]:
                headAfterTheChance.left()
                lastMoveMade = 'w'
            elif key[pygame.K_RIGHT]:
                headAfterTheChance.right()
                lastMoveMade = 'e'
            elif key[pygame.K_UP]:
                headAfterTheChance.up()
                lastMoveMade = 'n'
            elif key[pygame.K_DOWN]:
                headAfterTheChance.down()
                lastMoveMade = 's'
    headx, heady = snake[0].x, snake[0].y
    headx, heady = headx // 15, (heady - 30) // 15
    headAfterTheChance = coordinate(headx, heady)
    if lastMoveMade == 'w':
        headAfterTheChance.left()
    elif lastMoveMade == 'e':
        headAfterTheChance.right()
    elif lastMoveMade == 'n':
        headAfterTheChance.up()
    elif lastMoveMade == 's':
        headAfterTheChance.down()
    if is_out_of_bounds(headAfterTheChance):
        game_over = True
        break
    if any(seg.x == headAfterTheChance.x and seg.y == headAfterTheChance.y for seg in snake):
        game_over = True
        break
    snake.insert(0, headAfterTheChance)
    if mainFood.x == headAfterTheChance.x and mainFood.y == headAfterTheChance.y:
        score += 1
        if score % 5 == 0:
            speed = max(0.03, speed - 0.02)
        mainFood = randomize()
    else:
        snake = snake[:-1]
    pygame.display.update()
    time.sleep(speed)

# Game Over screen
while True:
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, 600, 30))
    draw_border()
    over_text = font.render('Game Over!', True, red)
    score_text = font.render(f'Final Score: {score}', True, white)
    exit_text = font.render('Press Enter to exit', True, white)
    screen.blit(over_text, (200, 200))
    screen.blit(score_text, (200, 250))
    screen.blit(exit_text, (160, 320))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pygame.quit()
                exit()
# 1.贪吃蛇游戏环境搭建
import pygame
import sys
from random import randint
from pygame.draw import rect as draw_r
from pygame.locals import *
# 定义全局常量
cell_size = 20
rows = 20
cols = 20  # 整个游戏界面的场地行数和列数均为20个格子
area = rows * cols
total_cols = cell_size * cols
total_rows = cell_size * rows  # 整个游戏场地的行、列的像素数，用于后续的区域图形绘制
# 用一维数组来表示二维的场地
board = [0] * area
snake = [((rows // 2) * cols + (cols // 2)) + i for i in range(2)] + [0] * (area - 2)
snake_size = 3
# 创建用于表示场地中每一个格子状态的常量(差值尽量大)
stat_food = 0
stat_empty = (rows + 1) * (cols + 1)
stat_snake = 2 * stat_empty
moves = {'left': -1, 'right': 1, 'up': -cols, 'down': cols}  # 将所有的运动方向存储在一个字典中，便于后续调用与表示
score = 0
pygame.init()  # 初始化pygame
play_surface = pygame.display.set_mode((total_cols, total_rows))  # 创建pygame显示层
pygame.display.set_caption('AI贪吃蛇游戏')
play_surface.fill('black')  # 绘制pygame显示层
draw_r(play_surface, 'yellow', [0, 0, total_cols, total_rows], cell_size)  # 初始化围墙
eaten = True
cur_direction = 'left'
while True:
    pygame.time.Clock().tick(5)  # 游戏速度控制(可调整)
    draw_r(play_surface, 'yellow', [0, 0, cell_size, cell_size])
    if eaten and snake_size < (cols - 2) * (rows - 2):
        while True:
            c = randint(1, cols - 2)
            r = randint(1, rows - 2)
            if cols * c + r not in snake[:snake_size]:
                food_position = cols * c + r
                eaten = False
                break
        draw_r(play_surface, 'red', [cell_size * r, cell_size * c, cell_size, cell_size])
    board = [stat_empty for _ in range(area)]  # 重置board
    board[food_position] = stat_food
    for i in snake[:snake_size]:board[i] = stat_snake
    for event in pygame.event.get():
        if snake_size == (cols - 2) * (rows - 2) or event.type == QUIT or (event.type == KEYDOW and event.key == K_ESCAPE):
            print(score)
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT and (cur_direction == 'up' or cur_direction == 'down'):cur_direction='right'
            elif event.key == K_LEFT and (cur_direction == 'up' or cur_direction == 'down'):cur_direction='left'
            elif event.key == K_UP and (cur_direction == 'left' or cur_direction == 'right'):cur_direction='up'
            elif event.key == K_DOWN and (cur_direction == 'left' or cur_direction == 'right'):cur_direction='down'
    pygame.display.flip()  # 每次循环都需要刷新pygame显示层
    for index in range(snake_size, 0, -1):snake[index] = snake[index - 1]
    snake[0] += moves[cur_direction]
    for body in snake[:snake_size]:
        draw_r(play_surface, 'white', [cell_size * (body % cols), cell_size * (body // cols), cell_size, cell_size])
    pygame.display.flip()
    if snake[0] == food_position:
        board[snake[0]] = stat_snake
        snake_size += 1
        score += 1
        eaten = True
    elif board[snake[0]] == stat_snake or not (0 < (snake[0] + moves[cur_direction]) % cols < cols - 1 and 0 < (snake[0] + moves[cur_direction]) // cols < rows - 1):
        draw_r(play_surface, 'black', [cell_size * (snake[snake_size] % cols), cell_size * (snake[snake_size] // cols), cell_size, cell_size])
        print(score)
        pygame.quit()
        sys.exit()
    else:
        board[snake[0]] = stat_snake
        board[snake[snake_size]] = stat_empty
        draw_r(play_surface, 'black', [cell_size * (snake[snake_size] % cols), cell_size * (snake[snake_size] // cols), cell_size, cell_size])
        pygame.display.flip()

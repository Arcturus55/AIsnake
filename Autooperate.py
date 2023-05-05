# 2.贪吃蛇游戏实现自动运行
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
# 与上面数组对应的临时数组，用于表示蛇试探性移动的过程
temp_board = [0] * area
temp_snake = snake[:]
temp_snake_size = 3
# 创建用于表示场地中每一个格子状态的常量(差值尽量大)
stat_food = 0
stat_empty = (rows + 1) * (cols + 1)
stat_snake = 2 * stat_empty
moves = {'left': -1, 'right': 1, 'up': -cols, 'down': cols}  # 将所有的运动方向存储在一个字典中，便于后续调用与表示
score = 0
error = -666  # 错误初始化代码
best_move = error
def bfs(food_position_0, snake_0, board_0):
    '''广度优先搜索遍历整个board 计算出board中相应格子到达食物的路径长度并且查看蛇头与食物之间是否有通路'''
    queue = [food_position_0, ]
    mark = [0 for _ in range(area)]
    exist_path = False
    while queue:
        i = queue.pop(0)  # 初始时idx是食物的坐标
        if mark[i] == 1:continue
        mark[i] = 1# 防止重复赋值
        for mov in moves.values():  # 左右上下
            if 0 < (i + mov) % cols < cols - 1 and 0 < (i + mov) // cols < rows - 1:
                if i + mov == snake_0[0]:  # 如果运动以后的坐标时蛇头的坐标
                    exist_path = True  # 蛇头与食物之间有通路
                if board_0[i + mov] < stat_snake:  # 如果该点不是蛇的身体
                    if board_0[i + mov] > board_0[i] + 1:board_0[i + mov] = board_0[i] + 1  # 取最短的路径
                    if mark[i + mov] == 0:queue.append(i + mov)
    return exist_path
def find_certain_path(snake_0, board_0, initiate_val, cmp):
    '''按照一定的规则选择一步来运行'''
    final_path = error
    val = initiate_val
    for mov in moves.values():
        if 0 < (snake_0[0] + mov) % cols < cols - 1 and 0 < (snake_0[0] + mov) // cols < rows - 1 and\
            stat_empty > board_0[snake_0[0] + mov] and cmp(board_0[snake_0[0] + mov], val):
            val = board_0[snake_0[0] + mov]
            final_path = mov
    return final_path
def follow_tail():
    '''在虚拟的temp_board和temp_snake中让蛇头朝着蛇尾运行一步'''
    global temp_board, temp_snake, food_position, temp_snake_size
    temp_snake_size = snake_size
    temp_snake = snake[:]
    temp_board = [stat_empty for _ in range(area)]  # 重置temp_board
    for i in temp_snake[:temp_snake_size - 1]:temp_board[i] = stat_snake
    temp_board[temp_snake[temp_snake_size - 1]] = stat_food  # 虚拟地将蛇尾变为食物
    temp_board[food_position] = stat_snake  # 放置食物的地方，看成蛇身,目的是避免场地上同时存在两个食物
    bfs(temp_snake[temp_snake_size - 1], temp_snake, temp_board)  # 求得各个位置到达蛇尾的路径长度
    temp_board[temp_snake[temp_snake_size - 1]] = stat_snake  # 还原蛇尾
    return find_certain_path(temp_snake, temp_board, -1, lambda x, y: x > y)  # 返回运行方向(让蛇头运动1步)
    # 这里之所以用最长路径是因为吃食物的时候走的是最短路径，如果这里再用最短路径到后面很容易陷入死循环。
pygame.init()  # 初始化pygame
play_surface = pygame.display.set_mode((total_cols, total_rows))  # 创建pygame显示层
pygame.display.set_caption('AI贪吃蛇游戏')
play_surface.fill('black')  # 绘制pygame显示层
draw_r(play_surface, 'yellow', [0, 0, total_cols, total_rows], cell_size)  # 初始化围墙
eaten = True
while True:
    pygame.time.Clock().tick(20)  # 游戏速度控制(可调整)
    draw_r(play_surface, 'yellow', [0, 0, cell_size, cell_size])
    if eaten and snake_size < (cols - 2) * (rows - 2):
        while True:
            c = randint(1, cols - 2)
            r = randint(1, rows - 2)
            if cols * c + r not in snake[:snake_size]:
                food_position = cols * c + r
                break
        eaten = False
        draw_r(play_surface, 'red', [cell_size * r, cell_size * c, cell_size, cell_size])
    for event in pygame.event.get():
        if snake_size == (cols - 2) * (rows - 2) or event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            print(score)
            pygame.quit()
            sys.exit()
    pygame.display.flip()  # 每次循环都需要刷新pygame显示层
    board = [stat_empty for _ in range(area)]  # 重置board
    board[food_position] = stat_food
    for i in snake[:snake_size]:board[i] = stat_snake
    if bfs(food_position, snake, board):
        best_move = error  # 以下为在虚拟环境下的模拟操作，用来判断蛇是否会走入死路
        temp_snake_size = snake_size
        temp_snake = snake[:]
        temp_board = board[:]
        while True:
            bfs(food_position, temp_snake, temp_board)
            move = find_certain_path(temp_snake, temp_board, stat_snake, lambda x, y: x < y)
            for i in range(temp_snake_size, 0, -1):temp_snake[i] = temp_snake[i - 1]
            temp_snake[0] += move  # 在蛇头前加入一个新的位置
            if temp_snake[0] == food_position:  # 此时蛇头吃到食物，就可以不必向下运行，而是退出循环，看蛇头是否进入死路
                temp_snake_size += 1
                temp_board[food_position] = stat_snake
                break
            temp_board[temp_snake[0]] = stat_snake
            temp_board[temp_snake[temp_snake_size]] = stat_empty  # 虚拟贪吃蛇正常运动，直到吃到食物时停止
        # 判断虚拟贪吃蛇的蛇头是否进入死路，以便决定实际的蛇头是不是要按照虚拟蛇这么走
        temp_board = [stat_empty for _ in range(area)]  # 重置temp_board
        for i in temp_snake[:temp_snake_size - 1]:temp_board[i] = stat_snake
        temp_board[temp_snake[temp_snake_size - 1]] = stat_food  # 虚拟地将蛇尾变为食物
        temp_board[food_position] = stat_snake  # 放置食物的地方，看成蛇身,目的是避免场地上同时存在两个食物
        exist_path = bfs(temp_snake[temp_snake_size - 1], temp_snake, temp_board)
        if (not exist_path) or (temp_snake[temp_snake_size - 1] - temp_snake[0]) in list(moves.values()):
            best_move = follow_tail()  # 如果蛇头蛇尾间没有通路或者紧挨着
        else:  # 如果虚拟运行后，蛇头蛇尾间有通路，则选最短路运行一步
            best_move = find_certain_path(snake, board, stat_snake, lambda x, y: x < y)
    else:best_move = follow_tail()
    if best_move == error:
        for mov in moves.values():  # 上面所有情况均不可行，随便选择一个可行的方向走一步
            if 0 < (snake[0] + mov) % cols < cols - 1 and 0 < (snake[0] + mov) // cols < rows - 1 and board[snake[0] + mov] < stat_snake:
                best_move = mov
                break
    if best_move != error:
        for index in range(snake_size, 0, -1):snake[index] = snake[index - 1]
        snake[0] += best_move
        for body in snake[:snake_size]:
            draw_r(play_surface, 'white', [cell_size * (body % cols), cell_size * (body // cols), cell_size, cell_size])
        pygame.display.flip()
        if snake[0] == food_position:
            board[snake[0]] = stat_snake
            snake_size += 1
            score += 1
            eaten = True
        else:
            board[snake[0]] = stat_snake
            board[snake[snake_size]] = stat_empty
            draw_r(play_surface, 'black', [cell_size * (snake[snake_size] % cols), cell_size * (snake[snake_size] // cols), cell_size, cell_size])
            pygame.display.flip()
    else:
        print(score)  # 游戏结束后打印分数
        break

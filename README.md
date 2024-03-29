# 人工智能程序设计课程设计 

2023.3.31


### 项目名称
利用广度优先搜索算法实现的贪吃蛇游戏AI


### 项目中使用到的库及作用 
###### pygame：
用于实现游戏的图形化界面、速度控制和对按键状态的监听。
###### sys：
用于实现游戏的推出功能。
###### random：
用于实现随机生成食物的坐标。


### 项目中的子模块名称及作用
###### bfs函数：
项目的主要算法，将场地中每个格子中的数改为该格子到食物的曼哈顿距离，同时返回蛇头与食物间是否存在通路。
###### find_certain_path函数：
以蛇头为基准点，把与之相邻的四个点遍历一次，并且返回四个点中满足特定条件的那个点相对于蛇头的移动方向。
###### can_follow_tail函数：
检查蛇头与蛇尾之间是否存在通路，以便于避免蛇头进入死路。
###### follow_tail函数：
虚拟地控制蛇头朝蛇尾的方向运动一步。


### 环境依赖以及运行代码所需指令
本项目使用pycharm编写。推荐使用pycharm在项目模式中打开即可直接运行。也可以使用其他编辑器打开运行，但需实现在终端上安装pygame库(pip install pygame)。

### 其他说明
当游戏结束时，所得的分数会在终端中打印出来，而非直接在游戏界面中显示。
游戏的场地宽度高度、单元格的大小以及游戏运行速度都可进行直接修改，已在程序相应位置标记出来。
游戏的场地横纵长度不可太小，默认设定的20为最佳。

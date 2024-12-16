import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from random import randint, choice
from collections import deque
import matplotlib.colors as mcolors

# 设置迷宫大小
WIDTH = 60
HEIGHT = 40

# 设置递归深度
sys.setrecursionlimit(WIDTH * HEIGHT)

# 初始化已访问列表
def initVisitedList():
    return [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]

# 画线
def drawLine(x1, y1, x2, y2):
    plt.plot([x1, x2], [y1, y2], color="black")

# 删除线
def removeLine(x1, y1, x2, y2):
    plt.plot([x1, x2], [y1, y2], color="white")

# 给格子上色
def colorCell(x, y, color):
    plt.gca().add_patch(Rectangle((x, y), 1, 1, color=color))

# 获取 (x, y) 右下空格的四个边
def get_edges(x, y):
    return [
        (x, y, x, y+1),
        (x+1, y, x+1, y+1),
        (x, y, x+1, y),
        (x, y+1, x+1, y+1)
    ]

# 画一个 (x, y) 右下角的格子
def drawCell(x, y):
    for edge in get_edges(x, y):
        drawLine(edge[0], edge[1], edge[2], edge[3])

# 获取两个格子的公共边
def getCommonEdge(cell1_x, cell1_y, cell2_x, cell2_y):
    edges1 = get_edges(cell1_x, cell1_y)
    edges2 = set(get_edges(cell2_x, cell2_y))
    for edge in edges1:
        if edge in edges2:
            return edge
    return None

# 将所有边加入到边集中
def initEdgeList():
    edges = set()
    for x in range(WIDTH):
        for y in range(HEIGHT):
            for edge in get_edges(x, y):
                edges.add(edge)
    return edges

# 判断坐标是否有效（在迷宫内）
def isValidPosition(x, y):
    return 0 <= x < WIDTH and 0 <= y < HEIGHT

# 创建随机序列来随机选择方向
def shuffle(dX, dY):
    for t in range(4):
        i = randint(0, 3)
        j = randint(0, 3)
        dX[i], dX[j] = dX[j], dX[i]
        dY[i], dY[j] = dY[j], dY[i]

# 深度优先搜索凿墙创建迷宫通路
def DFS(X, Y, edgeList, visited):
    dX = [0, 0, -1, 1]
    dY = [-1, 1, 0, 0]
    shuffle(dX, dY)  # 随机选择方向
    for i in range(len(dX)):
        nextX = X + dX[i]
        nextY = Y + dY[i]  # 下一个坐标
        if isValidPosition(nextX, nextY) and not visited[nextY][nextX]:
            visited[nextY][nextX] = True
            commonEdge = getCommonEdge(X, Y, nextX, nextY)
            if commonEdge in edgeList:
                edgeList.remove(commonEdge)
            DFS(nextX, nextY, edgeList, visited)

# 广度优先搜索算法
def BFS(start, end, edgeList):
    dX = [0, 0, -1, 1]
    dY = [-1, 1, 0, 0]
    queue = deque([start])
    came_from = {start: None}
    visited = set([start])

    while queue:
        current = queue.popleft()
        if current == end:
            break
        for i in range(4):
            nextX = current[0] + dX[i]
            nextY = current[1] + dY[i]
            if isValidPosition(nextX, nextY) and (nextX, nextY) not in visited:
                commonEdge = getCommonEdge(current[0], current[1], nextX, nextY)
                if commonEdge not in edgeList:
                    queue.append((nextX, nextY))
                    visited.add((nextX, nextY))
                    came_from[(nextX, nextY)] = current
    # 重建路径
    path = []
    while end:
        path.append(end)
        end = came_from.get(end, None)
    path.reverse()
    return path

# 创建渐变颜色映射
def create_gradient_color_map(color1, color2, n=100):
    colors = [color1, color2]
    return mcolors.LinearSegmentedColormap.from_list('gradient', colors, N=n)

# 在图上绘制路径，并支持渐变颜色
def drawGradientPath(path, color1='red', color2='blue'):
    gradient = create_gradient_color_map(color1, color2, n=len(path))
    for i in range(len(path) - 1):
        plt.plot([path[i][0] + 0.5, path[i + 1][0] + 0.5], 
                 [path[i][1] + 0.5, path[i + 1][1] + 0.5], 
                 color=gradient(i / (len(path) - 1)), linewidth=2)

# 定义多个入口和出口
def define_multiple_entrances_exits(num_entrances, num_exits):
    entrances = []
    exits = []

    # 确保入口和出口不在同一位置
    all_positions = [(x, y) for x in [0, WIDTH-1] for y in range(HEIGHT)] + \
                    [(x, y) for x in range(WIDTH) for y in [0, HEIGHT-1]]
    
    selected_positions = set()

    for _ in range(num_entrances):
        pos = choice([p for p in all_positions if p not in selected_positions])
        entrances.append(pos)
        selected_positions.add(pos)

    for _ in range(num_exits):
        pos = choice([p for p in all_positions if p not in selected_positions])
        exits.append(pos)
        selected_positions.add(pos)

    return entrances, exits

# 确保入口和出口之间有路径，并且入口和出口与迷宫外部相通
def connect_entrances_exits(entrances, exits, edgeList, visited):
    def remove_border_edge(x, y):
        # 移除与迷宫外部相邻的边
        if x == 0:  # 左边界
            edgeList.discard((x, y, x, y + 1))  # 上边
            edgeList.discard((x, y, x + 1, y))  # 右边
        elif x == WIDTH - 1:  # 右边界
            edgeList.discard((x + 1, y, x + 1, y + 1))  # 上边
            edgeList.discard((x, y, x + 1, y))  # 左边
        elif y == 0:  # 底部边界
            edgeList.discard((x, y, x + 1, y))  # 右边
            edgeList.discard((x, y, x, y + 1))  # 下边
        elif y == HEIGHT - 1:  # 顶部边界
            edgeList.discard((x, y + 1, x + 1, y + 1))  # 下边
            edgeList.discard((x, y, x + 1, y))  # 右边

        # 如果位于角落，则只移除一条边
        if (x == 0 and y == 0):  # 左下角
            edgeList.discard((x, y, x, y + 1))
        elif (x == WIDTH - 1 and y == 0):  # 右下角
            edgeList.discard((x + 1, y, x + 1, y + 1))
        elif (x == 0 and y == HEIGHT - 1):  # 左上角
            edgeList.discard((x, y + 1, x + 1, y + 1))
        elif (x == WIDTH - 1 and y == HEIGHT - 1):  # 右上角
            edgeList.discard((x, y, x + 1, y))

        # 对于非角落的边缘位置，确保至少有一条边被移除
        else:
            edges_to_remove = get_edges(x, y)
            for edge in edges_to_remove:
                if edge in edgeList:
                    edgeList.remove(edge)
                    break

    # 处理入口
    for entrance in entrances:
        visited[entrance[1]][entrance[0]] = True
        DFS(entrance[0], entrance[1], edgeList, visited)
        remove_border_edge(entrance[0], entrance[1])

    # 处理出口
    for exit in exits:
        remove_border_edge(exit[0], exit[1])

# 主程序
if __name__ == "__main__":
    num_entrances = 3
    num_exits = 3
    entrances, exits = define_multiple_entrances_exits(num_entrances, num_exits)

    plt.axis('equal')
    plt.title('Maze with Multiple Entrances and Exits')

    edgeList = initEdgeList()
    visited = initVisitedList()
    connect_entrances_exits(entrances, exits, edgeList, visited)

    # 绘制迷宫
    for edge in edgeList:
        drawLine(edge[0], edge[1], edge[2], edge[3])

    #为每个入口找到到每个出口的路径并绘制
    colors1 = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    colors2 = ['#FFC0CB', '#ADD8E6', '#90EE90', '#FFFF00', '#D8BFD8', '#D2B48C']

    for i, entrance in enumerate(entrances):
        for j, exit in enumerate(exits):
            path = BFS(entrance, exit, edgeList)
            if path:
                drawGradientPath(path, 
                                color1=colors1[(i * num_exits + j) % len(colors1)], 
                                color2=colors2[(i * num_exits + j) % len(colors2)])
            else:
                print(f"No path found from entrance {entrance} to exit {exit}")

    # 绘制入口和出口
    for entrance in entrances:
        colorCell(entrance[0], entrance[1], 'yellow')
    for exit in exits:
        colorCell(exit[0], exit[1], 'cyan')

    plt.show()
import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from random import randint
from collections import deque

# 设置迷宫大小
WIDTH = 60
HEIGHT = 40

# 设置递归深度
sys.setrecursionlimit(WIDTH * HEIGHT)

# 初始化已访问列表
def initVisitedList():
    visited = []
    for y in range(HEIGHT):
        line = []
        for x in range(WIDTH):
            line.append(False)
        visited.append(line)
    return visited

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
    result = []
    result.append((x, y, x, y+1))
    result.append((x+1, y, x+1, y+1))
    result.append((x, y, x+1, y))
    result.append((x, y+1, x+1, y+1))
    return result

# 画一个 (x, y) 右下角的格子
def drawCell(x, y):
    edges = get_edges(x, y)
    for item in edges:
        drawLine(item[0], item[1], item[2], item[3])

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
    edges = set()  # 边集初始化为空集合
    for x in range(WIDTH):
        for y in range(HEIGHT):
            cellEdges = get_edges(x, y)
            for edge in cellEdges:
                edges.add(edge)
    return edges

# 判断坐标是否有效（在迷宫内）
def isValidPosition(x, y):
    if x < 0 or x >= WIDTH:
        return False
    elif y < 0 or y >= HEIGHT:
        return False
    else:
        return True

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
        if isValidPosition(nextX, nextY):
            if not visited[nextY][nextX]:
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

# 在图上绘制路径
def drawPath(path, color='red'):
    for i in range(len(path) - 1):
        plt.plot([path[i][0] + 0.5, path[i + 1][0] + 0.5], [path[i][1] + 0.5, path[i + 1][1] + 0.5], color=color, linewidth=2)

# 设置起点和终点
start = (0, 0)
end = (WIDTH-1, HEIGHT-1)

# 初始化迷宫
plt.axis('equal')
plt.title('Maze')
edgeList = initEdgeList()
visited = initVisitedList()
DFS(0, 0, edgeList, visited)
edgeList.remove((0, 0, 0, 1))  # 创建起点
edgeList.remove((WIDTH, HEIGHT-1, WIDTH, HEIGHT))  # 创建终点

# 绘制迷宫
for edge in edgeList:
    drawLine(edge[0], edge[1], edge[2], edge[3])

# 执行BFS并获取路径
path = BFS(start, end, edgeList)

# 绘制路径
if path:
    drawPath(path)
else:
    print("No path found")

plt.show()
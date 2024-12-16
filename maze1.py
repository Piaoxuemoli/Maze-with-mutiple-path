import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from random import randint
from collections import deque

# �����Թ���С
WIDTH = 60
HEIGHT = 40

# ���õݹ����
sys.setrecursionlimit(WIDTH * HEIGHT)

# ��ʼ���ѷ����б�
def initVisitedList():
    visited = []
    for y in range(HEIGHT):
        line = []
        for x in range(WIDTH):
            line.append(False)
        visited.append(line)
    return visited

# ����
def drawLine(x1, y1, x2, y2):
    plt.plot([x1, x2], [y1, y2], color="black")

# ɾ����
def removeLine(x1, y1, x2, y2):
    plt.plot([x1, x2], [y1, y2], color="white")

# ��������ɫ
def colorCell(x, y, color):
    plt.gca().add_patch(Rectangle((x, y), 1, 1, color=color))

# ��ȡ (x, y) ���¿ո���ĸ���
def get_edges(x, y):
    result = []
    result.append((x, y, x, y+1))
    result.append((x+1, y, x+1, y+1))
    result.append((x, y, x+1, y))
    result.append((x, y+1, x+1, y+1))
    return result

# ��һ�� (x, y) ���½ǵĸ���
def drawCell(x, y):
    edges = get_edges(x, y)
    for item in edges:
        drawLine(item[0], item[1], item[2], item[3])

# ��ȡ�������ӵĹ�����
def getCommonEdge(cell1_x, cell1_y, cell2_x, cell2_y):
    edges1 = get_edges(cell1_x, cell1_y)
    edges2 = set(get_edges(cell2_x, cell2_y))
    for edge in edges1:
        if edge in edges2:
            return edge
    return None

# �����б߼��뵽�߼���
def initEdgeList():
    edges = set()  # �߼���ʼ��Ϊ�ռ���
    for x in range(WIDTH):
        for y in range(HEIGHT):
            cellEdges = get_edges(x, y)
            for edge in cellEdges:
                edges.add(edge)
    return edges

# �ж������Ƿ���Ч�����Թ��ڣ�
def isValidPosition(x, y):
    if x < 0 or x >= WIDTH:
        return False
    elif y < 0 or y >= HEIGHT:
        return False
    else:
        return True

# ����������������ѡ����
def shuffle(dX, dY):
    for t in range(4):
        i = randint(0, 3)
        j = randint(0, 3)
        dX[i], dX[j] = dX[j], dX[i]
        dY[i], dY[j] = dY[j], dY[i]

# �������������ǽ�����Թ�ͨ·
def DFS(X, Y, edgeList, visited):
    dX = [0, 0, -1, 1]
    dY = [-1, 1, 0, 0]
    shuffle(dX, dY)  # ���ѡ����
    for i in range(len(dX)):
        nextX = X + dX[i]
        nextY = Y + dY[i]  # ��һ������
        if isValidPosition(nextX, nextY):
            if not visited[nextY][nextX]:
                visited[nextY][nextX] = True
                commonEdge = getCommonEdge(X, Y, nextX, nextY)
                if commonEdge in edgeList:
                    edgeList.remove(commonEdge)
                DFS(nextX, nextY, edgeList, visited)

# ������������㷨
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
    # �ؽ�·��
    path = []
    while end:
        path.append(end)
        end = came_from.get(end, None)
    path.reverse()
    return path

# ��ͼ�ϻ���·��
def drawPath(path, color='red'):
    for i in range(len(path) - 1):
        plt.plot([path[i][0] + 0.5, path[i + 1][0] + 0.5], [path[i][1] + 0.5, path[i + 1][1] + 0.5], color=color, linewidth=2)

# ���������յ�
start = (0, 0)
end = (WIDTH-1, HEIGHT-1)

# ��ʼ���Թ�
plt.axis('equal')
plt.title('Maze')
edgeList = initEdgeList()
visited = initVisitedList()
DFS(0, 0, edgeList, visited)
edgeList.remove((0, 0, 0, 1))  # �������
edgeList.remove((WIDTH, HEIGHT-1, WIDTH, HEIGHT))  # �����յ�

# �����Թ�
for edge in edgeList:
    drawLine(edge[0], edge[1], edge[2], edge[3])

# ִ��BFS����ȡ·��
path = BFS(start, end, edgeList)

# ����·��
if path:
    drawPath(path)
else:
    print("No path found")

plt.show()
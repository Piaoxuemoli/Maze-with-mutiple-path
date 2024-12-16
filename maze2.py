import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from random import randint, choice
from collections import deque
import matplotlib.colors as mcolors

# �����Թ���С
WIDTH = 60
HEIGHT = 40

# ���õݹ����
sys.setrecursionlimit(WIDTH * HEIGHT)

# ��ʼ���ѷ����б�
def initVisitedList():
    return [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]

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
    return [
        (x, y, x, y+1),
        (x+1, y, x+1, y+1),
        (x, y, x+1, y),
        (x, y+1, x+1, y+1)
    ]

# ��һ�� (x, y) ���½ǵĸ���
def drawCell(x, y):
    for edge in get_edges(x, y):
        drawLine(edge[0], edge[1], edge[2], edge[3])

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
    edges = set()
    for x in range(WIDTH):
        for y in range(HEIGHT):
            for edge in get_edges(x, y):
                edges.add(edge)
    return edges

# �ж������Ƿ���Ч�����Թ��ڣ�
def isValidPosition(x, y):
    return 0 <= x < WIDTH and 0 <= y < HEIGHT

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
        if isValidPosition(nextX, nextY) and not visited[nextY][nextX]:
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

# ����������ɫӳ��
def create_gradient_color_map(color1, color2, n=100):
    colors = [color1, color2]
    return mcolors.LinearSegmentedColormap.from_list('gradient', colors, N=n)

# ��ͼ�ϻ���·������֧�ֽ�����ɫ
def drawGradientPath(path, color1='red', color2='blue'):
    gradient = create_gradient_color_map(color1, color2, n=len(path))
    for i in range(len(path) - 1):
        plt.plot([path[i][0] + 0.5, path[i + 1][0] + 0.5], 
                 [path[i][1] + 0.5, path[i + 1][1] + 0.5], 
                 color=gradient(i / (len(path) - 1)), linewidth=2)

# ��������ںͳ���
def define_multiple_entrances_exits(num_entrances, num_exits):
    entrances = []
    exits = []

    # ȷ����ںͳ��ڲ���ͬһλ��
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

# ȷ����ںͳ���֮����·����������ںͳ������Թ��ⲿ��ͨ
def connect_entrances_exits(entrances, exits, edgeList, visited):
    def remove_border_edge(x, y):
        # �Ƴ����Թ��ⲿ���ڵı�
        if x == 0:  # ��߽�
            edgeList.discard((x, y, x, y + 1))  # �ϱ�
            edgeList.discard((x, y, x + 1, y))  # �ұ�
        elif x == WIDTH - 1:  # �ұ߽�
            edgeList.discard((x + 1, y, x + 1, y + 1))  # �ϱ�
            edgeList.discard((x, y, x + 1, y))  # ���
        elif y == 0:  # �ײ��߽�
            edgeList.discard((x, y, x + 1, y))  # �ұ�
            edgeList.discard((x, y, x, y + 1))  # �±�
        elif y == HEIGHT - 1:  # �����߽�
            edgeList.discard((x, y + 1, x + 1, y + 1))  # �±�
            edgeList.discard((x, y, x + 1, y))  # �ұ�

        # ���λ�ڽ��䣬��ֻ�Ƴ�һ����
        if (x == 0 and y == 0):  # ���½�
            edgeList.discard((x, y, x, y + 1))
        elif (x == WIDTH - 1 and y == 0):  # ���½�
            edgeList.discard((x + 1, y, x + 1, y + 1))
        elif (x == 0 and y == HEIGHT - 1):  # ���Ͻ�
            edgeList.discard((x, y + 1, x + 1, y + 1))
        elif (x == WIDTH - 1 and y == HEIGHT - 1):  # ���Ͻ�
            edgeList.discard((x, y, x + 1, y))

        # ���ڷǽ���ı�Եλ�ã�ȷ��������һ���߱��Ƴ�
        else:
            edges_to_remove = get_edges(x, y)
            for edge in edges_to_remove:
                if edge in edgeList:
                    edgeList.remove(edge)
                    break

    # �������
    for entrance in entrances:
        visited[entrance[1]][entrance[0]] = True
        DFS(entrance[0], entrance[1], edgeList, visited)
        remove_border_edge(entrance[0], entrance[1])

    # �������
    for exit in exits:
        remove_border_edge(exit[0], exit[1])

# ������
if __name__ == "__main__":
    num_entrances = 3
    num_exits = 3
    entrances, exits = define_multiple_entrances_exits(num_entrances, num_exits)

    plt.axis('equal')
    plt.title('Maze with Multiple Entrances and Exits')

    edgeList = initEdgeList()
    visited = initVisitedList()
    connect_entrances_exits(entrances, exits, edgeList, visited)

    # �����Թ�
    for edge in edgeList:
        drawLine(edge[0], edge[1], edge[2], edge[3])

    #Ϊÿ������ҵ���ÿ�����ڵ�·��������
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

    # ������ںͳ���
    for entrance in entrances:
        colorCell(entrance[0], entrance[1], 'yellow')
    for exit in exits:
        colorCell(exit[0], exit[1], 'cyan')

    plt.show()
import numpy as np
import math





# areacal(v1,v2,v3)由三个顶点坐标计算三角形面积
def areacal(v1, v2, v3):
    a = math.sqrt((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2 + (v1[2] - v2[2]) ** 2)
    b = math.sqrt((v2[0] - v3[0]) ** 2 + (v2[1] - v3[1]) ** 2 + (v2[2] - v3[2]) ** 2)
    c = math.sqrt((v1[0] - v3[0]) ** 2 + (v1[1] - v3[1]) ** 2 + (v1[2] - v3[2]) ** 2)
    p = (a + b + c) / 2
    return math.sqrt(p * (p - a) * (p - b) * (p - c))


# 读入数据
elements_file = 'data/elephant.elements.txt'  #记录哪三个点构成一个三角形
nodes_file = 'data/elephant.nodes.txt'        #记录点的坐标

elements_data = np.loadtxt(elements_file)  #记录哪三个点构成三角形
nodes_data = np.loadtxt(nodes_file)         #记录点的坐标
print(nodes_data)
elephant_area = 0
# 计算每一个三角形的面积
for element in elements_data:
    v1 = [nodes_data[int(element[1]) - 1][1], nodes_data[int(element[1]) - 1][2], nodes_data[int(element[1]) - 1][3]]
    v2 = [nodes_data[int(element[2]) - 1][1], nodes_data[int(element[2]) - 1][2], nodes_data[int(element[2]) - 1][3]]
    v3 = [nodes_data[int(element[3]) - 1][1], nodes_data[int(element[3]) - 1][2], nodes_data[int(element[3]) - 1][3]]
    elephant_area += areacal(v1, v2, v3)
elements_file = 'data/Mountain.elements.txt'
nodes_file = 'data/Mountain.nodes.txt'
print("wangfuhao1")
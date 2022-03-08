import numpy as np
import cv2


# 使用叉乘计算三角形面积
def vecTriangleArea(point, depth_z):
    if np.size(point, 0) != 3:
        print("error,the point size is not 3")
        return 0
    data = point[np.argsort(point[:, 2])]
    edge_vector1 = data[1] - data[0]
    edge_vector2 = data[2] - data[0]
    # z平面深度小于深度最小值，直接返回0
    if depth_z <= data[0, 2]:
        return 0
    # z平面深度大于深度最大值但是小于等于深度次小值，直接计算z平面靠近相机侧的三角形面积
    elif depth_z <= data[1, 2]:
        k1 = (depth_z - data[0, 2]) / (data[1, 2] - data[0, 2])
        k2 = (depth_z - data[0, 2]) / (data[2, 2] - data[0, 2])
        edge_vector1 = k1 * edge_vector1
        edge_vector2 = k2 * edge_vector2
        return 0.5 * np.linalg.norm(np.cross(edge_vector1, edge_vector2))
    # z平面深度仅小于深度最大值，使用完整三角形减去z平面远离相机侧的三角形面积
    elif depth_z < data[2, 2]:
        k1 = (depth_z - data[2, 2]) / (data[0, 2] - data[2, 2])
        k2 = (depth_z - data[2, 2]) / (data[1, 2] - data[2, 2])
        sub_edge_vector1 = k1 * (data[0] - data[2])
        sub_edge_vector2 = k2 * (data[1] - data[2])
        return 0.5 * np.linalg.norm(np.cross(edge_vector1, edge_vector2)) - 0.5 * np.linalg.norm(
            np.cross(sub_edge_vector1, sub_edge_vector2))
    # z平面深度大于深度最大值，则直接计算完整三角形面积
    else:
        return 0.5 * np.linalg.norm(np.cross(edge_vector1, edge_vector2))


def square_area(point, depth_z):
    point1 = point[:3]
    point2 = point[1:]
    return vecTriangleArea(point1, depth_z) + vecTriangleArea(point2, depth_z)


def triangle_area(point, depth_z):
    return vecTriangleArea(point, depth_z)


def surfaceComputing(src, midline, depth_z):
    ans = [0, 0]
    h = len(midline)
    w = src.shape[1]
    for i in range(1, h):
        for j in range(1, midline[i] + 1):
            if j == midline[i]:
                pre = midline[i - 1]
                # 判断与上一个中线位置形成的形状并计算面积（三角形或者正方形）
                if pre < j:
                    point = [[pre, i, src[i, pre]],
                             [pre, i - 1, src[i - 1, pre]],
                             [j, i, src[i, j]]]
                    ans[0] += triangle_area(point, depth_z)
                elif pre == j:
                    point = [[j - 1, i - 1, src[i - 1, j - 1]],
                             [j, i - 1, src[i - 1, j]],
                             [j - 1, i, src[i, j - 1]],
                             [j, i, src[i, j]]]
                    ans[0] += square_area(point, depth_z)
                else:
                    point = [[j, i - 1, src[i - 1, j]],
                             [pre, i - 1, src[i - 1, pre]],
                             [j, i, src[i, j]]]
                    ans[0] += triangle_area(point, depth_z)
            else:
                point = [[j - 1, i - 1, src[i - 1, j - 1]],
                         [j, i - 1, src[i - 1, j]],
                         [j - 1, i, src[i, j - 1]],
                         [j, i, src[i, j]]]
                ans[0] += square_area(point, depth_z)
        for j in range(w - 2, midline[i] - 1, -1):
            if j == midline[i]:
                pre = midline[i - 1]
                if pre > j:
                    point = [[pre, i, src[i, pre]],
                             [pre, i - 1, src[i - 1, pre]],
                             [j, i, src[i, j]]]
                    ans[1] += triangle_area(point, depth_z)
                elif pre == j:
                    point = [[j + 1, i - 1, src[i - 1, j + 1]],
                             [j, i - 1, src[i - 1, j]],
                             [j + 1, i, src[i, j + 1]],
                             [j, i, src[i, j]]]
                    ans[1] += square_area(point, depth_z)
                else:
                    point = [[j, i - 1, src[i - 1, j]],
                             [pre, i - 1, src[i - 1, pre]],
                             [j, i, src[i, j]]]
                    ans[1] += triangle_area(point, depth_z)
            else:
                point = [[j + 1, i - 1, src[i - 1, j + 1]],
                         [j, i - 1, src[i - 1, j]],
                         [j + 1, i, src[i, j + 1]],
                         [j, i, src[i, j]]]
                ans[1] += square_area(point, depth_z)
    return ans

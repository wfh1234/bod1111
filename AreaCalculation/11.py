# import numpy as np
# import cv2
#
# def vecTriangleArea(point,depth_z):
#     if np.size(point, 0)!=3: #np.size()统计矩阵元素的个数
#         print("error,the point size is nont 3")
#         return 0
#     data=point[np.argsort(point[:,2])] #np.argsort() 先排序，然后找出排序后对应的索引号
#     edge_vector1=data[1]-data[0]
#     edge_vector2=data[2]-data[0]
#     #z平面的深度小于深度最小值，直接返回0
#     if depth_z<=data[0,2]:
#         return 0
#     #z平面的深度大于深度最大值但是小于深度次小值，直接计算z平面靠近相机侧的三角形的面积
#     elif depth_z<=data[1, 2]:
#         k1=(depth_z-data[0,2])/(data[1,2]-data[0,2])
#         k2=(depth_z-data[0,2])/(data[2,2]-data[0,2])
#         edge_vector1=k1*edge_vector1
#         edge_vector2=k2*edge_vector2
#         return 0.5*np.linalg.norm(np.cross(edge_vector1,edge_vector2))
#     elif depth_z <data[2,2]:
#
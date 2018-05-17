#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np  # 载入numpy
import math  # 载入 math
import matplotlib as mpl #载入matplotlib
import matplotlib.pyplot as plt
import RTtoB
import QtoDCM
import DCMtoQ

file_address = "/Users/wangtianrun/Downloads/IR_Mat_V1_0/Test11.dat"  #定位数据文件位置

###########################################数据导入##########################################
f = open(file_address, 'r')             # 打开文件，只读

lines = 0
row = 0

for line in f.readlines():#读取文件行数
    lines += 1
    if lines == 1:
        for str in line:
            if str == ' ':#读取文件列数
                row += 1

Row = lines - 197399                 #储存数据维度
Line = row

Data = np.zeros((Row, Line))#创建数据矩阵

lines = 1

data1 = ''
f.close()

f = open(file_address, 'r')
i = 0
j = 0
for line in f.readlines():  #逐行读取
    if lines > 197399:
        for str in line:        #逐字读取
            if str == ' ':     #判断空格
                Data[i - 197399,j] = float(data1)#字符串转换成浮点数并储存至 Data 矩阵
                j += 1
                data1 = ''      #清空
                continue
            data1 += str        #字符串拼接
    lines += 1
    i += 1
    j = 0

f.close()

##############################变量初始化###################################
dt = 0.001                          # 积分时间
Time = Data[:, 0]*0.001             # 系统时间
Gyro = Data[:, 1: 4] * math.pi/ 180 # 陀螺仪数据            列表中a:b表示从第 a+1 项的前面到 b+1 项的前面
Acc = Data[:, 4: 7]                 #加速度计数据
Att = np.zeros((Row, 3))

###############################初始对准####################################
f_x = np.mean(Acc[0: 20, 0], 0)
f_y = np.mean(Acc[0: 20, 1], 0)
f_z = np.mean(Acc[0: 20, 2], 0)

roll = math.atan2(-f_y,-f_z)
pitch = math.asin(f_x/ math.sqrt(f_x ** 2+ f_y ** 2+ f_z ** 2))
yaw = 0
Att[0, 0:3] = [ x * 180/ math.pi for x in [yaw, pitch, roll] ]         #list * a 表示将 list 复制 a 次，故不能使用直接相乘的方法,要么将 list 转换成矩阵，要么用本行的方法

attitude = np.array([[roll], [pitch], [0]])

Rb2t = np.array(RTtoB.Rt2b(attitude))

Rb2t = Rb2t.T

q = DCMtoQ.dcm2q(Rb2t)

L_G = np.array ([[Time[1499], Time[1499]], [-180, 100]])

###############################数据处理###################################
for i in range(Row):                                                        #i从i=0开始循环
    if i > 0:
        dt = (Data[i,0]-Data[i-1,0]) * 0.001

    w_tb = Gyro[i, 0:3]

    P = w_tb[0] * dt   #一阶比卡算法
    Q = w_tb[1] * dt
    R = w_tb[2] * dt
    OMEGA = np.zeros((4,4))
    OMEGA[0, :] = 0.5 * np.array([ 0,   R,  -Q,   P])
    OMEGA[1, :] = 0.5 * np.array([-R,   0,   P,   Q])
    OMEGA[2, :] = 0.5 * np.array([ Q,  -P,   0,   R])
    OMEGA[3, :] = 0.5 * np.array([-P,  -Q,  -R,   0])

    v = np.linalg.norm(w_tb) * dt       #和 matlab的 norm()函数计算结果有误差

    if v != 0 :
        q = np.dot((math.cos(v / 2) * np.eye(4) + 2 / v * math.sin(v / 2) * OMEGA) , q ) # 矩阵内乘法要使用 np.dot(A,B)
        q = q / np.linalg.norm(q)

    Rb2t = QtoDCM.q2dcm(q)

    # roll
    roll = math.atan2(Rb2t[2, 1], Rb2t[2, 2])
    # pitch
    pitch = -math.atan(Rb2t[2, 0] / math.sqrt(1 - Rb2t[2, 0] ** 2))
    # yaw
    yaw = math.atan2(Rb2t[1, 0], Rb2t[0, 0])

    Att[i, 0: 3] = np.array([yaw, pitch, roll]) * 180 / math.pi

################################显示输出################################

mpl.rcParams['xtick.labelsize'] = 12 # 通过rcParams设置全局横纵轴字体大小
mpl.rcParams['ytick.labelsize'] = 12

plt.figure('data')#图的名称
plt.axis([317.8, 319.8, -200, 200])#横纵坐标刻度与范围

plt.plot(Time, Att[:,0], 'r',label = 'yaw')
plt.plot(Time, Att[:,1], 'g',label = 'pitch')
plt.plot(Time, Att[:,2], 'b',label = 'roll')
plt.plot(L_G[0, : ], L_G[1, : ], 'k')

plt.legend()
plt.show()


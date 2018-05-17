#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
def Rt2b(ang):  # Rt2b函数定义
    cr = math.cos(ang[0])
    sr = math.sin(ang[0])

    cp = math.cos(ang[1])
    sp = math.sin(ang[1])

    cy = math.cos(ang[2])
    sy = math.sin(ang[2])

    return [[cy * cp, sy * cp, -sp],
            [-sy * cr + cy * sp * sr, cy * cr + sy * sp * sr, cp * sr],
            [sy * sr + cy * sp * cr, - cy * sr + sy * sp * cr, cp * cr]]

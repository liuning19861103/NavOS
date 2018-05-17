#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def dcm2q(R):   # dcm2q函数定义

    T = 1 + R[0, 0] + R[1, 1] + R[2, 2]

    if T > 10 ^ (-8):

        S = 0.5 / T ** 0.5
        qw = 0.25 / S
        qx = (R[2, 1] - R[1, 2]) * S
        qy = (R[0, 2] - R[2, 0]) * S
        qz = (R[1, 0] - R[0, 1]) * S

    else:

        if (R[0, 0] > R[1, 1]) and (R[0, 0] > R[2, 2]):

            S = ((1 + R[0, 0] - R[1, 1] - R[2, 2]) ** 0.5) * 2 # S = 4 * qx
            qw = (R[2, 1] - R[1, 2]) / S
            qx = 0.25 * S
            qy = (R[0, 1] + R[1, 0]) / S
            qz = (R[0, 2] + R[2, 0]) / S

        elif (R[1, 1] > R[2, 2]):

            S = ((1 + R[1, 1] - R[0, 0] - R[2, 2]) ** 0.5) * 2 # S = 4 * qy
            qw = (R[0, 2] - R[2, 0]) / S
            qx = (R[0, 1] + R[1, 0]) / S
            qy = 0.25 * S
            qz = (R[1, 2] + R[2, 1]) / S

        else:

            S = ((1 + R[2, 2] - R[0, 0] - R[1, 1]) ** 0.5) * 2 # S = 4 * qz
            qw = (R[1, 0] - R[0, 1]) / S
            qx = (R[0, 2] + R[2, 0]) / S
            qy = (R[1, 2] + R[2, 1]) / S
            qz = 0.25 * S

    # Store in vector
    q = [[qx], [qy], [qz], [qw]]
    return q
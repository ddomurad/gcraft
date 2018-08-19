from math import *
import numpy as np


def v3_length(v):
    return sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])


def v3_length2(v):
    return v[0]*v[0] + v[1]*v[1] + v[2]*v[2]


def v3_normalize(v):
    length = v3_length(v)
    return [v[0]/length, v[1]/length, v[2]/length]


def v3_normalize_self(v):
    length = v3_length(v)
    if length == 0.0:
        length = 0.0000001

    v[0] = v[0] / length
    v[1] = v[1] / length
    v[2] = v[2] / length
    return v

def v3_add(v1, v2):
    return [v2[0]+v1[0], v2[1]+v1[1], v2[2]+v1[2]]


def v3_add_self(v1, v2):
    v1[0] += v2[0]
    v1[1] += v2[1]
    v1[2] += v2[2]
    return v1


def v3_sub(v1, v2):
    return [v2[0]-v1[0], v2[1]-v1[1], v2[2]-v1[2]]


def v3_mul(v, k):
    return [v[0]*k, v[1]*k, v[2]*k]


def v3_rotate(v, axis, angle):
    q = q4_mk_quaternion(axis, angle)
    return v3_transform_quaternion(q, v)


def v3_rotate_self(v, axis, angle):
    q = q4_mk_quaternion(axis, angle)
    nv = v3_transform_quaternion(q, v)
    v[0] = nv[0]
    v[1] = nv[1]
    v[2] = nv[2]


def v3_cross(v1, v2):
    return [v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]]


def v3_cross_self(v1, v2):
    v1[:] = v3_cross(v1, v2)
    return v1


def q4_mk_quaternion(axis, angle):
    sa = sin(angle / 2)
    return [
        axis[0] * sa,
        axis[1] * sa,
        axis[2] * sa,
        cos(angle / 2)]


def v3_transform_quaternion(q, v):
    x2 = q[0] + q[0]
    y2 = q[1] + q[1]
    z2 = q[2] + q[2]

    wx2 = q[3] * x2
    wy2 = q[3] * y2
    wz2 = q[3] * z2

    xx2 = q[0] * x2
    xy2 = q[0] * y2
    xz2 = q[0] * z2

    yy2 = q[1] * y2
    yz2 = q[1] * z2
    zz2 = q[2] * z2

    x = v[0] * (1.0 - yy2 - zz2) + v[1] * (xy2 - wz2) + v[2] * (xz2 + wy2)
    y = v[0] * (xy2 + wz2) + v[1] * (1.0 - xx2 - zz2) + v[2] * (yz2 - wx2)
    z = v[0] * (xz2 - wy2) + v[1] * (yz2 + wx2) + v[2] * (1.0 - xx2 - yy2)

    return [x, y, z]


def m4_empty():
    return np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

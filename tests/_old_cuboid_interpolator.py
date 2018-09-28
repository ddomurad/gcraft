from functools import reduce
from gcraft.utils.vector_ops import *

"""
vertex pos:

ZYX
000
001
010
011
100
101
110
111


ex.
v_pos: ZYX=001 => x: s, y: -s, z: -s => (0 => -s, 1 => s)


cube coding:
[b0 b1 b2 b3 b4 b5 b6 b7] => bX: v_pos(ZYX=X)

ex.
b3 => vpos(ZYX:011) => x=s, y=s, z=-s

    [6]-------[7]
   / |        /|
  /  |       / |
[2]--------[3] |
 |   |      |  |
 |  [4]-----|-[5]
 | /        | /
 |/         |/
[0]--------[1]

"""


def _get_corner_vec(c, s):
    x = s if (0x01 & c) > 0 else -s
    y = s if (0x02 & c) > 0 else -s
    z = s if (0x04 & c) > 0 else -s
    return [x, y, z]


def _data_to_mesh_type(data):
    bin_data = [d > 0 for d in data]
    return sum([2**i for (i, b) in enumerate(bin_data) if b > 0])


def _generate_triangle(A, B, C, s):
    c_a1 = _get_corner_vec(A[0], s)
    c_a2 = _get_corner_vec(A[1], s)

    c_b1 = _get_corner_vec(B[0], s)
    c_b2 = _get_corner_vec(B[1], s)

    c_c1 = _get_corner_vec(C[0], s)
    c_c2 = _get_corner_vec(C[1], s)

    c_a = v3_add(c_a1, c_a2)
    c_b = v3_add(c_b1, c_b2)
    c_c = v3_add(c_c1, c_c2)

    v3_div_self(c_a, 2)
    v3_div_self(c_b, 2)
    v3_div_self(c_c, 2)

    return reduce(list.__add__, [c_a, c_b, c_c])


ROT_90X1_X_MAP = {0: 2, 1: 3, 2: 6, 3: 7, 4: 0, 5: 1, 6: 4, 7: 5}
ROT_90X2_X_MAP = {0: 6, 1: 7, 2: 4, 3: 5, 4: 2, 5: 3, 6: 0, 7: 1}
ROT_90X3_X_MAP = {0: 4, 1: 5, 2: 0, 3: 1, 4: 6, 5: 7, 6: 2, 7: 3}

ROT_90X1_Y_MAP = {0: 1, 1: 5, 2: 3, 3: 7, 4: 0, 5: 4, 6: 2, 7: 6}
ROT_90X2_Y_MAP = {0: 5, 1: 4, 2: 7, 3: 6, 4: 1, 5: 0, 6: 3, 7: 2}
ROT_90X3_Y_MAP = {0: 4, 1: 0, 2: 6, 3: 2, 4: 5, 5: 1, 6: 7, 7: 3}

ROT_90X1_Z_MAP = {0: 2, 1: 0, 2: 3, 3: 1, 4: 6, 5: 4, 6: 7, 7: 5}
ROT_90X2_Z_MAP = {0: 3, 1: 2, 2: 1, 3: 0, 4: 7, 5: 6, 6: 5, 7: 4}
ROT_90X3_Z_MAP = {0: 1, 1: 3, 2: 0, 3: 2, 4: 5, 5: 7, 6: 4, 7: 6}

MIRROR_X_MAP = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6}
MIRROR_Y_MAP = {0: 2, 1: 3, 2: 0, 3: 1, 4: 6, 5: 7, 6: 4, 7: 5}


def _apply_map(edges, rot_map):
    return [[(rot_map[ed[0]], rot_map[ed[1]]) for ed in edge] for edge in edges]


def rot_90x1_x(edges):
    return _apply_map(edges, ROT_90X1_X_MAP)


def rot_90x2_x(edges):
    return _apply_map(edges, ROT_90X2_X_MAP)


def rot_90x3_x(edges):
    return _apply_map(edges, ROT_90X3_X_MAP)


def rot_90x1_y(edges):
    return _apply_map(edges, ROT_90X1_Y_MAP)


def rot_90x2_y(edges):
    return _apply_map(edges, ROT_90X2_Y_MAP)


def rot_90x3_y(edges):
    return _apply_map(edges, ROT_90X3_Y_MAP)


def rot_90x1_z(edges):
    return _apply_map(edges, ROT_90X1_Z_MAP)


def rot_90x2_z(edges):
    return _apply_map(edges, ROT_90X2_Z_MAP)


def rot_90x3_z(edges):
    return _apply_map(edges, ROT_90X3_Z_MAP)


def reverse_edges(edges):
    return [list(reversed(e)) for e in edges]


def mirror_x(edges):
    return reverse_edges(_apply_map(edges, MIRROR_X_MAP))

def mirror_y(edges):
    return reverse_edges(_apply_map(edges, MIRROR_Y_MAP))


def _get_case_1_edges():
    return [[(0, 1), (0, 2), (0, 4)]]


def _get_case_3_edges():
    return [[(0, 4), (1, 5), (1, 3)], [(0, 4), (1, 3), (0, 2)]]


def _get_case_7_edges():
    return [[(0, 4), (1, 5), (1, 3)], [(0, 4), (1, 3), (2, 3)], [(0, 4), (2, 3), (2, 6)]]


def _get_case_15_edges():
    return [[(0, 4), (3, 7), (2, 6)], [(0, 4), (1, 5), (3, 7)]]


def _get_case_23_edges():
    return [[(4, 5), (1, 5), (4, 6)], [(4, 6), (1, 5), (1, 3)], [(4, 6), (1, 3), (2, 6)], [(2, 6), (1, 3), (2, 3)]]


def _get_case_27_edges():
    return [[(4, 5), (1, 5), (4, 6)], [(4, 6), (1, 5), (0, 2)], [(3, 7), (0, 2), (1, 5)], [(0, 2), (3, 7), (2, 3)]]


def interpolate_cuboid_mesh(data, size):
    mtype = _data_to_mesh_type(data)
    edges = []

    if mtype == 1:
        edges.extend(_get_case_1_edges())
    elif mtype == 2:
        edges.extend(rot_90x1_y(_get_case_1_edges()))
    elif mtype == 3:
        edges.extend(_get_case_3_edges())
    elif mtype == 4:
        edges.extend(rot_90x1_z(_get_case_1_edges()))
    elif mtype == 5:
        edges.extend(rot_90x1_z(_get_case_3_edges()))
    elif mtype == 6:
        edges.extend(rot_90x1_y(_get_case_1_edges()))
        edges.extend(rot_90x1_z(_get_case_1_edges()))
    elif mtype == 7:
        edges.extend(_get_case_7_edges())
    elif mtype == 8:
        edges.extend(rot_90x2_z(_get_case_1_edges()))
    elif mtype == 9:
        edges.extend(_get_case_1_edges())
        edges.extend(rot_90x2_z(_get_case_1_edges()))
    elif mtype == 10:
        edges.extend(rot_90x3_z(_get_case_3_edges()))
    elif mtype == 11:
        edges.extend(mirror_x(_get_case_7_edges()))
    elif mtype == 12:
        edges.extend(rot_90x1_x(_get_case_3_edges()))
    elif mtype == 13:
        edges.extend(rot_90x1_z(_get_case_7_edges()))
    elif mtype == 14:
        edges.extend(rot_90x2_z(_get_case_7_edges()))
    elif mtype == 15:
        edges.extend(_get_case_15_edges())
    elif mtype == 16:
        edges.extend(rot_90x3_y(_get_case_1_edges()))
    elif mtype == 16:
        edges.extend(rot_90x3_y(_get_case_1_edges()))
    elif mtype == 17:
        edges.extend(rot_90x3_y(_get_case_3_edges()))
    elif mtype == 18:
        edges.extend(rot_90x1_y(_get_case_1_edges()))
        edges.extend(rot_90x3_y(_get_case_1_edges()))
    elif mtype == 19:
        edges.extend(rot_90x1_y(rot_90x3_x(_get_case_7_edges())))
    elif mtype == 20:
        edges.extend(rot_90x1_x(_get_case_1_edges()))
        edges.extend(rot_90x3_x(_get_case_1_edges()))
    elif mtype == 21:
        edges.extend(rot_90x3_z(rot_90x1_x(_get_case_7_edges())))
    elif mtype == 22:
        edges.extend(rot_90x1_y(_get_case_1_edges()))
        edges.extend(rot_90x1_x(_get_case_1_edges()))
        edges.extend(rot_90x3_x(_get_case_1_edges()))
    elif mtype == 23:
        edges.extend(_get_case_23_edges())
    elif mtype == 24:
        edges.extend(rot_90x3_y(_get_case_1_edges()))
        edges.extend(rot_90x2_z(_get_case_1_edges()))
    elif mtype == 25:
        edges.extend(rot_90x2_z(_get_case_1_edges()))
        edges.extend(rot_90x3_y(_get_case_3_edges()))
    elif mtype == 26:
        edges.extend(rot_90x3_y(_get_case_1_edges()))
        edges.extend(rot_90x3_z(_get_case_3_edges()))
    elif mtype == 27:
        edges.extend(_get_case_27_edges())
    elif mtype == 28:
        edges.extend(rot_90x3_y(_get_case_1_edges()))
        edges.extend(rot_90x1_x(_get_case_3_edges()))
    elif mtype == 29:
        edges.extend(mirror_x(rot_90x3_z(_get_case_27_edges())))
    elif mtype == 30:
        edges.extend(mirror_x(rot_90x1_z(_get_case_7_edges())))
        edges.extend(mirror_x(rot_90x2_y(_get_case_1_edges())))
    elif mtype == 31:
        edges.extend(reverse_edges(rot_90x3_z(rot_90x2_y(_get_case_7_edges()))))
    elif mtype == 32:
        edges.extend(rot_90x2_y(_get_case_1_edges()))
    elif mtype == 33:
        edges.extend(rot_90x2_y(_get_case_1_edges()))
        edges.extend(_get_case_1_edges())
    elif mtype == 34:
        edges.extend(rot_90x1_y(_get_case_3_edges()))
    elif mtype == 35:
        edges.extend(rot_90x2_y(rot_90x3_x(_get_case_7_edges())))
    elif mtype == 36:
        edges.extend(rot_90x2_y(_get_case_1_edges()))
        edges.extend(rot_90x1_z(_get_case_1_edges()))
    elif mtype == 37:
        edges.extend(rot_90x2_y(_get_case_1_edges()))
        edges.extend(rot_90x1_z(_get_case_3_edges()))
    elif mtype == 38:
        edges.extend(rot_90x1_y(_get_case_3_edges()))
        edges.extend(rot_90x1_z(_get_case_1_edges()))
    elif mtype == 39:
        edges.extend(mirror_x(_get_case_27_edges()))
    elif mtype == 40:
        edges.extend(rot_90x2_y(_get_case_1_edges()))
        edges.extend(rot_90x2_z(_get_case_1_edges()))
    elif mtype == 41:
        edges.extend(_get_case_1_edges())
        edges.extend(rot_90x2_y(_get_case_1_edges()))
        edges.extend(rot_90x2_z(_get_case_1_edges()))
    elif mtype == 42:
        edges.extend(rot_90x1_y(_get_case_7_edges()))
    elif mtype == 43:
        edges.extend(rot_90x1_y(_get_case_23_edges()))
    elif mtype == 44:
        edges.extend(rot_90x1_x(_get_case_3_edges()))
        edges.extend(rot_90x2_y(_get_case_1_edges()))
    elif mtype == 45:
        edges.extend(rot_90x1_z(_get_case_7_edges()))
        edges.extend(rot_90x2_y(_get_case_1_edges()))
    elif mtype == 46:
        edges.extend(rot_90x3_z(_get_case_27_edges()))
    elif mtype == 47:
        edges.extend(reverse_edges(rot_90x2_x(_get_case_7_edges())))
    elif mtype == 48:
        edges.extend(rot_90x2_y(_get_case_3_edges()))
    elif mtype == 49:
        edges.extend(rot_90x3_x(_get_case_7_edges()))
    elif mtype == 50:
        edges.extend(rot_90x3_y(rot_90x3_x(_get_case_7_edges())))
    elif mtype == 51:
        edges.extend(rot_90x3_x(_get_case_15_edges()))
    elif mtype == 52:
        edges.extend(rot_90x2_y(_get_case_3_edges()))
        edges.extend(rot_90x1_z(_get_case_1_edges()))
    elif mtype == 53:
        edges.extend(rot_90x3_y(_get_case_27_edges()))
    elif mtype == 54:
        edges.extend(rot_90x3_y(rot_90x3_x(_get_case_7_edges())))
        edges.extend(rot_90x1_z(_get_case_1_edges()))
    elif mtype == 55:
        edges.extend(reverse_edges(rot_90x2_y(rot_90x1_x(_get_case_7_edges()))))
    elif mtype == 56:
        edges.extend(rot_90x2_z(_get_case_1_edges()))
        edges.extend(rot_90x2_y(_get_case_3_edges()))
    elif mtype == 57:
        edges.extend(rot_90x2_z(_get_case_1_edges()))
        edges.extend(rot_90x3_x(_get_case_7_edges()))
    elif mtype == 58:
        edges.extend(rot_90x1_y(mirror_x(_get_case_27_edges())))
    elif mtype == 59:
        edges.extend(reverse_edges(rot_90x1_x(rot_90x1_z(_get_case_7_edges()))))
    elif mtype == 60:
        edges.extend(rot_90x2_y(_get_case_3_edges()))
        edges.extend(rot_90x1_x(_get_case_3_edges()))
    elif mtype == 61:
        edges.extend(reverse_edges(rot_90x2_x(_get_case_3_edges())))
        edges.extend(reverse_edges(rot_90x1_y(_get_case_1_edges())))
    elif mtype == 62:
        edges.extend(reverse_edges(rot_90x2_x(_get_case_3_edges())))
        edges.extend(reverse_edges(_get_case_1_edges()))
    elif mtype == 63:
        edges.extend(reverse_edges(rot_90x2_x(_get_case_3_edges())))
        edges.extend(reverse_edges(_get_case_1_edges()))
    elif mtype == 64:
        edges.extend(rot_90x2_x(_get_case_1_edges()))
    elif mtype == 65:
        edges.extend(_get_case_1_edges())
        edges.extend(rot_90x2_x(_get_case_1_edges()))
    elif mtype == 66:
        edges.extend(rot_90x1_y(_get_case_1_edges()))
        edges.extend(rot_90x2_x(_get_case_1_edges()))
    elif mtype == 67:
        edges.extend(_get_case_3_edges())
        edges.extend(rot_90x2_x(_get_case_1_edges()))
    elif mtype == 68:
        edges.extend(rot_90x3_y(rot_90x2_z(_get_case_3_edges())))
    elif mtype == 69:
        edges.extend(rot_90x2_x(rot_90x3_y(_get_case_7_edges())))
    elif mtype == 70:
        edges.extend(rot_90x3_y(rot_90x1_x(_get_case_3_edges())))
        edges.extend(rot_90x1_y(_get_case_1_edges()))
    elif mtype == 71:
        edges.extend(rot_90x1_z(_get_case_27_edges()))
    elif mtype == 72:
        edges.extend(rot_90x2_x(_get_case_1_edges()))
        edges.extend(rot_90x2_z(_get_case_1_edges()))
    elif mtype == 73:
        edges.extend(rot_90x2_x(_get_case_1_edges()))
        edges.extend(rot_90x2_z(_get_case_1_edges()))
        edges.extend(_get_case_1_edges())
    elif mtype == 74:
        edges.extend(rot_90x2_x(_get_case_1_edges()))
        edges.extend(rot_90x3_z(_get_case_3_edges()))
    elif mtype == 75:
        edges.extend(rot_90x2_x(_get_case_1_edges()))
        edges.extend(rot_90x3_z(_get_case_7_edges()))
    elif mtype == 76:
        edges.extend(rot_90x1_x(_get_case_7_edges()))
    elif mtype == 77:
        edges.extend(rot_90x1_x(_get_case_23_edges()))
    elif mtype == 78:
        edges.extend(mirror_y(_get_case_27_edges()))
    elif mtype == 79:
        edges.extend(reverse_edges(rot_90x2_y(_get_case_7_edges())))
    elif mtype == 80:
        edges.extend(reverse_edges(rot_90x2_y(_get_case_7_edges())))


    vertex_data = [_generate_triangle(ed[0], ed[1], ed[2], size/2) for ed in edges]
    vertex_data = reduce(list.__add__, vertex_data)
    return vertex_data

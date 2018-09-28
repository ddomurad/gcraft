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


def data_to_mesh_type(data):
    bin_data = [d > 0 for d in data]
    return sum([2**i for (i, b) in enumerate(bin_data) if b > 0])


def _get_corner_vec(c, s):
    x = s if (0x01 & c) > 0 else -s
    y = s if (0x02 & c) > 0 else -s
    z = s if (0x04 & c) > 0 else -s
    return [x, y, z]


def _generate_triangle(A, B, C, offset, s):
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

    v3_add_self(c_a, offset)
    v3_add_self(c_b, offset)
    v3_add_self(c_c, offset)

    return reduce(list.__add__, [c_a, c_b, c_c])


ROT_90X1_X_MAP = {0: 2, 1: 3, 2: 6, 3: 7, 4: 0, 5: 1, 6: 4, 7: 5}
ROT_90X3_X_MAP = {0: 4, 1: 5, 2: 0, 3: 1, 4: 6, 5: 7, 6: 2, 7: 3}

ROT_90X1_Y_MAP = {0: 1, 1: 5, 2: 3, 3: 7, 4: 0, 5: 4, 6: 2, 7: 6}
ROT_90X3_Y_MAP = {0: 4, 1: 0, 2: 6, 3: 2, 4: 5, 5: 1, 6: 7, 7: 3}

ROT_90X1_Z_MAP = {0: 2, 1: 0, 2: 3, 3: 1, 4: 6, 5: 4, 6: 7, 7: 5}
ROT_90X3_Z_MAP = {0: 1, 1: 3, 2: 0, 3: 2, 4: 5, 5: 7, 6: 4, 7: 6}


def _apply_map_to_edges(edges, rot_map):
    return [[(rot_map[ed[0]], rot_map[ed[1]]) for ed in edge] for edge in edges]


def _apply_map_to_data(data, rot_map):
    return [data[rot_map[i]] for i in range(8)]


def reverse_edges(edges):
    return [list(reversed(e)) for e in edges]


EDGE_CASES = {
    1: lambda: [[(0, 1), (0, 2), (0, 4)]],
    3: lambda: [[(0, 4), (1, 5), (1, 3)], [(0, 4), (1, 3), (0, 2)]],
    7: lambda: [[(0, 4), (1, 5), (1, 3)], [(0, 4), (1, 3), (2, 3)], [(0, 4), (2, 3), (2, 6)]],
    9: lambda: [[(0, 1), (0, 2), (0, 4)], [(1, 3), (3, 7), (2, 3)]],
    15: lambda: [[(0, 4), (3, 7), (2, 6)], [(0, 4), (1, 5), (3, 7)]],
    23: lambda: [[(4, 5), (1, 5), (4, 6)], [(4, 6), (1, 5), (1, 3)], [(4, 6), (1, 3), (2, 6)], [(2, 6), (1, 3), (2, 3)]],
    27: lambda: [[(4, 5), (1, 5), (4, 6)], [(4, 6), (1, 5), (0, 2)], [(3, 7), (0, 2), (1, 5)], [(0, 2), (3, 7), (2, 3)]],
    73: lambda: [[(0, 1), (0, 2), (0, 4)], [(3, 7), (2, 3), (1, 3)], [(6, 7), (4, 6), (2, 6)]],
    105: lambda: [[(0, 1), (0, 2), (0, 4)], [(4, 5), (5, 7), (1, 5)], [(3, 7), (2, 3), (1, 3)], [(6, 7), (4, 6), (2, 6)]],
    129: lambda: [[(0, 1), (0, 2), (0, 4)], [(6, 7), (3, 7), (5, 7)]],
    131: lambda: [[(0, 4), (1, 5), (1, 3)], [(0, 4), (1, 3), (0, 2)], [(6, 7), (3, 7), (5, 7)]],
    135: lambda: [[(0, 4), (1, 5), (1, 3)], [(0, 4), (1, 3), (2, 3)], [(0, 4), (2, 3), (2, 6)], [(6, 7), (3, 7), (5, 7)]],
    177: lambda: [[(0, 1), (0, 2), (4, 6)], [(0, 1), (4, 6), (3, 7)], [(4, 6), (6, 7), (3, 7)], [(0, 1), (3, 7), (1, 5)]],
    195: lambda: [[(0, 4), (1, 5), (1, 3)], [(0, 4), (1, 3), (0, 2)], [(2, 6), (3, 7), (5, 7)], [(5, 7), (4, 6), (2, 6)]]
}

EDGE_TEMPLATE_DATA = {
    1: lambda: [1, 0, 0, 0, 0, 0, 0, 0],
    3: lambda: [1, 1, 0, 0, 0, 0, 0, 0],
    7: lambda: [1, 1, 1, 0, 0, 0, 0, 0],
    9: lambda: [1, 0, 0, 1, 0, 0, 0, 0],
    15: lambda: [1, 1, 1, 1, 0, 0, 0, 0],
    23: lambda: [1, 1, 1, 0, 1, 0, 0, 0],
    27: lambda: [1, 1, 0, 1, 1, 0, 0, 0],
    73: lambda: [1, 0, 0, 1, 0, 0, 1, 0],
    105: lambda: [1, 0, 0, 1, 0, 1, 1, 0],
    129: lambda: [1, 0, 0, 0, 0, 0, 0, 1],
    131: lambda: [1, 1, 0, 0, 0, 0, 0, 1],
    135: lambda: [1, 1, 1, 0, 0, 0, 0, 1],
    177: lambda: [1, 0, 0, 0, 1, 1, 0, 1],
    195: lambda: [1, 1, 0, 0, 0, 0, 1, 1]
}

CORNERS_NUMBER_CASE_MAP = {1: [1], 2: [3, 9, 129], 3: [7, 73, 131], 4: [15, 23, 27, 105, 135, 177, 195]}


def find_rotation_for_case(data, case_number):
    mtype = data_to_mesh_type(data)

    tmp_edges = EDGE_CASES[case_number]()
    tmp_data = EDGE_TEMPLATE_DATA[case_number]()
    tmp_case = data_to_mesh_type(tmp_data)

    if mtype == tmp_case:
        return tmp_edges

    for rx in range(4):
        tmp_edges = _apply_map_to_edges(tmp_edges, ROT_90X1_X_MAP)
        tmp_data = _apply_map_to_data(tmp_data, ROT_90X3_X_MAP)
        tmp_case = data_to_mesh_type(tmp_data)

        if mtype == tmp_case:
            return tmp_edges

        for ry in range(4):
            tmp_edges = _apply_map_to_edges(tmp_edges, ROT_90X1_Y_MAP)
            tmp_data = _apply_map_to_data(tmp_data, ROT_90X3_Y_MAP)
            tmp_case = data_to_mesh_type(tmp_data)

            if mtype == tmp_case:
                return tmp_edges

            for rz in range(4):
                tmp_edges = _apply_map_to_edges(tmp_edges, ROT_90X1_Z_MAP)
                tmp_data = _apply_map_to_data(tmp_data, ROT_90X3_Z_MAP)
                tmp_case = data_to_mesh_type(tmp_data)

                if mtype == tmp_case:
                    return tmp_edges

    return None


def find_case(data):
    corners_number = sum([1 for d in data if d > 0])
    if corners_number > 4:
        rev_data = [d*-1 for d in data]
        sup_corners_number = 8 - corners_number
        optional_cases = CORNERS_NUMBER_CASE_MAP[sup_corners_number]
        for case in optional_cases:
            result = find_rotation_for_case(rev_data, case)
            if result is not None:
                return reverse_edges(result)

    optional_cases = CORNERS_NUMBER_CASE_MAP[corners_number]
    for case in optional_cases:
        result = find_rotation_for_case(data, case)
        if result is not None:
           return result

    return None


def generate_case(case):
    if case == 0 or case == 255:
        return None

    data = [
        1 if (case & 1) else -1,
        1 if (case & 2) else -1,
        1 if (case & 4) else -1,
        1 if (case & 8) else -1,
        1 if (case & 16) else -1,
        1 if (case & 32) else -1,
        1 if (case & 64) else -1,
        1 if (case & 128) else -1
    ]

    corners_number = sum([1 for d in data if d > 0])
    if corners_number > 4:
        rev_data = [d*-1 for d in data]
        sup_corners_number = 8 - corners_number
        optional_cases = CORNERS_NUMBER_CASE_MAP[sup_corners_number]
        for case in optional_cases:
            result = find_rotation_for_case(rev_data, case)
            if result is not None:
                return reverse_edges(result)

    optional_cases = CORNERS_NUMBER_CASE_MAP[corners_number]
    for case in optional_cases:
        result = find_rotation_for_case(data, case)
        if result is not None:
           return result

    return None


def interpolate_cuboid_mesh(edges, offset, size):
    if edges is None:
        return []

    vertex_data = [_generate_triangle(ed[0], ed[1], ed[2], offset, size/2) for ed in edges]
    vertex_data = reduce(list.__add__, vertex_data)
    return vertex_data


def generate_vertex_cache():
    vertex_cache = {}
    for i in range(256):
        vertex_cache[i] = generate_case(i)

    return vertex_cache

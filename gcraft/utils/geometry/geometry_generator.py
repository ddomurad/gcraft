from functools import reduce
from OpenGL.GL import *
from gcraft.utils.geometry.mesh_geometry import MeshGeometry


class Face:
    def __init__(self):
        self.vertices = [[0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0]]
        self.normals = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.texture = [[0, 0], [0, 1], [1, 1], [1, 0]]
        self.indices = [0, 1, 2, 0, 2, 3]

    def get_vertex_data(self):
        out_data = []
        for i in range(len(self.vertices)):
            out_data.extend(self.vertices[i])
            out_data.extend(self.normals[i])
            out_data.extend(self.texture[i])
        return out_data

    def get_indices(self, offset):
        return [i+offset for i in self.indices]


def generate_cube_geometry(size, texture_rec):
    sx = size[0] / 2.0
    sy = size[1] / 2.0
    sz = size[2] / 2.0

    faces = [Face() for _ in range(6)]
    faces[0].vertices = [[-sx, -sy, -sz], [-sx,  sy, -sz], [ sx,  sy, -sz], [ sx, -sy, -sz]]
    faces[1].vertices = [[ sx, -sy, sz],  [ sx,  sy,  sz], [-sx,  sy,  sz], [-sx, -sy,  sz]]
    faces[2].vertices = [[ sx, -sy, -sz], [ sx,  sy, -sz], [ sx,  sy,  sz], [ sx, -sy,  sz]]
    faces[3].vertices = [[-sx, -sy,  sz], [-sx,  sy,  sz], [-sx,  sy, -sz], [-sx, -sy, -sz]]
    faces[4].vertices = [[-sx,  sy, -sz], [-sx,  sy,  sz], [ sx,  sy,  sz], [ sx,  sy, -sz]]
    faces[5].vertices = [[-sx, -sy,  sz], [-sx, -sy, -sz], [ sx, -sy, -sz], [ sx, -sy,  sz]]

    faces[0].normals = [[0, 0, -1], [0, 0, -1], [0, 0, -1], [0, 0, -1]]
    faces[1].normals = [[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]]
    faces[2].normals = [[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0]]
    faces[3].normals = [[-1, 0, 0], [-1, 0, 0], [-1, 0, 0], [-1, 0, 0]]
    faces[4].normals = [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]]
    faces[5].normals = [[0, -1, 0], [0, -1, 0], [0, -1, 0], [0, -1, 0]]

    uv_left = texture_rec[0][0]
    uv_bottom = texture_rec[0][1]
    uv_right = texture_rec[1][0]
    uv_top = texture_rec[1][1]

    for face in faces:
        face.texture = [[uv_left, uv_top], [uv_left, uv_bottom], [uv_right, uv_bottom], [uv_right, uv_top]]

    vertex_data = reduce(list.__add__, [face.get_vertex_data() for face in faces])

    vertex_metadata = [("v_pos", 3), ("v_normal", 3), ("uv_0", 2)]
    index_data = []
    index_offset = 0
    for face in faces:
        index_data.extend(face.get_indices(index_offset))
        index_offset += 4

    return MeshGeometry(GL_TRIANGLES, vertex_data, vertex_metadata, index_data, 6)


def generate_cube_frame_geometry(size):
    sx = size[0] / 2.0
    sy = size[1] / 2.0
    sz = size[2] / 2.0

    p0 = [-sx, -sy, -sz]
    p1 = [sx,  -sy, -sz]
    p2 = [-sx, sy, -sz]
    p3 = [sx, sy, -sz]
    p4 = [-sx, -sy, sz]
    p5 = [sx, -sy, sz]
    p6 = [-sx, sy, sz]
    p7 = [sx, sy, sz]

    vertex_data = [p0, p1, p1, p5, p5, p4, p4, p0, p0, p2, p1, p3, p5, p7, p4, p6, p2, p3, p3, p7, p7, p6, p6, p2]
    vertex_data = reduce(list.__add__, vertex_data)

    return MeshGeometry(GL_LINES, vertex_data, [("v_pos", 3)], None, len(vertex_data)/3)


def generate_gird_geometry(size, segments):
    dx = size[0] / segments[0]
    dz = size[1] / segments[1]

    start_x = -segments[0] * dx/2
    start_z = -segments[1] * dz/2

    end_x = segments[0] * dx/2
    end_z = segments[1] * dz/2

    vertex_data = []

    for i in range(segments[0]):
        vertex_data.extend([start_x + i*dx, 0, start_z])
        vertex_data.extend([start_x + i * dx, 0, end_z])

    for i in range(segments[1]):
        vertex_data.extend([start_x, 0, start_z + i*dz])
        vertex_data.extend([end_x, 0, start_z + i*dz])

    vertex_metadata = [("v_pos", 3)]
    return MeshGeometry(GL_LINES, vertex_data, vertex_metadata, None, (segments[0] + segments[1])*2)

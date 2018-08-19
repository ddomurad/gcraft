from functools import reduce
from OpenGL.GL import *
from gcraft.utils.mesh_geometry import MeshGeometry
from gcraft.utils.vector_ops import *


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
    index_data = [i for i in range(int(len(vertex_data)/3))]
    return MeshGeometry(GL_LINES, vertex_data, vertex_metadata, index_data, (segments[0] + segments[1])*2)


def remove_indices_from_mesh(geometry: MeshGeometry):
    new_vertex_data = []
    vertex_stride = sum([d[1] for d in geometry.vertex_metadata])

    if not geometry.index_data:
        return

    for index in geometry.index_data:
        new_vertex_data.extend(
            geometry.vertex_data[index*vertex_stride: (index+1)*vertex_stride])

    geometry.vertex_data = new_vertex_data
    geometry.vertex_count = len(new_vertex_data)//vertex_stride
    geometry.index_data = None


def add_tangents_data(geometry: MeshGeometry):
    if "v_tangent" in geometry.vertex_metadata:
        raise ValueError("Mesh already contains tangents")

    if geometry.index_data is None:
        raise ValueError("Vertex tangent calculation not supported for not indexed mesh")

    if geometry.primitive_type != GL_TRIANGLES:
        raise ValueError("Vertex tangent calculation not supported for other primitives than triangles")

    tangent_work_data = list([[0, 0, 0] for i in range(geometry.vertex_count)])
    vertex_stride = geometry.get_vertex_stride()

    # vertex pos offset
    vpo = geometry.get_data_offset("v_pos")
    # vertex uv offset
    vuo =  geometry.get_data_offset("uv_0")

    if vuo is None:
        raise ValueError("Vertex tangent calculation not supported without uv coordinates")

    for i in range(len(geometry.index_data)//3):
        i0 = geometry.index_data[0 + i * 3]
        i1 = geometry.index_data[1 + i * 3]
        i2 = geometry.index_data[2 + i * 3]

        v0 = geometry.vertex_data[i0 * vertex_stride: (i0 + 1) * vertex_stride]
        v1 = geometry.vertex_data[i1 * vertex_stride: (i1 + 1) * vertex_stride]
        v2 = geometry.vertex_data[i2 * vertex_stride: (i2 + 1) * vertex_stride]

        e1 = v3_sub(v1[vpo:vpo+3], v0[vpo:vpo+3])
        e2 = v3_sub(v2[vpo:vpo+3], v0[vpo:vpo+3])

        delta_u1 = v1[vuo] - v0[vuo]
        delta_v1 = v1[vuo + 1] - v0[vuo + 1]

        delta_u2 = v2[vuo] - v0[vuo]
        delta_v2 = v2[vuo + 1] - v0[vuo + 1]

        f = 1/(delta_u1*delta_v2 - delta_u2*delta_v1)

        tx = f * (delta_v2 * e1[0] - delta_u1 * e2[0])
        ty = f * (delta_v2 * e1[1] - delta_u1 * e2[1])
        tz = f * (delta_v2 * e1[1] - delta_u1 * e2[2])

        tangent = [tx, ty, tz]
        v3_add_self(tangent_work_data[i0], tangent)
        v3_add_self(tangent_work_data[i1], tangent)
        v3_add_self(tangent_work_data[i2], tangent)

    new_vertex_data = []

    for vi in range(geometry.vertex_count):
        tangent = tangent_work_data[vi]
        v3_normalize_self(tangent)

        new_vertex_data.extend(
            geometry.vertex_data[vi*vertex_stride:(vi+1)*vertex_stride])

        new_vertex_data.extend(tangent)

    geometry.vertex_data = new_vertex_data
    geometry.vertex_metadata.append(('v_tangent', 3))
from OpenGL.GL import *
from gcraft.utils.mesh_geometry import MeshGeometry
from gcraft.utils.vector_ops import *


def mod_vertex_data(geometry: MeshGeometry, data_tag, data_len, mod):

    if not geometry.contains_data(data_tag):
        return

    vertex_stride = geometry.get_vertex_stride()

    # data offset
    do1 = geometry.get_data_offset(data_tag)
    do2 = do1 + data_len

    for i in range(geometry.vertex_count):
        vs = i * vertex_stride
        ve = (i + 1) * vertex_stride
        v = geometry.vertex_data[vs:ve]
        v[do1:do2] = mod(v[do1:do2])
        geometry.vertex_data[vs:ve] = v


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
        return

    if geometry.index_data is None:
        raise ValueError("Vertex tangent calculation not supported for not indexed mesh")

    if geometry.primitive_type != GL_TRIANGLES:
        raise ValueError("Vertex tangent calculation not supported for other primitives than triangles")

    tangent_work_data = list([[0, 0, 0] for i in range(geometry.vertex_count)])
    vertex_stride = geometry.get_vertex_stride()

    # vertex pos offset
    vpo = geometry.get_data_offset("v_pos")
    # vertex uv offset
    vuo = geometry.get_data_offset("uv_0")

    if vuo is None:
        raise ValueError("Vertex tangent calculation not supported without uv coordinates")

    for i in range(len(geometry.index_data)//3):
        i0 = geometry.index_data[0 + i * 3]
        i1 = geometry.index_data[1 + i * 3]
        i2 = geometry.index_data[2 + i * 3]

        v0 = geometry.vertex_data[i0 * vertex_stride: (i0 + 1) * vertex_stride]
        v1 = geometry.vertex_data[i1 * vertex_stride: (i1 + 1) * vertex_stride]
        v2 = geometry.vertex_data[i2 * vertex_stride: (i2 + 1) * vertex_stride]

        e1 = v3_sub(v1[vpo:vpo + 3], v0[vpo:vpo + 3])
        e2 = v3_sub(v2[vpo:vpo + 3], v0[vpo:vpo + 3])

        delta_u1 = v1[vuo] - v0[vuo]
        delta_v1 = v1[vuo + 1] - v0[vuo + 1]

        delta_u2 = v2[vuo] - v0[vuo]
        delta_v2 = v2[vuo + 1] - v0[vuo + 1]

        f = 1/(delta_u1*delta_v2 - delta_u2*delta_v1)

        tx = f * (delta_v2 * e1[0] - delta_v1 * e2[0])
        ty = f * (delta_v2 * e1[1] - delta_v1 * e2[1])
        tz = f * (delta_v2 * e1[2] - delta_v1 * e2[2])

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


def add_normals_data(geometry: MeshGeometry):
    if "v_normals" in geometry.vertex_metadata:
        return

    if geometry.index_data is None:
        raise ValueError("Vertex tangent calculation not supported for not indexed mesh")

    if geometry.primitive_type != GL_TRIANGLES:
        raise ValueError("Vertex tangent calculation not supported for other primitives than triangles")

    normal_work_data = list([[0, 0, 0] for i in range(geometry.vertex_count)])
    normals_avg_count = [0]*geometry.vertex_count

    vertex_stride = geometry.get_vertex_stride()

    # vertex pos offset
    vpo = geometry.get_data_offset("v_pos")

    for i in range(len(geometry.index_data)//3):
        i0 = geometry.index_data[0 + i * 3]
        i1 = geometry.index_data[1 + i * 3]
        i2 = geometry.index_data[2 + i * 3]

        v0 = geometry.vertex_data[i0 * vertex_stride: (i0 + 1) * vertex_stride]
        v1 = geometry.vertex_data[i1 * vertex_stride: (i1 + 1) * vertex_stride]
        v2 = geometry.vertex_data[i2 * vertex_stride: (i2 + 1) * vertex_stride]

        e1 = v3_sub(v1[vpo:vpo + 3], v0[vpo:vpo + 3])
        e2 = v3_sub(v2[vpo:vpo + 3], v0[vpo:vpo + 3])

        normal = v3_cross(e1, e2)

        v3_add_self(normal_work_data[i0], normal)
        v3_add_self(normal_work_data[i1], normal)
        v3_add_self(normal_work_data[i2], normal)

        normals_avg_count[i0] += 1
        normals_avg_count[i1] += 1
        normals_avg_count[i2] += 1

    new_vertex_data = []

    for vi in range(geometry.vertex_count):
        normal = v3_div(normal_work_data[vi], normals_avg_count[vi])
        v3_normalize_self(normal)

        new_vertex_data.extend(
            geometry.vertex_data[vi*vertex_stride:(vi+1)*vertex_stride])

        new_vertex_data.extend(normal)

    geometry.vertex_data = new_vertex_data
    geometry.vertex_metadata.append(('v_normal', 3))

from OpenGL.GL import *
from os import path
import struct
import math

from gcraft.resources.resource_types import RT_MESH
from gcraft.resources.resource_loader import ResourceLoader, FileResourceLoader
from gcraft.resources.resource import Resource
from gcraft.resources.mesh import StaticMesh

from gcraft.utils.geometry.mesh_geometry import MeshGeometry
from gcraft.utils.geometry.geometry_generator import generate_cube_geometry
from gcraft.utils.geometry.geometry_generator import generate_cube_frame_geometry
from gcraft.utils.geometry.geometry_generator import generate_square_geometry


def _apply_mesh_ops(geometry: MeshGeometry, ops):
    for op in ops:
        op(geometry)


class DefaultMeshLoader(ResourceLoader):

    def can_load(self, r_id, r_type, params):
        return r_type == RT_MESH and (r_id == "default_cube" or r_id == "default_cube_frame" or r_id == "default_square")

    def load(self, r_id, params) -> Resource or None:
        if r_id == "default_cube":
            mesh_size = params.get("size") or [1, 1, 1]
            texture_rect = params.get("texture_rect") or [[0, 0], [1, 1]]
            return StaticMesh(r_id, generate_cube_geometry(mesh_size, texture_rect))
        elif r_id == "default_cube_frame":
            mesh_size = params.get("size") or [1, 1, 1]
            return StaticMesh(r_id, generate_cube_frame_geometry(mesh_size))
        elif r_id == "default_square":
            mesh_offset = params.get("offset") or [0, 0]
            mesh_size = params.get("size") or [1, 1]
            texture_rect = params.get("texture_rect") or [[0, 0], [1, 1]]

            return StaticMesh(r_id, generate_square_geometry(mesh_offset, mesh_size, texture_rect))

        return None


class StlFileMeshLoader(FileResourceLoader):
    def can_load(self, r_id, r_type, params):

        return r_type == RT_MESH and FileResourceLoader.can_load_file(r_id, params, ".stl")
        # return r_type == RT_MESH and isinstance(r_id, str) and r_id.endswith(".stl") and path.exists(r_id)

    def load(self, r_id, params) -> Resource:
        file_path = FileResourceLoader.get_file_name(r_id, params)

        with open(file_path, 'rb') as stl_file:
            stl_file.seek(80)
            faces_count, = struct.unpack('i', stl_file.read(4))

            vertex_data = []
            index_data = [i for i in range(faces_count*3)]
            vertex_metadata = [("v_pos", 3), ("v_normal", 3)]
            vertex_stride = 6

            for i in range(faces_count):
                normal_vector = [StlFileMeshLoader.remove_nan(f) for f in struct.unpack('fff', stl_file.read(12))]

                vertex_data.extend(StlFileMeshLoader.remove_nan(f) for f in struct.unpack('fff', stl_file.read(12)))
                vertex_data.extend(normal_vector[:])

                vertex_data.extend(StlFileMeshLoader.remove_nan(f) for f in struct.unpack('fff', stl_file.read(12)))
                vertex_data.extend(normal_vector[:])

                vertex_data.extend(StlFileMeshLoader.remove_nan(f) for f in struct.unpack('fff', stl_file.read(12)))
                vertex_data.extend(normal_vector[:])

                stl_file.read(2)

        return StaticMesh(r_id, MeshGeometry(GL_TRIANGLES, vertex_data, vertex_metadata, index_data,
                                             len(vertex_data)/vertex_stride))

    @staticmethod
    def remove_nan(v):
        if math.isnan(v):
            return 0
        return v


class PlyFileMeshLoader(ResourceLoader):
    def can_load(self, r_id, r_type, params):
        return r_type == RT_MESH and FileResourceLoader.can_load_file(r_id, params, ".ply")
        # return r_type == RT_MESH and isinstance(r_id, str) and r_id.endswith(".ply") and path.exists(r_id)

    def load(self, r_id, params) -> Resource or None:
        file_path = FileResourceLoader.get_file_name(r_id, params)
        with open(file_path, "r") as ply_file:
            ply_tag = ply_file.readline().strip()
            ply_format = ply_file.readline().strip()

            if ply_tag != "ply":
                raise ValueError("Invalid .ply file format")

            if ply_format != "format ascii 1.0":
                raise ValueError("Unsupported .ply file format")

            elements = {}
            ctx_element = None

            vertex_data = []
            index_data = []
            primitive_type = None

            vertex_data_order = ["x", "y", "z", "nx", "ny", "nz", "s", "t"]

            # TODO ADD FORMAT VALIDATION

            def read_header(words):
                global ctx_element

                if words[0] == "end_header":
                    return False

                elif words[0] == "element":
                    element_type = words[1]
                    ctx_element = {"type": element_type, "count": int(words[2]), "props": []}
                    elements[element_type] = ctx_element

                elif words[0] == "property":
                    if ctx_element["type"] == "vertex":
                        ctx_element["props"].append(words[2])
                    elif ctx_element["type"] == "face":
                        pass

                return True

            def read_vertex_data(words):
                vertex_line_data = [0.0]*len(elements["vertex"]["props"])
                for (pi, prop) in enumerate(elements["vertex"]["props"]):
                    vertex_line_data[vertex_data_order.index(prop)] = float(words[pi])

                vertex_data.extend(vertex_line_data)

            def read_primitive_type(words):
                vertex_per_face = int(words[0])
                if vertex_per_face == 3:
                    return GL_TRIANGLES
                elif vertex_per_face == 4:
                    return GL_QUADS

            def read_index_data(words):
                index_data.extend([int(ind) for ind in words[1:]])

            # read header
            while True:
                ply_line = ply_file.readline()
                if ply_file == "":
                    return None
                ply_words = ply_line.strip().split(" ")

                if len(ply_words) < 0:
                    continue

                if not read_header(ply_words):
                    break

            vertex_data_order = [f for f in vertex_data_order if f in elements["vertex"]["props"]]
            vertex_metadata = []

            if "x" in vertex_data_order:
                vertex_metadata.append(("v_pos", 3))
            if "nx" in vertex_data_order:
                vertex_metadata.append(("v_normal", 3))
            if "s" in vertex_data_order:
                vertex_metadata.append(("uv_0", 2))

            # read vertex data
            for vi in range(elements["vertex"]["count"]):
                ply_line = ply_file.readline()
                if ply_file == "":
                    return None
                ply_words = ply_line.strip().split(" ")

                read_vertex_data(ply_words)

            # read index data
            for i in range(elements["face"]["count"]):
                ply_line = ply_file.readline()
                if ply_file == "":
                    return None
                ply_words = ply_line.strip().split(" ")

                if primitive_type is None:
                    primitive_type = read_primitive_type(ply_words)
                read_index_data(ply_words)

            mesh_geometry = MeshGeometry(primitive_type, vertex_data, vertex_metadata, index_data, elements["vertex"]["count"])

            if "mesh_ops" in params:
                _apply_mesh_ops(mesh_geometry, params["mesh_ops"])

            return StaticMesh(r_id, mesh_geometry)


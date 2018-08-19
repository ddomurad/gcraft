from OpenGL.GL import *

from gcraft.resources.resource import Resource
from gcraft.resources.shader import Shader
from gcraft.resources.resource_types import *
from gcraft.utils.mesh_geometry import MeshGeometry
import gcraft.utils.state_manager as sm


class StaticMesh(Resource):
    def __init__(self, r_id, mesh_geometry: MeshGeometry):
        Resource.__init__(self, r_id, RT_MESH)

        self.primitive_type = mesh_geometry.primitive_type

        self.vertex_buffer = None
        self.vertex_metadata = []

        self.index_buffer = None
        self.ind_count = 0
        self.vertex_stride = 0

        if mesh_geometry.index_data is not None:
            self._set_index_data(mesh_geometry.index_data)

        self._set_vertex_data(mesh_geometry.vertex_data, mesh_geometry.vertex_metadata, mesh_geometry.vertex_count)

    def draw(self, shader: Shader):
        shader.use()

        sm.bind_array_buffer(self.vertex_buffer)
        if self.index_buffer is None:
            sm.bind_element_buffer(0)
        else:
            sm.bind_element_buffer(self.index_buffer)

        offset = 0
        for metadata in self.vertex_metadata:
            attrib = shader.get_attrib(metadata[0])
            if attrib != -1:
                sm.set_vertex_attrib_pointer(attrib, metadata[1], self.vertex_stride, offset)
                sm.enable_vertex_attrib(attrib)

            offset += metadata[1]*4

        if self.index_buffer is None:
            glDrawArrays(self.primitive_type, 0, self.vertex_count)
        else:
            glDrawElements(self.primitive_type, self.ind_count, GL_UNSIGNED_INT, None)

    def _set_index_data(self, index_data):
        self.index_buffer = glGenBuffers(1)
        self.ind_count = len(index_data)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.index_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(index_data) * 4,
                     (ctypes.c_uint * len(index_data))(*index_data), GL_STATIC_DRAW)

    def _set_vertex_data(self, vertex_data, vertex_metadata, vertex_count):
        self.vertex_buffer = glGenBuffers(1)
        self.vertex_metadata = vertex_metadata

        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, len(vertex_data) * 4,
                     (ctypes.c_float * len(vertex_data))(*vertex_data), GL_STATIC_DRAW)

        self.vertex_stride = sum(map(lambda m: m[1], vertex_metadata))*4
        self.vertex_count = vertex_count
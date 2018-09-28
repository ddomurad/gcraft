class MeshGeometry:
    def __init__(self, primitive_type, vertex_data, vertex_metadata, index_data, vertex_count):
        self.primitive_type = primitive_type
        self.vertex_data = vertex_data
        self.vertex_metadata = vertex_metadata
        self.index_data = index_data
        self.vertex_count = int(vertex_count)

    def contains_data(self, data_type):
        return any([md[0] == data_type for md in self.vertex_metadata])

    def get_vertex_stride(self):
        return sum([d[1] for d in self.vertex_metadata])

    def get_data_offset(self, data_type):
        offset = 0
        for md in self.vertex_metadata:
            if md[0] == data_type:
                return offset
            offset += md[1]

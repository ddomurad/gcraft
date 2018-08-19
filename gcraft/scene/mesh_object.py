from gcraft.resources.shader import Shader
from gcraft.resources.mesh import StaticMesh
from gcraft.scene.scene_object import SceneObject
from gcraft.scene.scene_object import Camera
from gcraft.scene.material import Material, BasicMaterial
from gcraft.scene.transformation import Transformation

import gcraft.utils.state_manager as sm

import numpy as np


class SimpleMeshObject(SceneObject):

    def __init__(self, mesh: StaticMesh, shader: Shader, material: Material = None):
        SceneObject.__init__(self)
        self.trans = Transformation()

        self.mesh = mesh
        self.shader = shader
        self.material = material if material is not None else BasicMaterial()
        self.textures = []

    def update(self, dt):
        pass

    def draw(self, camera: Camera):
        self.material.apply(self.shader)

        self.shader.set_uniform_matrix_4f("projection_view_matrix",
                                          np.matmul(self.trans.get_matrix(), camera.projection_view_matrix))

        self.shader.set_uniform_matrix_4f("normal_view_matrix",
                                          np.matrix.transpose(
                                              np.linalg.inv(self.trans.get_matrix())))

        if self.textures:
            self.shader.set_uniform_1i("textures_count", len(self.textures))
            for (i, texture) in enumerate(self.textures):
                if texture is not None:
                    texture.use(i, self.shader)
        else:
            sm.bind_2d_texture(0)
            self.shader.set_uniform_1i("textures_count", 0)

        self.mesh.draw(self.shader)

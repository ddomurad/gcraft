from OpenGL.GL import *

from gcraft.resources.resource import Resource
from gcraft.resources.shader import Shader
from gcraft.resources.resource_types import *

import gcraft.utils.state_manager as sm


class Texture(Resource):

    def __init__(self, r_id, texture_id):
        Resource.__init__(self, r_id, RT_TEXTURE)

        self.texture_id = texture_id

    def use(self, index, shader: Shader):
        shader.use()
        sm.activate_texture(GL_TEXTURE0 + index)
        sm.bind_2d_texture(self.texture_id)
        shader.set_uniform_1i("texture_" + str(index), index)

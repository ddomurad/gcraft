from OpenGL.GL import *

from gcraft.resources.resource import Resource
from gcraft.resources.shader import Shader
from gcraft.resources.resource_types import *

import gcraft.utils.state_manager as sm


class Texture(Resource):
    def __init__(self, r_id, texture_size, texture_data):
        Resource.__init__(self, r_id, RT_TEXTURE)

        self.texture_id = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 4)

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_size[0], texture_size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    def use(self, index, shader: Shader):
        shader.use()
        sm.activate_texture(GL_TEXTURE0 + index)
        sm.bind_2d_texture(self.texture_id)
        shader.set_uniform_1i("texture_" + str(index), index)

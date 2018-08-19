from OpenGL.GL import *

from gcraft.resources.resource import Resource
from gcraft.resources.shader import Shader
from gcraft.resources.resource_types import *
import gcraft.utils.state_manager as sm


class Texture(Resource):
    def __init__(self, r_id, texture_size, texture_data):
        Resource.__init__(self, r_id, RT_TEXTURE)

        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        glTexImage2D(GL_TEXTURE_2D, 0, 3, texture_size[0], texture_size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        glGenerateMipmap(GL_TEXTURE_2D)
        # glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

    def use(self, index, shader: Shader):
        shader.use()
        sm.activate_texture(GL_TEXTURE0 + index)
        sm.bind_2d_texture(self.texture_id)
        shader.set_uniform_1i("texture_" + str(index), index)

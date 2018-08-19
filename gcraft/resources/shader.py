from OpenGL.GL import *
from OpenGL.GL import shaders

from gcraft.resources.resource import Resource
from gcraft.resources.resource_types import *
import gcraft.utils.state_manager as sm


class Shader(Resource):
    def __init__(self, r_id, vs, fs):
        Resource.__init__(self, r_id, RT_SHADER_PROGRAM)

        v_shader = shaders.compileShader(vs, GL_VERTEX_SHADER)
        f_shader = shaders.compileShader(fs, GL_FRAGMENT_SHADER)

        self.shader = shaders.compileProgram(v_shader, f_shader)
        self.uniforms = {}
        self.attributes = {}

    def use(self):
        sm.use_program(self.shader)

    def get_attrib(self, attrib_name):
        if attrib_name in self.attributes:
            return self.attributes[attrib_name]

        self.attributes[attrib_name] = glGetAttribLocation(self.shader, attrib_name)
        return self.attributes[attrib_name]

    def set_uniform_matrix_4f(self, uniform_name, mat):
        uniform = self.get_uniform(uniform_name)
        if uniform != -1:
            glUniformMatrix4fv(uniform, 1, GL_FALSE, mat)

    # def set_uniform_1iv(self, uniform_name, index, val):
    #     uniform = self.get_uniform(uniform_name)
    #     if uniform != -1:d
    #         sm.set_uniform_1iv(self.shader, uniform, index, val)

    def set_uniform_1i(self, uniform_name, val):
        uniform = self.get_uniform(uniform_name)
        if uniform != -1:
            sm.set_uniform_1i(self.shader, uniform, val)

    def set_uniform_1f(self, uniform_name, val):
        uniform = self.get_uniform(uniform_name)
        if uniform != -1:
            sm.set_uniform_1f(self.shader, uniform, val)

    def set_uniform_3f(self, uniform_name, val):
        uniform = self.get_uniform(uniform_name)
        if uniform != -1:
            sm.set_uniform_3f(self.shader, uniform, val)

    def set_uniform_4f(self, uniform_name, val):
        uniform = self.get_uniform(uniform_name)
        if uniform != -1:
            sm.set_uniform_4f(self.shader, uniform, val)

    def get_uniform(self, uniform_name):
        if uniform_name in self.uniforms:
            return self.uniforms[uniform_name]

        self.uniforms[uniform_name] = glGetUniformLocation(self.shader, uniform_name)
        return self.uniforms[uniform_name]

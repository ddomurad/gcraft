from OpenGL.GL import *
import gcraft.utils.state_manager as sm


class RenderBuffer:

    def __init__(self, buffer_id, texture_id):
        self.texture_id = texture_id
        self.buffer_id = buffer_id

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.buffer_id)

    def release(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        sm.bind_2d_texture(0)

        glDeleteFramebuffers(self.buffer_id)
        glDeleteTextures(self.texture_id)

    @staticmethod
    def bind_screen():
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    @staticmethod
    def create(texture_size: (int, int)):

        frame_buffer_id = glGenFramebuffers(1)
        texture_id = glGenTextures(1)

        glBindFramebuffer(GL_FRAMEBUFFER, frame_buffer_id)
        sm.bind_2d_texture(texture_id)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_size[0], texture_size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, texture_id, 0)

        buffer = RenderBuffer(frame_buffer_id, texture_id)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        sm.bind_2d_texture(0)

        return buffer

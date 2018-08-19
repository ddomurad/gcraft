from OpenGL.GL import *

_management_off = True
_last_program = None
_last_array_buffer = None
_last_element_buffer = None
_enabled_attributes = []
_last_vertex_attributes_setups = {}
_last_shader_uniforms = {}
_last_2d_texture = None
_active_textures = []

_gl_calls = 0


def get_gl_calls():
    return _gl_calls


def reset():
    global _last_program
    global _last_array_buffer
    global _last_element_buffer
    global _enabled_attributes
    global _last_vertex_attributes_setups
    global _last_shader_uniforms
    global _last_2d_texture
    global _active_textures
    global _gl_calls

    _last_program = None
    _last_array_buffer = None
    _last_element_buffer = None
    _enabled_attributes = []
    _last_vertex_attributes_setups = {}
    _last_shader_uniforms = {}
    _last_2d_texture = None
    _active_textures = []

    _gl_calls = 0


def use_program(program):
    global _last_program
    global _gl_calls

    if _last_program != program or _management_off:
        _last_program = program
        glUseProgram(_last_program)
        _gl_calls += 1


def bind_array_buffer(buffer):
    global _last_array_buffer
    global _gl_calls

    if _last_array_buffer != buffer or _management_off:
        _last_array_buffer = buffer
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        _gl_calls += 1


def bind_element_buffer(buffer):
    global _last_element_buffer
    global _gl_calls

    if _last_element_buffer != buffer or _management_off:
        _last_element_buffer = buffer
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer)
        _gl_calls += 1


def enable_vertex_attrib(attrib):
    global _last_vertex_attributes_setups
    global _enabled_attributes
    global _gl_calls

    if attrib not in _enabled_attributes or _management_off:
        _enabled_attributes.append(attrib)
        glEnableVertexAttribArray(attrib)
        _last_vertex_attributes_setups = {}
        _gl_calls += 1


def set_vertex_attrib_pointer(attrib, size, stride, offset):
    global _last_vertex_attributes_setups
    global _gl_calls

    val = (size, stride, offset)
    if attrib not in _last_vertex_attributes_setups or _management_off:
        _last_vertex_attributes_setups[attrib] = val
        glVertexAttribPointer(attrib, size, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(offset))
        _gl_calls += 1
    else:
        if _last_vertex_attributes_setups[attrib] != val:
            _last_vertex_attributes_setups[attrib] = val
            glVertexAttribPointer(attrib, size, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(offset))
            _gl_calls += 1


def set_uniform_1f(shader, uniform, val):
    global _last_shader_uniforms
    global _gl_calls

    key = (shader, uniform)

    if key not in _last_shader_uniforms or _management_off:
        _last_shader_uniforms[key] = val
        glUniform1f(uniform, val)
        _gl_calls += 1
    else:
        if _last_shader_uniforms[key] != val:
            _last_shader_uniforms[key] = val
            glUniform1f(uniform, val)
            _gl_calls += 1


def set_uniform_3f(shader, uniform, val):
    global _last_shader_uniforms
    global _gl_calls

    key = (shader, uniform)
    tuple_val = tuple(val)

    if key not in _last_shader_uniforms or _management_off:
        _last_shader_uniforms[key] = tuple_val
        glUniform3f(uniform, val[0], val[1], val[2])
        _gl_calls += 1
    else:
        if _last_shader_uniforms[key] != tuple_val:
            _last_shader_uniforms[key] = tuple_val
            glUniform3f(uniform, val[0], val[1], val[2])
            _gl_calls += 1


def set_uniform_4f(shader, uniform, val):
    global _last_shader_uniforms
    global _gl_calls

    key = (shader, uniform)
    tuple_val = tuple(val)

    if key not in _last_shader_uniforms or _management_off:
        _last_shader_uniforms[key] = tuple_val
        glUniform4f(uniform, val[0], val[1], val[2], val[3])
        _gl_calls += 1
    else:
        if _last_shader_uniforms[key] != tuple_val:
            _last_shader_uniforms[key] = tuple_val
            glUniform4f(uniform, val[0], val[1], val[2], val[3])
            _gl_calls += 1


def set_uniform_1iv(shader, uniform, index, val):
    global _last_shader_uniforms
    global _gl_calls

    key = (shader, uniform, index)

    if key not in _last_shader_uniforms or _management_off:
        _last_shader_uniforms[key] = val
        glUniform1iv(uniform, index, val)
        _gl_calls += 1
    else:
        if _last_shader_uniforms[key] != val:
            _last_shader_uniforms[key] = val
            glUniform1iv(uniform, index, val)
            _gl_calls += 1


def set_uniform_1i(shader, uniform, val):
    global _last_shader_uniforms
    global _gl_calls

    key = (shader, uniform)

    if key not in _last_shader_uniforms or _management_off:
        _last_shader_uniforms[key] = val
        glUniform1i(uniform, val)
        _gl_calls += 1
    else:
        if _last_shader_uniforms[key] != val:
            _last_shader_uniforms[key] = val
            glUniform1i(uniform, val)
            _gl_calls += 1


def activate_texture(index):
    global _gl_calls

    if index not in _active_textures:
        _active_textures.append(index)
        glActiveTexture(index)
        _gl_calls += 1


def bind_2d_texture(texture):
    global _last_2d_texture
    global _gl_calls

    if _last_2d_texture != texture or _management_off:
        _last_2d_texture = texture
        glBindTexture(GL_TEXTURE_2D, texture)
        _gl_calls += 1

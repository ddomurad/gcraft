from gcraft.resources.shader import Shader


class Material:
    def apply(self, shader: Shader):
        pass


class BasicMaterial(Material):
    def __init__(self):
        Material.__init__(self)
        self.difusse_color = [1, 1, 1, 1]

    def apply(self, shader: Shader):
        shader.use()
        shader.set_uniform_4f("difusse_color", self.difusse_color)

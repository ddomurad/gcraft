from os import path
from PIL import Image

from OpenGL.GL import *
from gcraft.resources.resource import Resource
from gcraft.resources.resource_loader import ResourceLoader
from gcraft.resources.resource_types import RT_TEXTURE
from gcraft.resources.texture import Texture


class TextureFileLoader(ResourceLoader):
    def can_load(self, r_id, r_type):
        return r_type == RT_TEXTURE and path.exists(r_id)

    def load(self, r_id, params) -> Resource:
        if not path.exists(r_id):
            return None

        image = Image.open(r_id)
        image_data = image.tobytes("raw")

        texture = Texture(r_id, image.size, image_data)

        glBindTexture(GL_TEXTURE_2D, texture.texture_id)

        mipmaps = "mipmaps" in params and params["mipmaps"]

        if mipmaps:
            glGenerateMipmap(GL_TEXTURE_2D)

        if "filter" in params and params["filter"] == "linear":
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR if mipmaps else GL_LINEAR)
        else:
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                            GL_NEAREST_MIPMAP_NEAREST if mipmaps else GL_NEAREST)

        return texture

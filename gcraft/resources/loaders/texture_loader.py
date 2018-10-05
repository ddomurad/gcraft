from PIL import Image
import numpy as np

from OpenGL.GL import *
from gcraft.resources.resource import Resource
from gcraft.resources.resource_loader import FileResourceLoader
from gcraft.resources.resource_types import RT_TEXTURE
from gcraft.resources.texture import Texture


class TextureFileLoader(FileResourceLoader):
    def can_load(self, r_id, r_type, params):
        return r_type == RT_TEXTURE and FileResourceLoader.can_load_file(r_id, params)

    def load(self, r_id, params) -> Resource:
        file_path = FileResourceLoader.get_file_name(r_id, params)

        image = Image.open(file_path)

        image_data = image.tobytes("raw", "RGBA") if 'A' in image.getbands() else image.tobytes("raw", "RGBX")

        print(image.info)
        texture = Texture(r_id, image.size, image_data)
        image.close()

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

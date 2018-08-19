from gcraft.resources.resource import Resource
from gcraft.resources.resource_loader import ResourceLoader
from gcraft.resources.resource_types import RT_TEXTURE
from gcraft.resources.texture import Texture

from os import path
from PIL import Image


class TextureFileLoader(ResourceLoader):
    def can_load(self, r_id, r_type):
        return r_type == RT_TEXTURE and path.exists(r_id)

    def load(self, r_id) -> Resource:
        if not path.exists(r_id):
            return None

        image = Image.open(r_id)
        image_data = image.tobytes("raw")

        return Texture(r_id, image.size, image_data)

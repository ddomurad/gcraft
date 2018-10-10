from gcraft.resources.resources_manager import ResourcesManager
from gcraft.resources.texture import Texture

import gcraft.resources.resource_types as RT
from gcraft.scene.mesh_object import SimpleMeshObject


class SceneFactory:
    def __init__(self, resource_manager: ResourcesManager):
        self.resource_manager = resource_manager

    def create_sprite_2d(self, texture) -> SimpleMeshObject:
        sprite_texture = texture if isinstance(texture, Texture) else self.resource_manager.get(RT.RT_TEXTURE, texture)
        sprite_mesh = self.resource_manager.get(RT.RT_MESH, "default_square")
        sprite_shader = self.resource_manager.get(RT.RT_SHADER_PROGRAM, "default_basic")

        sprite_object = SimpleMeshObject(sprite_mesh, sprite_shader)
        sprite_object.textures.append(sprite_texture)

        return sprite_object

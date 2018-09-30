from gcraft.resources.resource import Resource
from gcraft.resources.resource_loader import ResourceLoader
from gcraft.resources.loaders import DefaultShaderLoader
from gcraft.resources.loaders import FileShaderLoader
from gcraft.resources.loaders import DefaultMeshLoader
from gcraft.resources.loaders import TextureFileLoader
from gcraft.resources.loaders import StlFileMeshLoader
from gcraft.resources.loaders import PlyFileMeshLoader


class ResourcesManager:

    def __init__(self):
        self.resources_types = {}
        self.resources_loaders = [DefaultShaderLoader(), FileShaderLoader(), DefaultMeshLoader(), TextureFileLoader(),
                                  StlFileMeshLoader(), PlyFileMeshLoader()]

    def push(self, r_id, resource: Resource):
        if resource is None:
            return None

        if resource.r_type not in self.resources_types:
            self.resources_types[resource.r_type] = {}

        self.resources_types[resource.r_type][r_id] = resource

        return resource

    def get(self, res_type, r_id, load_params={}):
        if self.load(res_type, r_id, load_params):
            return self.resources_types[res_type][r_id]
        return None

    def load(self, res_type, r_id, load_params={}):
        if res_type in self.resources_types:
            resources = self.resources_types[res_type]
            if r_id in resources:
                return True

        loader = self._get_loader(r_id, res_type, load_params)
        if loader is None:
            return False

        self.push(r_id, loader.load(r_id, load_params))
        return True

    def _get_loader(self, r_id, res_type, load_params) -> ResourceLoader:
        res = list(filter(lambda f: f.can_load(r_id, res_type, load_params), self.resources_loaders))
        return res[0] if res else None

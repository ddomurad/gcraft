from gcraft.resources.resource import Resource
from os import path


class ResourceLoader:

    def can_load(self, r_id, r_type, params) -> bool:
        return False

    def load(self, r_id, params) -> Resource or None:
        return None


class FileResourceLoader(ResourceLoader):

    @staticmethod
    def can_load_file(r_id, params, file_ext=None) -> bool:
        file_path = FileResourceLoader.get_file_name(r_id, params)
        if file_path is None or (file_ext and not file_path.endswith(file_ext)) or not path.exists(file_path):
            return False

        return True

    @staticmethod
    def get_file_name(r_id, params) -> str or None:
        return params.get("path") or r_id if isinstance(r_id, str) else None

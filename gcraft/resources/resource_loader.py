from gcraft.resources.resource import Resource


class ResourceLoader:

    def can_load(self, r_id, r_type):
        return False

    def load(self, r_id, params) -> Resource:
        return None

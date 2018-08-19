from gcraft.resources.resource_types import *


class Resource:

    def __init__(self, r_id, r_type):
        self.r_id = r_id
        self.r_type = r_type

    def release(self):
        pass
from math import sin, cos
import numpy as np
from gcraft.utils.vector_ops import v3_add

class Transformation:
    def __init__(self):
        self._pos = [0, 0, 0]
        self._rot = [0, 0, 0]
        self._scale = [1, 1, 1]

        self.translation_matrix = np.identity(4)
        self.rotation_matrix = np.identity(4)
        self.scale_matrix = np.identity(4)
        self.transform_matrix = np.identity(4)

    def get_pos(self):
        return self._pos[:]
    
    def get_rot(self):
        return self._rot[:]

    def get_scale(self):
        return self._scale[:]

    def set_pos(self, pos):
        self._pos[0] = pos[0]
        self._pos[1] = pos[1]
        self._pos[2] = pos[2]

        self.translation_matrix[3][0] = pos[0]
        self.translation_matrix[3][1] = pos[1]
        self.translation_matrix[3][2] = pos[2]
        self._update_transform_matrix()

    def rotate(self, delta_rot):
        self.set_rot(v3_add(self._rot, delta_rot))

    def set_rot(self, rot):

        self._rot[0] = rot[0]
        self._rot[1] = rot[1]
        self._rot[2] = rot[2]

        a = cos(rot[0])
        b = sin(rot[0])
        c = cos(rot[1])
        d = sin(rot[1])
        e = cos(rot[2])
        f = sin(rot[2])
        ad = a * d
        bd = b * d

        self.rotation_matrix[0][0] = c * e
        self.rotation_matrix[0][1] = -c * f
        self.rotation_matrix[0][2] = d
        self.rotation_matrix[1][0] = bd * e + a * f
        self.rotation_matrix[1][1] = -bd * f + a * e
        self.rotation_matrix[1][2] = -b * c
        self.rotation_matrix[2][0] = -ad * e + b * f
        self.rotation_matrix[2][1] = ad * f + b * e
        self.rotation_matrix[2][2] = a * c

        self.rotation_matrix[0][3] = self.rotation_matrix[1][3] = self.rotation_matrix[2][3] = self.rotation_matrix[3][0] \
            = self.rotation_matrix[3][1] = self.rotation_matrix[3][2] = 0
        self.rotation_matrix[3][3] = 1
        self._update_transform_matrix()

    def set_scale(self, scale):
        self._scale[0] = scale[0]
        self._scale[1] = scale[1]
        self._scale[2] = scale[2]

        self.scale_matrix[0][0] *= scale[0]
        self.scale_matrix[1][1] *= scale[1]
        self.scale_matrix[2][2] *= scale[2]
        self._update_transform_matrix()

    def _update_transform_matrix(self):
        self.transform_matrix = np.matmul(self.scale_matrix, np.matmul(self.rotation_matrix, self.translation_matrix))

    def get_matrix(self):
        return self.transform_matrix

from OpenGL.GL import *
from gcraft.utils.vector_ops import *


class CameraProjection:
    def get_projection_matrix(self, view_angle, z_near, z_far, window_size):
        pass


class FrustumProjection(CameraProjection):
    def get_projection_matrix(self, view_angle, z_near, z_far, window_size):
        ratio = window_size[1]/window_size[0]

        n, f = z_near, z_far
        w = tan(view_angle*pi/360)*n
        l, r = -w, w
        b, t = -w*ratio, w*ratio

        return np.array([[2.0*n/(r-l),  0.0,            0.0,            0.0],
                         [0.0,          2.0*n/(t-b),    0.0,            0.0],
                         [(r+l)/(r-l),  (t+b)/(t-b),    -(f+n)/(f-n),   -1],
                         [0.0,          0.0,            -2*f*n/(f-n),   0.0]])


class Camera:
    def __init__(self):
        self.projection = FrustumProjection()
        self.projection_matrix = np.identity(4)
        self.view_matrix = np.identity(4)

        self.projection_view_matrix = np.identity(4)

        self.view_angle = 45
        self.view_near = 0.1
        self.view_far = 1000

    def apply_window_size(self, window_size):
        glViewport(0, 0, window_size[0], window_size[1])
        self.projection_matrix = self.projection.get_projection_matrix(self.view_angle, self.view_near, self.view_far,
                                                                       window_size)
        self._update_pv_matrix()

    def look_at(self, pos, target, up):
        z_axis = v3_normalize_self(v3_sub(target, pos))
        x_axis = v3_normalize_self(v3_cross(up, z_axis))
        y_axis = v3_cross(z_axis, x_axis)

        d1 = x_axis[0] * -pos[0] + x_axis[1] * -pos[1] + x_axis[2] * -pos[2]
        d2 = y_axis[0] * -pos[0] + y_axis[1] * -pos[1] + y_axis[2] * -pos[2]
        d3 = z_axis[0] * -pos[0] + z_axis[1] * -pos[1] + z_axis[2] * -pos[2]

        self.view_matrix = np.array([[x_axis[0], y_axis[0], z_axis[0], 0],
                                     [x_axis[1], y_axis[1], z_axis[1], 0],
                                     [x_axis[2], y_axis[2], z_axis[2], 0],
                                     [d1,        d2,        d3,        1]])
        self._update_pv_matrix()

    def _update_pv_matrix(self):
        self.projection_view_matrix = np.matmul(self.view_matrix, self.projection_matrix)


class Camera3d(Camera):
    def __init__(self):
        Camera.__init__(self)
        self.pos = [0.0, 0.0, 0.0]
        self.target = [0.0, 0.0, 0.0]
        self.up = [0.0, 1.0, 0.0]
        self.screen_size = [1.0, 1.0]

    def update_view(self):
        self.look_at(self.pos, self.target, self.up)


class Camera2d(Camera):
    def __init__(self):
        Camera.__init__(self)
        self.target = [0.0, 0.0]
        self.screen_size = [1.0, 1.0]
        self.dist = 10.0

    def update_view(self):
        self.look_at(self.target + [self.dist], self.target + [0], (0, 1, 0))


class FlyingCamera3d(Camera):
    def __init__(self):
        Camera.__init__(self)
        self.pos = [0.0, 0.0, 0.0]
        self.look_dir = [0.0, 0.0, 1.0]
        self.look_side = [0.0, 0.0, 0.0]

        self.yaw = 0.0
        self.pitch = 0.0

    def move(self, dist):
        v3_add_self(self.pos, v3_mul(self.look_dir, dist))

    def move_side(self, dist):
        v3_add_self(self.pos, v3_mul(self.look_side, dist))

    def move_up(self, dist):
        self.pos[1] += dist

    def rotate(self, r):
        self.yaw += r[0]
        self.pitch += r[1]

        if self.pitch > pi/2.1:
            self.pitch = pi/2.1
        elif self.pitch < -pi/2.1:
            self.pitch = -pi/2.1

    def update_view(self):
        cp = cos(self.pitch)
        self.look_dir[0] = cos(self.yaw) * cp
        self.look_dir[1] = sin(self.pitch)
        self.look_dir[2] = sin(self.yaw) * cp

        self.look_side[0] = cos(self.yaw - pi / 2)
        self.look_side[2] = sin(self.yaw - pi / 2)

        self.look_at(self.pos, np.add(self.pos, self.look_dir), [0, 1, 0])

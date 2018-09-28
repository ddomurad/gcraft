from tests.cuboid_interpolator import interpolate_cuboid_mesh, generate_vertex_cache, data_to_mesh_type
from gcraft.utils.vector_ops import v3_add
from gcraft.utils.geometry.mesh_ops import add_normals_data
import gcraft as gc
import math


class TestRenderer(gc.core.GCraftRenderer):

    def __init__(self):
        gc.core.GCraftRenderer.__init__(self)
        self.resource_manager = None
        self.camera = None

        self.grid_object = None
        self.cube_frame = None
        self.test_model = None

        self.model_rotation = 0
        self.model_rotation_2 = 0
        self.mesh_counter = 31

        self.vertex_mesh_cache = generate_vertex_cache()

    def on_init(self):
        self.resource_manager = gc.resources.ResourcesManager()

        self.camera = gc.scene.FlyingCamera()
        self.camera.pos = [5, 3, 5]
        self.camera.target = [0, 0.5, 0]

        self.camera.update_view()

        self.simple_lighting_shader = self.resource_manager.get(gc.resources.RT_SHADER_PROGRAM, "default_lighting")
        self.simple_lighting_shader.use()
        self.simple_lighting_shader.set_uniform_1f("ambient_lighting", 0.25)


        grid_mesh = gc.resources.StaticMesh('grid', gc.utils.geometry.generate_gird_geometry([50, 50], [10, 10]))
        self.grid_object = gc.scene.SimpleMeshObject(grid_mesh,
                                        self.resource_manager.get(gc.resources.RT_SHADER_PROGRAM, "default_basic"))

        self.grid_object.material.difusse_color = [0.3, 0.3, 0.3, 1]

        self.generate_procedural_mesh()

        gc.glClearColor(0.1, 0.1, 0.1, 1.0)
        gc.glEnable(gc.GL_DEPTH_TEST)
        gc.glEnable(gc.GL_CULL_FACE)

        self.mouse_warp = [400, 300]

    def generate_procedural_mesh(self):
        mesh_data = []
        self.sx = -1.5

        def add_vertecies(data, offset, size):
            type = data_to_mesh_type(data)
            vertex = interpolate_cuboid_mesh(self.vertex_mesh_cache[type], offset, size)
            mesh_data.extend(vertex)

        def fnc(x, y, z):
            return 1 if math.sin(z/5)*math.sin(x/5)*2 > (y-5) else -1


        interpulationAreaSize = 50
        segments = 50
        dCube = interpulationAreaSize/segments

        for sx in range(segments):
            for sy in range(segments):
                for sz in range(segments):
                    x1 = sx * dCube
                    y1 = sy * dCube
                    z1 = sz * dCube

                    x2 = (sx + 1) * dCube
                    y2 = (sy + 1) * dCube
                    z2 = (sz + 1) * dCube

                    add_vertecies([fnc(x1, y1, z1), fnc(x2, y1, z1), fnc(x1, y2, z1), fnc(x2, y2, z1),
                                   fnc(x1, y1, z2), fnc(x2, y1, z2), fnc(x1, y2, z2), fnc(x2, y2, z2)], [x1, y1, z1], dCube)

        mesh_geometry = gc.utils.geometry.MeshGeometry(gc.GL_TRIANGLES, mesh_data, [("v_pos", 3)], None, len(mesh_data) / 3)
        add_normals_data(mesh_geometry)
        mesh = gc.resources.StaticMesh("test", mesh_geometry)

        self.test_model = gc.scene.SimpleMeshObject(mesh, self.simple_lighting_shader)

    def on_render(self):
        gc.glClear(gc.GL_COLOR_BUFFER_BIT | gc.GL_DEPTH_BUFFER_BIT)

        self.camera.update_view()
        self.simple_lighting_shader.set_uniform_3f("light_dir", self.camera.look_dir)
        self.grid_object.draw(self.camera)

        self.test_model.trans.set_rot([self.model_rotation_2, self.model_rotation, 0])
        self.test_model.draw(self.camera)

        self.swap_buffers()

        if self.input_state.is_key_pressed(b'w'):
            self.camera.move(0.3)
        elif self.input_state.is_key_pressed(b's'):
            self.camera.move(-0.3)

        if self.input_state.is_key_pressed(b'a'):
            self.camera.move_side(0.3)
        elif self.input_state.is_key_pressed(b'd'):
            self.camera.move_side(-0.3)

        if self.input_state.is_key_pressed(101):
            self.camera.move_up(0.3)
        elif self.input_state.is_key_pressed(103):
            self.camera.move_up(-0.3)

        if self.input_state.is_mouse_moving:
            self.camera.rotate([-self.input_state.mouse_movement[0]/400, self.input_state.mouse_movement[1]/400])

    def on_reshape(self, w, h):
        self.camera.apply_window_size((w, h))

    def on_input(self, event: gc.core.InputEvent):
        if event.type == gc.core.InputEvent.IE_KEY_DOWN:
            if event.key == b'q':
                exit()

    def on_fps(self, fps, max_frame_time, avg_frame_time, min_frame_time):
        print("fps: {0}, max: {1}[ms], avg: {2}[ms], min: {3}[ms]".format(fps, max_frame_time*1000,
                                                                          avg_frame_time*1000, min_frame_time*1000))

        print("gl cals: {0}".format(gc.utils.state_manager.get_gl_calls()))


gc.application.glut.run((800,600), "trest", TestRenderer())
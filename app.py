import gcraft as gc
import gcraft.application.glut as glutApp

# from scene import TestScene

class TestScene(gc.core.GCraftScene):
    def __init__(self, app: gc.core.GCraftSceneApp):
        gc.core.GCraftScene.__init__(self, "test_scene", app)
        self.camera = None
        self.mesh_object = None
        self.grid_object = None

    def on_enter(self):
        self.camera = gc.scene.Camera3d()
        self.camera.pos = [5, 3, 5]
        self.camera.target = [0, 0.5, 0]
        self.camera.update_view()

        default_shader = self.app.resource_manager.get(gc.resources.RT_SHADER_PROGRAM, "default_basic")
        
        simple_lighting_shader = self.app.resource_manager.get(gc.resources.RT_SHADER_PROGRAM, "default_lighting")
        simple_lighting_shader.use()
        simple_lighting_shader.set_uniform_1f("ambient_lighting", 0.1)
        simple_lighting_shader.set_uniform_3f("light_dir", [0.0, -1.0, -1.0])
        
        mesh_transformation = gc.utils.Transformation()
        mesh_transformation.set_rot([-3.14/2, 0, 0])

        def apply_transform(m):
            gc.utils.geometry.mesh_ops.transform(m, mesh_transformation)
            gc.utils.geometry.mesh_ops.move_to_cog(m, [1, 0, 1])

        model_mesh = self.app.resource_manager.get(gc.resources.RT_MESH, 
            # "default_cube"
            # "C:\\tmp\\cracked_D12.stl"
            "/home/work/Projects/ender/miniatures/trap_door/cut_stone_floor.2x2.trapdoor.stl"
            , {"mesh_ops": [apply_transform, gc.utils.geometry.mesh_ops.normalize_normals]}
            )

        self.mesh_object = gc.scene.SimpleMeshObject(model_mesh, simple_lighting_shader)
        self.mesh_object.material.diffuse_color = [0.5, 0.5, 0.5, 1.0]
        self.mesh_object.trans.set_scale([0.12, 0.12, 0.12])

        grid = gc.utils.geometry.generate_gird_geometry([100, 100], [100, 100])
        grid_mesh = gc.resources.StaticMesh('grid', grid)
        self.grid_object = gc.scene.SimpleMeshObject(grid_mesh, default_shader)
        self.grid_object.material.diffuse_color = [0.5, 0.5, 0.5, 1.0]

    def on_exit(self):
        pass

    def on_render(self):
        gc.glClear(gc.GL_COLOR_BUFFER_BIT | gc.GL_DEPTH_BUFFER_BIT)
        self.camera.update_view()
        self.mesh_object.draw(self.camera)
        self.grid_object.draw(self.camera)

        self.mesh_object.trans.rotate([.0,.01,.0])

    def on_reshape(self, w, h):
        self.camera.apply_window_size((w, h))

    def on_input(self, event: gc.core.InputEvent):
        pass


class TestApp(gc.core.GCraftSceneApp):
    def __init__(self):
        gc.core.GCraftSceneApp.__init__(self)
        self.resource_manager = None
    
    def on_init(self):
        self.resource_manager = gc.resources.ResourcesManager()
        self.scene_mannager.add_scene(TestScene(self), True)
        
        gc.glClearColor(0.1, 0.1, 0.1, 1.0)
        gc.glEnable(gc.GL_CULL_FACE)
        gc.glCullFace(gc.GL_BACK)
        gc.glEnable(gc.GL_DEPTH_TEST)
    
    def on_fps(self, fps, max_frame_time, avg_frame_time, min_frame_time):
        print("fps: {0}, max: {1}[ms], avg: {2}[ms], min: {3}[ms]".format(fps, max_frame_time*1000, avg_frame_time*1000, min_frame_time*1000))
        print("gl cals: {0}".format(gc.utils.state_manager.get_gl_calls()))

glutApp.run((800,600), b"Test app", TestApp())
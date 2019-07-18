import gcraft as gc
from gcraft.utils.geometry.mesh_ops import add_normals_data

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
        simple_lighting_shader.set_uniform_3f("light_dir", [0.0, 1.0, -1.0])

        model_mesh = self.app.resource_manager.get(gc.resources.RT_MESH, 
            "C:\\tmp\\cracked_D12.stl"
            # "C:\\tmp\\Basilisk_Solid_Extra.stl"
            # , {"mesh_ops": [gc.utils.geometry.mesh_ops.add_normals_data]}
            )

        self.mesh_object = gc.scene.SimpleMeshObject(model_mesh, simple_lighting_shader)
        self.mesh_object.material.diffuse_color = [0.5, 0.5, 0.5, 1.0]
        self.mesh_object.trans.set_scale([0.05, 0.05, 0.05])

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

        self.mesh_object.trans.rotate([0.01,0,0])

    def on_reshape(self, w, h):
        self.camera.apply_window_size((w, h))

    def on_input(self, event: gc.core.InputEvent):
        pass

import gcraft as gc
import gcraft.application.glut as glutApp

class MyScene(gc.core.GCraftScene):
    def __init__(self, app: gc.core.GCraftSceneApp):
        gc.core.GCraftScene.__init__(self, "test_scene", app)
        self.camera = None
        self.cube_object = None

    def on_enter(self):
        self.camera = gc.scene.Camera3d()
        self.camera.pos = [5, 3, 5]
        self.camera.target = [0, 0.5, 0]
        self.camera.update_view()

        cube_mesh = self.app.resource_manager.get(gc.resources.RT_MESH, "default_cube")
        default_shader = self.app.resource_manager.get(gc.resources.RT_SHADER_PROGRAM, "default_basic")

        self.cube_object = gc.scene.SimpleMeshObject(cube_mesh, default_shader)

    def on_exit(self):
        pass

    def on_render(self):
        gc.glClear(gc.GL_COLOR_BUFFER_BIT | gc.GL_DEPTH_BUFFER_BIT)
        self.camera.update_view()
        self.cube_object.draw(self.camera)

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
        self.scene_mannager.add_scene(MyScene(self), True)
        
        gc.glClearColor(0.1, 0.1, 0.1, 1.0)
        gc.glEnable(gc.GL_CULL_FACE)
        gc.glCullFace(gc.GL_BACK)
        gc.glEnable(gc.GL_DEPTH_TEST)
    
    def on_fps(self, fps, max_frame_time, avg_frame_time, min_frame_time):
        print("fps: {0}, max: {1}[ms], avg: {2}[ms], min: {3}[ms]".format(fps, max_frame_time*1000, avg_frame_time*1000, min_frame_time*1000))
        print("gl cals: {0}".format(gc.utils.state_manager.get_gl_calls()))
        
glutApp.run((800,600), b"Test app", TestApp())
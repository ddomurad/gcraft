import gcraft as gc


class Test2dRenderer(gc.core.GCraftRenderer):

    def __init__(self):
        gc.core.GCraftRenderer.__init__(self)
        self.resource_manager = None
        self.camera = None
        self.shader = None
        self.cup_model = None
        self.object2d = None
        self.sprite1 = None
        self.rotation = 0.5

    def on_init(self):
        self.resource_manager = gc.resources.ResourcesManager()
        self.camera = gc.scene.camera.Camera2d()
        self.camera.target = [1, 1]

        self.shader = self.resource_manager.get(gc.resources.RT_SHADER_PROGRAM, "default_basic")
        self.cup_model = self.resource_manager.get(gc.resources.RT_MESH, "/home/work/Tmp/cup.ply")
        self.object2d = gc.scene.SimpleMeshObject(self.cup_model, self.shader)

        factory = gc.scene.SceneFactory(self.resource_manager)
        self.sprite1 = factory.create_sprite_2d("/home/work/Tmp/crate.jpeg")

        gc.glDisable(gc.GL_CULL_FACE)
        gc.glClearColor(0.1, 0.1, 0.1, 1.0)

    def on_render(self):
        gc.glClear(gc.GL_COLOR_BUFFER_BIT | gc.GL_DEPTH_BUFFER_BIT)

        self.camera.update_view()
        self.shader.use()

        # self.shader.set_uniform_4f("difusse_color", [1, 1, 1, 1])
        # self.shader.set_uniform_matrix_4f("projection_view_matrix",
        #                                   self.camera.projection_view_matrix)

        self.object2d.draw(self.camera)
        self.sprite1.trans.set_rot([0, 0, self.rotation])
        self.sprite1.draw(self.camera)

        self.swap_buffers()

    def on_reshape(self, w, h):
        self.camera.apply_window_size((w, h))

    def on_input(self, event: gc.core.InputEvent):
        if event.type == gc.core.InputEvent.IE_KEY_DOWN:
            if event.key == b'q':
                exit()

    def on_fps(self, fps, max_frame_time, avg_frame_time, min_frame_time):
        print("fps: {0}, max: {1}[ms], avg: {2}[ms], min: {3}[ms]".format(fps, max_frame_time * 1000,
                                                                          avg_frame_time * 1000, min_frame_time * 1000))

        print("gl cals: {0}".format(gc.utils.state_manager.get_gl_calls()))


gc.application.glut.run((800, 600), "2d test", Test2dRenderer())

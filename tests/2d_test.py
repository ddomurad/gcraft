import gcraft as gc


class Test2dRenderer(gc.core.GCraftApp):

    def __init__(self):
        gc.core.GCraftApp.__init__(self)
        self.resource_manager = None
        self.camera = None
        self.shader = None
        self.cup_model = None
        self.object2d = None
        self.sprite1 = None
        self.rotation = 0.5

        self.buffer_sprite = None
        self.test_buffer = None

    def on_init(self):
        gc.core.GCraftApp.on_init(self)

        self.resource_manager = gc.resources.ResourcesManager()
        self.camera = gc.scene.camera.Camera2d()
        self.camera.target = [1, 1]

        self.shader = self.resource_manager.get(gc.resources.RT_SHADER_PROGRAM, "default_basic")
        self.cup_model = self.resource_manager.get(gc.resources.RT_MESH, "cup_model", {"path": "/home/work/Tmp/cup.ply"})

        self.object2d = gc.scene.SimpleMeshObject(
            self.resource_manager.get(gc.resources.RT_MESH, "cup_model"), self.shader)

        self.resource_manager.load(gc.resources.RT_TEXTURE, "texture_01",
                                   {"path": "/home/work/Tmp/man.png", "mipmaps": True})

        factory = gc.scene.SceneFactory(self.resource_manager)
        self.sprite1 = factory.create_sprite_2d("texture_01")
        self.sprite1.blend_fnc = gc.utils.constants.ALPHA_BLEND

        self.test_buffer = gc.core.RenderBuffer.create((800, 600))
        self.buffer_sprite = factory.create_sprite_2d(gc.resources.Texture("test_texture", self.test_buffer.texture_id))

        gc.glClearColor(0.1, 0.1, 0.1, 0.0)

    def render(self, sprite):
        gc.glClear(gc.GL_COLOR_BUFFER_BIT | gc.GL_DEPTH_BUFFER_BIT)

        self.camera.update_view()
        self.shader.use()

        self.object2d.draw(self.camera)
        sprite.trans.set_rot([0, 0, self.rotation])
        sprite.draw(self.camera)

    def on_render(self):

        self.test_buffer.bind()
        gc.glClearColor(0.1, 0.1, 0.1, 0.0)
        self.render(self.sprite1)

        self.test_buffer.bind_screen()
        gc.glClearColor(0.5, 0.1, 0.1, 0.0)
        self.render(self.buffer_sprite)

        self.swap_buffers()
        self.rotation += 0.01

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

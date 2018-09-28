import gcraft as gc


class TestRenderer(gc.core.GCraftRenderer):

    def __init__(self):
        gc.core.GCraftRenderer.__init__(self)
        self.camera = None
        self.resource_manager = None
        self.grid_object = None
        self.mesh_object = None
        self.simple_lighting_shader = None
        self.normal_map_lighting_shader = None

        self.should_run = True
        self.model_rotation = 0

    def on_init(self):
        self.resource_manager = gc.resources.ResourcesManager()

        self.camera = gc.scene.StaticCamera()
        self.camera.pos = [5, 3, 5]
        self.camera.target = [0, 0.5, 0]

        self.camera.update_view()


        self.simple_lighting_shader = self.resource_manager.get(gc.resources.RT_SHADER_PROGRAM, "default_lighting")
        self.simple_lighting_shader.use()
        self.simple_lighting_shader.set_uniform_1f("ambient_lighting", 0.0)
        self.simple_lighting_shader.set_uniform_3f("light_dir", [0.0, -1.0, -1.0])

        normal_mapping_shader = ("../resources/normal_mapping.vs", "../resources/normal_mapping.fs")
        self.normal_map_lighting_shader = self.resource_manager.get(gc.resources.RT_SHADER_PROGRAM,
                                                                    normal_mapping_shader)

        self.normal_map_lighting_shader.use()
        self.normal_map_lighting_shader.set_uniform_1f("ambient_lighting", 0.0)
        self.normal_map_lighting_shader.set_uniform_3f("light_dir", [0.0, -1.0, -1.0])

        def fix_uv(v): v[1] = 1-v[1]; return v

        mesh = self.resource_manager.get(gc.resources.RT_MESH, "/home/work/Tmp/Rock_6_FREE/Rock_6/rock.ply",
                                         {"mesh_ops": [
                                             lambda m: gc.utils.geometry.mesh_ops.mod_vertex_data(m, "uv_0", 2, fix_uv),
                                             gc.utils.geometry.mesh_ops.add_tangents_data
                                         ]})

        grid = gc.utils.geometry.generate_gird_geometry([100, 100], [100, 100])
        grid_mesh = gc.resources.StaticMesh('grid', grid)

        self.grid_object = gc.scene.SimpleMeshObject(grid_mesh, self.resource_manager.get(gc.resources.RT_SHADER_PROGRAM,
                                                                                         "default_basic"))

        self.grid_object.material.difusse_color = [0.3, 0.3, 0.3, 1]

        self.mesh_object = gc.scene.SimpleMeshObject(mesh, self.simple_lighting_shader)
        self.mesh_object.material.difusse_color = [1.0, 1.0, 1.0, 1.0]

        self.mesh_object.textures.append(
            self.resource_manager.get(gc.resources.RT_TEXTURE,
                                      "/home/work/Tmp/Rock_6_FREE/Rock_6/Rock_6_Tex/Rock_6_d.png",
                                      {"mipmaps": True, "filter": "linear"}))

        self.mesh_object.textures.append(
            self.resource_manager.get(gc.resources.RT_TEXTURE,
                                      "/home/work/Tmp/Rock_6_FREE/Rock_6/Rock_6_Tex/Rock_6_n.png",
                                      {"mipmaps": True, "filter": "linear"}))

        self.mesh_object.textures.append(
            self.resource_manager.get(gc.resources.RT_TEXTURE,
                                      "/home/work/Tmp/Rock_6_FREE/Rock_6/Rock_6_Tex/Rock_6_ao.png",
                                      {"mipmaps": True, "filter": "linear"}))

        self.model_rotation = 0

        gc.glClearColor(0.1, 0.1, 0.1, 1.0)
        gc.glEnable(gc.GL_CULL_FACE)
        gc.glCullFace(gc.GL_BACK)
        gc.glEnable(gc.GL_DEPTH_TEST)


    def on_render(self):
        gc.glClear(gc.GL_COLOR_BUFFER_BIT | gc.GL_DEPTH_BUFFER_BIT)

        self.camera.update_view()

        self.mesh_object.trans.set_rot([3.14 / 2, self.model_rotation, 0])
        # self.mesh_object.trans.set_rot([3.14 / 2, 0, 0])

        self.mesh_object.draw(self.camera)

        self.grid_object.draw(self.camera)
        self.swap_buffers()

        # self.normal_map_lighting_shader.use()
        # self.normal_map_lighting_shader.set_uniform_3f("light_dir", [-cos(self.model_rotation), -1.0, sin(self.model_rotation)])
        #
        # self.simple_lighting_shader.use()
        # self.simple_lighting_shader.set_uniform_3f("light_dir", [-cos(self.model_rotation), -1.0, sin(self.model_rotation)])

        self.model_rotation += 0.01

    def on_reshape(self, w, h):
        print((w, h))
        self.camera.apply_window_size((w, h))

    def on_input(self, event: gc.core.InputEvent):
        if event.type == gc.core.InputEvent.IE_KEY_DOWN:
            if event.key == b'1':
                print("normal mapping disabled")
                self.mesh_object.shader = self.simple_lighting_shader
            if event.key == b'2':
                print("normal mapping enabled")
                self.mesh_object.shader = self.normal_map_lighting_shader

    def on_fps(self, fps, max_frame_time, avg_frame_time, min_frame_time):
        print("fps: {0}, max: {1}[ms], avg: {2}[ms], min: {3}[ms]".format(fps, max_frame_time*1000,
                                                                          avg_frame_time*1000, min_frame_time*1000))

        print("gl cals: {0}".format(gc.utils.state_manager.get_gl_calls()))


gc.application.glut.run((800,600), "trest", TestRenderer())
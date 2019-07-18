from OpenGL.GL import *

from gcraft.core.scene import GCraftSceneManager
from gcraft.core.input_state import InputState
from gcraft.core.input_event import InputEvent
import gcraft.utils.state_manager as sm


class GCraftApp:
    def __init__(self):
        self.input_state = InputState()
        self.mouse_warp = None
        self.continuous_rendering = True
        
    def on_init(self):
        sm.enable(GL_BLEND)
        sm.enable(GL_CULL_FACE)

    def on_render(self):
        pass

    def on_reshape(self, w, h):
        pass

    def on_fps(self, fps, max_frame_time, avg_frame_time, min_frame_time):
        pass

    def on_input(self, event: InputEvent):
        pass

    def swap_buffers(self):
        pass

class GCraftSceneApp(GCraftApp):
    def __init__(self):
        GCraftApp.__init__(self)
        self.scene_mannager = GCraftSceneManager()
        
    def on_init(self):
        GCraftApp.on_init(self)

    def on_render(self):
        if self.scene_mannager.active_scene:
            self.scene_mannager.active_scene.on_render()

        self.swap_buffers()

    def on_reshape(self, w, h):
        if self.scene_mannager.active_scene:
            self.scene_mannager.active_scene.on_reshape(w, h)

    def on_fps(self, fps, max_frame_time, avg_frame_time, min_frame_time):
        pass

    def on_input(self, event: InputEvent):
        if self.scene_mannager.active_scene:
            self.scene_mannager.active_scene.on_input(event)

    def swap_buffers(self):
        pass    

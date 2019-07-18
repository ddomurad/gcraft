from OpenGL.GL import *

from gcraft.core.input_state import InputState
from gcraft.core.input_event import InputEvent
import gcraft.utils.state_manager as sm

class GCraftScene:
    def __init__(self, name: str, app):
        self.app = app
        self.name = name
        self.active_scene = None

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_render(self):
        pass

    def on_reshape(self, w, h):
        pass

    def on_input(self, event: InputEvent):
        pass



class GCraftSceneManager:
    def __init__(self):
        self.scenes = {}
        self.active_scene = None

    def add_scene(self, scene: GCraftScene, enter: bool = False):
        self.scenes[scene.name] = scene
        if enter:
            self.enter_scene(scene.name)
    
    def enter_scene(self, name):
        if self.active_scene:
            self.active_scene.on_exit()

        self.active_scene = self.scenes[name]
        self.active_scene.on_enter()


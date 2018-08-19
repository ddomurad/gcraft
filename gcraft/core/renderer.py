from gcraft.core.input_state import InputState
from gcraft.core.input_event import InputEvent


class GCraftRenderer:
    def __init__(self):
        self.input_state = InputState()
        self.mouse_warp = None
        self.continuous_rendering = True

    def on_init(self):
        pass

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


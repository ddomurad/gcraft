from gcraft.core.input_event import InputEvent


class InputState:
    def __init__(self):
        self._keys = {}
        self._buttons = {}
        self.mouse_pos = [0, 0]
        self.mouse_movement = [0, 0]
        self.is_mouse_moving = False

    def is_key_pressed(self, k):
        if k not in self._keys:
            return False

        return self._keys[k]

    def is_button_pressed(self, b):
        if b not in self._buttons:
            return False

        return self._buttons[b]

    def clear_mouse_movement(self):
        self.mouse_movement = [0, 0]
        self.is_mouse_moving = False

    def update_state(self, event: InputEvent):
        if event.type == InputEvent.IE_KEY_DOWN:
            self._keys[event.key] = True
        elif event.type == InputEvent.IE_KEY_UP:
            self._keys[event.key] = False
        elif event.type == InputEvent.IE_MOUSE:
            self.mouse_pos = event.mouse_pos[:]
            self._buttons[event.mouse_btn] = event.state
        elif event.type == InputEvent.IE_MOUSE_MOVE:
            self.mouse_pos = event.mouse_pos[:]
            self.mouse_movement = event.mouse_delta[:]
            self.is_mouse_moving = True


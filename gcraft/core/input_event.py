class InputEvent:
    IE_MOUSE_MOVE = 1
    IE_MOUSE = 2
    IE_KEY_DOWN = 3
    IE_KEY_UP = 4

    def __init__(self, input_type, mouse_x=0, mouse_y=0, mouse_dx=0, mouse_dy=0, mouse_btn=0, key=b'', state=0):
        self.mouse_pos = [mouse_x, mouse_y]
        self.mouse_delta = [mouse_dx, mouse_dy]
        self.mouse_btn = mouse_btn
        self.key = key
        self.state = state
        self.type = input_type


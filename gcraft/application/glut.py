from OpenGL.GLUT import *
from gcraft.core.app import GCraftApp
from gcraft.core.input_event import InputEvent
import gcraft.utils.state_manager as sm

import time

_start_time = time.time()
_frames_count = 0

_max_frame_time = 0
_min_frame_time = 1e5
_avg_frame_time = 0
_loop_stats_counter = 10

_last_mx = None
_last_my = None

_just_warped = False


def run(window_size, window_title, gc_app: GCraftApp):

    def _render_fnc():
        global _frames_count
        global _start_time
        global _max_frame_time
        global _min_frame_time
        global _avg_frame_time
        global _loop_stats_counter

        try:
            frame_time_start = time.time()
            sm.reset()
            gc_app.on_render()
            glutSwapBuffers()
            gc_app.input_state.clear_mouse_movement()
            frame_time_end = time.time()
            frame_time = frame_time_end - frame_time_start

            if frame_time > _max_frame_time:
                _max_frame_time = frame_time

            if frame_time < _min_frame_time:
                _min_frame_time = frame_time

            _avg_frame_time += frame_time

            _frames_count += 1
            if _frames_count >= _loop_stats_counter:
                _frames_count = 0
                end_time = time.time()
                _avg_frame_time /= _loop_stats_counter
                fps = _loop_stats_counter / (end_time - _start_time)
                gc_app.on_fps(fps, _max_frame_time, _avg_frame_time, _min_frame_time)

                _loop_stats_counter = fps * 3

                _start_time = end_time
                _avg_frame_time = 0
                _min_frame_time = 1e5
                _max_frame_time = 0
        except:
            print(sys.exc_info())
            glutLeaveMainLoop()

    def _on_mouse_move(x, y):
        global _last_mx
        global _last_my
        global _just_warped

        if _just_warped:
            _just_warped = False
            _last_mx = gc_app.mouse_warp[0]
            _last_my = gc_app.mouse_warp[1]
            return

        if _last_mx is None:
            _last_mx = x

        if _last_my is None:
            _last_my = y

        event = InputEvent(InputEvent.IE_MOUSE_MOVE, mouse_x=x, mouse_y=y, mouse_dx=_last_mx - x, mouse_dy=_last_my - y)
        gc_app.input_state.update_state(event)
        gc_app.on_input(event)

        _last_mx = x
        _last_my = y

        if gc_app.mouse_warp is not None:
            _just_warped = True
            glutWarpPointer(gc_app.mouse_warp[0], gc_app.mouse_warp[1])

    def _on_mouse(btn, state, x, y):
        event = InputEvent(InputEvent.IE_MOUSE, mouse_x=x, mouse_y=y, mouse_btn=btn, state=state == 0)
        gc_app.input_state.update_state(event)
        gc_app.on_input(event)

    def _on_key(key, x, y):
        event = InputEvent(InputEvent.IE_KEY_DOWN, mouse_x=x, mouse_y=y, key=key)
        gc_app.input_state.update_state(event)
        gc_app.on_input(event)

    def _on_key_up(key, x, y):
        event = InputEvent(InputEvent.IE_KEY_UP, mouse_x=x, mouse_y=y, key=key)
        gc_app.input_state.update_state(event)
        gc_app.on_input(event)

    glutInit()

    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(window_size[0], window_size[1])
    glutCreateWindow(window_title)

    glutMotionFunc(_on_mouse_move)
    glutPassiveMotionFunc(_on_mouse_move)
    glutMouseFunc(_on_mouse)
    # glutMouseWheelFunc(__on_mouse_wheel)
    glutKeyboardFunc(_on_key)
    glutSpecialFunc(_on_key)

    glutKeyboardUpFunc(_on_key_up)
    glutSpecialUpFunc(_on_key_up)

    glutIdleFunc(_render_fnc)
    glutDisplayFunc(_render_fnc)

    glutReshapeFunc(gc_app.on_reshape)

    gc_app.on_init()
    glutMainLoop()

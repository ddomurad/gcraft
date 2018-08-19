from OpenGL.GLUT import *
from gcraft.core.renderer import GCraftRenderer
from gcraft.core.input_event import InputEvent
import gcraft.utils.state_manager as sm

import wx
from wx import glcanvas


class GCraftCanvas(wx.glcanvas.GLCanvas):
    def __init__(self, parent, renderer: GCraftRenderer):
        wx.glcanvas.GLCanvas.__init__(self, parent, -1)

        self._renderer = renderer
        self._renderer.swap_buffers = self.on_swap_buffers

        self._renderer_inited = False

        self._last_mouse_pos = None

        self._context = wx.glcanvas.GLContext(self)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background_event)
        self.Bind(wx.EVT_SIZE, self.on_resize_event)
        self.Bind(wx.EVT_PAINT, self.on_paint_event)

        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_event)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down_event)
        self.Bind(wx.EVT_KEY_UP, self.on_key_up_event)

        self.Bind(wx.EVT_IDLE, self.on_idle_event)

    def init(self):
        glutInit()
        self._renderer_inited = True
        self._renderer.on_init()
        self.resize()

    def resize(self):
        if self._renderer_inited:
            size = self.GetClientSize()
            self.SetCurrent(self._context)
            self._renderer.on_reshape(size.width, size.height)

    def render(self):
        self._renderer.on_render()
        self._renderer.input_state.clear_mouse_movement()

    def on_swap_buffers(self):
        self.SwapBuffers()

    def on_idle_event(self, event):
        self.Refresh(False)

    def on_erase_background_event(self, event):
        pass  # Do nothing, to avoid flashing on MSW.

    def on_resize_event(self, event):
        wx.CallAfter(self.resize)
        event.Skip()

    def on_paint_event(self, event):
        self.SetCurrent(self._context)
        if not self._renderer_inited:
            self.init()

        self.render()
        self.Refresh(False)

    def on_mouse_event(self, event):
        if event.GetEventType() == wx.wxEVT_LEFT_DOWN:
            input_event = InputEvent(InputEvent.IE_MOUSE, mouse_x=event.X, mouse_y=event.Y, mouse_btn=0, state=True)
            self._renderer.input_state.update_state(input_event)
            self._renderer.on_input(input_event)
        elif event.GetEventType() == wx.wxEVT_LEFT_UP:
            input_event = InputEvent(InputEvent.IE_MOUSE, mouse_x=event.X, mouse_y=event.Y, mouse_btn=0, state=False)
            self._renderer.input_state.update_state(input_event)
            self._renderer.on_input(input_event)
        if event.GetEventType() == wx.wxEVT_RIGHT_DOWN:
            input_event = InputEvent(InputEvent.IE_MOUSE, mouse_x=event.X, mouse_y=event.Y, mouse_btn=1, state=True)
            self._renderer.input_state.update_state(input_event)
            self._renderer.on_input(input_event)
        elif event.GetEventType() == wx.wxEVT_RIGHT_UP:
            input_event = InputEvent(InputEvent.IE_MOUSE, mouse_x=event.X, mouse_y=event.Y, mouse_btn=1, state=False)
            self._renderer.input_state.update_state(input_event)
            self._renderer.on_input(input_event)
        elif event.GetEventType() == wx.wxEVT_MOTION:
            if self._last_mouse_pos is None:
                self._last_mouse_pos = [event.X, event.Y]

            input_event = InputEvent(InputEvent.IE_MOUSE_MOVE, mouse_x=event.X, mouse_y=event.Y,
                                     mouse_dx=self._last_mouse_pos[0] - event.X,
                                     mouse_dy=self._last_mouse_pos[1] - event.Y)

            self._renderer.input_state.update_state(input_event)
            self._renderer.on_input(input_event)

            self._last_mouse_pos[0] = event.X
            self._last_mouse_pos[1] = event.Y

        self.Refresh(False)

    def on_key_down_event(self, event):
        input_event = InputEvent(InputEvent.IE_KEY_DOWN, mouse_x=event.Y, mouse_y=event.Y, key=event.GetKeyCode())
        self._renderer.input_state.update_state(input_event)
        self._renderer.on_input(input_event)

        self.Refresh(False)

    def on_key_up_event(self, event):
        input_event = InputEvent(InputEvent.IE_KEY_UP, mouse_x=event.Y, mouse_y=event.Y, key=event.GetKeyCode())
        self._renderer.input_state.update_state(input_event)
        self._renderer.on_input(input_event)

        self.Refresh(False)

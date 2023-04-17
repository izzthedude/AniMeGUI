import cv2
import numpy as np
from gi.repository import GLib, Gtk

from animegui.controllers.controller_base import BaseController
from animegui.enums import Paths
from animegui.ui.view_page_live import LivePageView


class LiveController(BaseController):
    __gtype_name__ = "LiveController"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._view: LivePageView

        self.cap = cv2.VideoCapture(0)
        self.refresh_rate: int = 10
        self.is_current_view: bool = False

    def set_view(self, view: LivePageView):
        self._view = view
        self._view.connect("notify::sensitive", self._on_has_focus)

        self._view.fps_spin.set_range(1, 30)
        self._view.fps_spin.set_increments(1, 1)
        self._view.fps_spin.set_value(self.refresh_rate)
        self._view.fps_spin.connect("value-changed", self._on_fps_changed)

    def tick_frame(self):
        ret, frame = self.cap.read()
        frame: np.ndarray
        if ret and self._view:
            cv2.imwrite(Paths.FRAME_CACHE, frame)
            self._view.draw_area.queue_draw()

        if self.is_current_view:
            GLib.timeout_add(1000 // self.refresh_rate, self.tick_frame)

    def _on_fps_changed(self, spin: Gtk.SpinButton):
        self.refresh_rate = spin.get_value()

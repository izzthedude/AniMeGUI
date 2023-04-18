import cv2
import numpy as np
from gi.repository import GLib, Gtk, GObject

from animegui.controllers.controller_base import BaseController
from animegui.enums import Paths
from animegui.ui.view_page_live import LivePageView
from animegui.utils.gi_helpers import create_signal


class LiveController(BaseController):
    __gtype_name__ = "LiveController"

    TICK = "tanned-neuron"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not GObject.signal_list_names(self):
            create_signal(self, self.TICK)

        self._view: LivePageView
        self.cap = cv2.VideoCapture(0)

        self.is_current_view: bool = False
        self.is_enabled: bool = False
        self.refresh_rate: int = 10

    def set_view(self, view: LivePageView):
        self._view = view

        if not self.cap.isOpened():
            self._view.show_nocam_status()

        self._view.check_camera_btn.connect("clicked", self._on_check_camera)

        self.is_enabled = self._view.enable_switch.get_active()
        self._view.enable_switch.connect("notify::active", self._on_enable_changed)

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

            if self.is_enabled:
                self.emit(self.TICK)

            if self.is_current_view:
                GLib.timeout_add(1000 // self.refresh_rate, self.tick_frame)

        elif not ret:
            self.cap.release()
            self._view.show_nocam_status()

    def _on_check_camera(self, button: Gtk.Button):
        self.cap = cv2.VideoCapture(0)

        if self.cap.isOpened():
            self._view.show_nocam_status(False)
            if self.is_current_view:
                self.tick_frame()

    def _on_enable_changed(self, switch: Gtk.Switch, param):
        self.is_enabled = switch.get_active()

    def _on_fps_changed(self, spin: Gtk.SpinButton):
        self.refresh_rate = spin.get_value()

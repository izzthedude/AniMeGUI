import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from deepface import DeepFace
from gi.repository import GLib, Gtk, GObject, Adw

from animegui.controllers.controller_base import BaseController
from animegui.enums import Paths
from animegui.ui.view_page_live import LivePageView
from animegui.utils.gi_helpers import create_signal
from animegui.utils.task import TaskManager

emojis = {
    "angry": "\U0001F620",
    "disgust": "\U0001F922",
    "fear": "\U0001F631",
    "happy": "\U0001F603",
    "sad": "\U0001F641",
    "surprise": "\U0001F632",
    "neutral": "\U0001F610"
}


class LiveController(BaseController):
    __gtype_name__ = "LiveController"

    TICK = "tanned-neuron"
    DIRECT = 0
    EMOTIONS = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not GObject.signal_list_names(self):
            create_signal(self, self.TICK)

        self._view: LivePageView
        self.cap = cv2.VideoCapture(0)

        self.is_current_view: bool = False
        self.is_enabled: bool = False
        self.modes = {
            "Direct": self.DIRECT,
            "Emotions": self.EMOTIONS
        }
        self.current_mode: int = self.DIRECT
        self.refresh_rate: int = 10

        self.modes_model: Gtk.StringList = Gtk.StringList()
        for key in self.modes.keys():
            self.modes_model.append(key)

        self.task_manager: TaskManager = TaskManager(self._analyse_emotion)
        self.task_manager.set_source(self)

    def set_view(self, view: LivePageView):
        self._view = view

        if not self.cap.isOpened():
            self._view.show_nocam_status()

        self._view.check_camera_btn.connect("clicked", self._on_check_camera)

        self.is_enabled = self._view.enable_switch.get_active()
        self._view.enable_switch.connect("notify::active", self._on_enable_changed)

        self._view.mode_chooser_row.set_model(self.modes_model)
        self._view.mode_chooser_row.connect("notify::selected-item", self._on_mode_selected)

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

            if self.current_mode == self.EMOTIONS and not self.task_manager.is_running():
                self._analyse_emotion()

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

    def _on_mode_selected(self, row: Adw.ComboRow, param):
        selected = row.get_selected_item().get_string()
        self.current_mode = self.modes[selected]

    def _on_fps_changed(self, spin: Gtk.SpinButton):
        self.refresh_rate = spin.get_value()

    def _analyse_emotion(self):
        result = DeepFace.analyze(
            img_path=Paths.FRAME_CACHE,
            actions=("emotion",),
            enforce_detection=False,
            silent=True
        )[0]
        emotion = result["dominant_emotion"]
        emoji = emojis[emotion]
        self._emoji_to_image(emoji)

    def _emoji_to_image(self, emoji: str):
        width, height = 640, 480

        # Initialise some PIL stuff
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(Paths.EMOJI_FONT, size=109)

        # Calculate position and draw it
        fontw, fonth = font.getsize(emoji)
        textx, texty = width // 2 - fontw // 2, height // 2 - fonth // 2
        draw.text((textx, texty), emoji, font=font, embedded_color=True)

        # Save it
        image.save(Paths.FRAME_CACHE)

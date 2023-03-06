import math

from gi.repository import Gtk

from animegui.animepy.data import AniMeData
from animegui.animepy.dbus import AniMeDBus
from animegui.controllers.controller_base import BaseController
from animegui.ui.view_page_general import GeneralPageView


class GeneralController(BaseController):
    __gtype_name__ = "GeneralController"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._view: GeneralPageView
        self._dbus: AniMeDBus = AniMeDBus.instance()
        self._data: AniMeData = AniMeData()

    def get_data(self) -> AniMeData:
        return self._data

    def set_view(self, view: GeneralPageView):
        self._view = view

        # Enable AniMe
        self._view.enable_anime_switch.set_active(self._dbus.AwakeEnabled())
        self._view.enable_anime_switch.connect(
            "notify::active",
            self._on_enable_anime_switch_activated
        )

        # Enable system animations
        self._view.enable_animations_switch.set_active(self._dbus.BootEnabled())
        self._view.enable_animations_switch.connect(
            "notify::active",
            self._on_enable_animations_switch_activated
        )

        # Brightness
        self._view.global_brightness_scale.set_value(1.0)
        self._dbus.SetBrightness(1.0)  # There's no GetBrightness DBus method, so I'll just 'sync' it manually lol
        self._view.global_brightness_scale.connect(
            "value-changed",
            self._on_global_brightness_changed
        )

        # Image/GIF Path
        self._view.file_chooser_row.connect(
            self._view.file_chooser_row.FILE_SELECTED,
            self._on_file_chooser_selected
        )

        # Scale
        self._view.image_scale_button.set_value(1.0)
        self._view.image_scale_button.connect(
            "value-changed",
            self._on_image_scale_changed
        )

        # X Offset
        self._view.offset_x_button.set_value(0.0)
        self._view.offset_x_button.connect(
            "value-changed",
            self._on_x_offset_changed
        )

        # Y Offset
        self._view.offset_y_button.set_value(0.0)
        self._view.offset_y_button.connect(
            "value-changed",
            self._on_y_offset_changed
        )

        # Angle
        self._view.angle_scale.set_value(0)
        self._view.angle_scale.connect(
            "value-changed",
            self._on_angle_changed
        )

        # Brightness
        self._view.brightness_scale.set_value(1.0)
        self._view.brightness_scale.connect(
            "value-changed",
            self._on_brightness_changed
        )

        # Loops
        self._view.loops_button.set_value(1)
        self._view.loops_button.connect(
            "value-changed",
            self._on_loops_changed
        )

    def _on_enable_anime_switch_activated(self, switch: Gtk.Switch, param):
        self._dbus.SetOnOff(switch.get_active())

    def _on_enable_animations_switch_activated(self, switch: Gtk.Switch, param):
        self._dbus.SetBootOnOff(switch.get_active())

    def _on_global_brightness_changed(self, scale: Gtk.Scale):
        self._dbus.SetBrightness(scale.get_value())

    def _on_file_chooser_selected(self, row, path: str):
        self._data.path = path

    def _on_image_scale_changed(self, spin_button: Gtk.SpinButton):
        self._data.scale = spin_button.get_value()

    def _on_x_offset_changed(self, spin_button: Gtk.SpinButton):
        self._data.x_pos = spin_button.get_value()

    def _on_y_offset_changed(self, spin_button: Gtk.SpinButton):
        self._data.y_pos = spin_button.get_value()

    def _on_angle_changed(self, scale: Gtk.Scale):
        degrees = scale.get_value()
        radians = math.radians(degrees)
        self._data.angle = radians

    def _on_brightness_changed(self, scale: Gtk.Scale):
        self._data.bright = scale.get_value()

    def _on_loops_changed(self, spin_button: Gtk.SpinButton):
        self._data.loops = spin_button.get_value()

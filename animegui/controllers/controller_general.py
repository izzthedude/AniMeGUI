import os

from gi.repository import Gtk

from animegui.animepy.data import AniMeData
from animegui.animepy.dbus import AniMeDBus
from animegui.controllers.controller_base import BaseController
from animegui.presets import PresetData
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

    def load_preset(self, preset: PresetData):
        anime = preset.anime
        self._view.file_chooser_row.set_path(anime.path)
        self._view.image_scale_button.set_value(anime.scale)
        self._view.offset_x_button.set_value(anime.x_pos)
        self._view.offset_y_button.set_value(anime.y_pos)
        self._view.angle_scale.set_value(anime.angle)
        self._view.brightness_scale.set_value(anime.bright)
        self._view.loops_button.set_value(anime.loops)

    def update_preset_selector(self, presets: list[PresetData]):
        model = self._view.presets_dropdown.get_model()
        for preset in presets:
            model.append(preset.name)

    def clear_preset_selector(self):
        new_model = Gtk.StringList()
        new_model.append("Load Preset")
        self._view.presets_dropdown.set_model(new_model)

    def _on_enable_anime_switch_activated(self, switch: Gtk.Switch, param):
        self._dbus.SetOnOff(switch.get_active())

    def _on_enable_animations_switch_activated(self, switch: Gtk.Switch, param):
        self._dbus.SetBootOnOff(switch.get_active())

    def _on_global_brightness_changed(self, scale: Gtk.Scale):
        self._dbus.SetBrightness(scale.get_value())

    def _on_file_chooser_selected(self, row, path: str):
        self._data.path = path

        suffix = os.path.basename(path).split(".")[-1]
        visible = False
        if suffix == "gif":
            visible = True
        self._view.loops_row.set_visible(visible)

    def _on_image_scale_changed(self, spin_button: Gtk.SpinButton):
        self._data.scale = spin_button.get_value()

    def _on_x_offset_changed(self, spin_button: Gtk.SpinButton):
        self._data.x_pos = spin_button.get_value()

    def _on_y_offset_changed(self, spin_button: Gtk.SpinButton):
        self._data.y_pos = spin_button.get_value()

    def _on_angle_changed(self, scale: Gtk.Scale):
        degrees = scale.get_value()
        self._data.angle = degrees

    def _on_brightness_changed(self, scale: Gtk.Scale):
        self._data.bright = scale.get_value()

    def _on_loops_changed(self, spin_button: Gtk.SpinButton):
        self._data.loops = spin_button.get_value()

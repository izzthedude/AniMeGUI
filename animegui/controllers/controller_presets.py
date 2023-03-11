from animegui.controllers.controller_base import BaseController
from animegui.presets import PresetData, load_presets, commit_presets
from animegui.ui.view_page_presets import PresetsPageView
from animegui.utils.task import TaskManager
from animegui.widgets.rows import *


class PresetsController(BaseController):
    __gtype_name__ = "PresetsController"

    PRESETS_LOADED = "unclad-radiator"
    PRESETS_CHANGED = "jacket-grafting"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not GObject.signal_list_names(self):
            create_signal(self, self.PRESETS_LOADED, [object])  # Emits list[PresetData]
            create_signal(self, self.PRESETS_CHANGED, [object])  # Emits PresetData

        self._view: PresetsPageView
        self._presets: list[tuple[PresetData, PresetExpanderRow]] = []

    def set_view(self, view: PresetsPageView):
        self._view = view
        self._view.presets_add_button.connect("clicked", self._on_add_button_clicked)

        # Load presets from presets file
        task = TaskManager(load_presets)
        task.set_on_finish(self._load_presets_finish)
        task.start()

    def add_preset(self, preset: PresetData):
        row = self._preset_to_row(preset)
        self._connect_preset_to_row(preset, row)
        self._presets.append((preset, row))
        self._view.add_preset_row(row)
        self.emit(self.PRESETS_CHANGED, self.get_presets())

    def remove_preset(self, preset: PresetData):
        index = self._find_preset(preset)
        pair = self._presets[index]
        self._view.remove_preset_row(pair[1])
        self._presets.remove(pair)
        self.emit(self.PRESETS_CHANGED, self.get_presets())

    def get_presets(self) -> list[PresetData]:
        presets = [preset for preset, row in self._presets]
        return presets

    def get_preset(self, name: str):
        for preset, row in self._presets:
            if preset.name == name:
                return preset

    def commit_presets(self):
        presets = [preset for preset, row in self._presets]
        commit_presets(presets)

    def _load_presets_finish(self, presets: list[PresetData]):
        for preset in presets:
            self.add_preset(preset)
        self.emit(self.PRESETS_LOADED, [preset for preset, row in self._presets])

    def _on_add_button_clicked(self, button: Gtk.Button):
        preset = PresetData.placeholder()
        preset.name = f"Preset {len(self._presets) + 1}"
        self.add_preset(preset)

    def _preset_to_row(self, preset: PresetData):
        return PresetExpanderRow(**preset.convert_to_dict())

    def _find_preset(self, preset: PresetData):
        for i, (p, row) in enumerate(self._presets):
            if p is preset:
                return i

    def _connect_preset_to_row(self, preset: PresetData, row: PresetExpanderRow):
        row.delete_button.connect("clicked", self._on_delete_row, preset, row)
        row.name_row.entry.connect("changed", self._on_name_changed, preset)
        row.path_row.connect(row.path_row.FILE_SELECTED, self._on_path_changed, preset)
        row.scale_row.spin_button.connect("value-changed", self._on_scale_changed, preset)
        row.offset_x_row.spin_button.connect("value-changed", self._on_offset_x_changed, preset)
        row.offset_y_row.spin_button.connect("value-changed", self._on_offset_y_changed, preset)
        row.angle_row.scale.connect("value-changed", self._on_angle_changed, preset)
        row.brightness_row.scale.connect("value-changed", self._on_brightness_changed, preset)
        row.loops_row.spin_button.connect("value-changed", self._on_loops_changed, preset)

    def _on_delete_row(self, button: Gtk.Button, preset: PresetData, row: PresetExpanderRow):
        self.remove_preset(preset)

    def _on_name_changed(self, entry: Gtk.Entry, preset: PresetData):
        name = entry.get_text()
        preset.name = name
        self.emit(self.PRESETS_CHANGED, self.get_presets())  # Jank solution

    def _on_path_changed(self, row: ImagePathParameter, path: str, preset: PresetData):
        preset.anime.path = path

    def _on_scale_changed(self, spin: Gtk.SpinButton, preset: PresetData):
        img_scale = spin.get_value()
        preset.anime.scale = img_scale

    def _on_offset_x_changed(self, spin: Gtk.SpinButton, preset: PresetData):
        x_pos = spin.get_value()
        preset.anime.x_pos = x_pos

    def _on_offset_y_changed(self, spin: Gtk.SpinButton, preset: PresetData):
        y_pos = spin.get_value()
        preset.anime.y_pos = y_pos

    def _on_angle_changed(self, scale: Gtk.Scale, preset: PresetData):
        angle = scale.get_value()
        preset.anime.angle = angle

    def _on_brightness_changed(self, scale: Gtk.Scale, preset: PresetData):
        bright = scale.get_value()
        preset.anime.bright = bright

    def _on_loops_changed(self, spin: Gtk.SpinButton, preset: PresetData):
        loops = spin.get_value()
        preset.anime.loops = loops

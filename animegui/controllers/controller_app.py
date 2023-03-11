import math

from gi.repository import Gio, GObject, Gtk

from animegui.animepy.cli import AniMeCLI
from animegui.controllers.controller_base import BaseController
from animegui.controllers.controller_general import GeneralController
from animegui.controllers.controller_presets import PresetsController
from animegui.presets import PresetData
from animegui.ui.window_app import AniMeGUIAppWindow
from animegui.utils.gi_helpers import create_action


class AppController(BaseController):
    __gtype_name__ = "AppController"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._cli: AniMeCLI = AniMeCLI.instance()

        # The 'view' for the AppController is AniMeGUIAppWindow, set in app.py
        self._view: AniMeGUIAppWindow
        self._general_controller: GeneralController = GeneralController.instance()
        self._presets_controller: PresetsController = PresetsController.instance()

    def set_view(self, view: AniMeGUIAppWindow):
        self._view = view
        create_action(self._view, "stop-anime", self._on_stop_anime)
        create_action(self._view, "start-anime", self._on_start_anime)
        create_action(self._view, "clear-anime", self._on_clear_anime)

        # Bind button properties
        self._view.stop_btn.bind_property(
            "visible",
            self._view.start_btn,
            "visible",
            GObject.BindingFlags.BIDIRECTIONAL | GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.INVERT_BOOLEAN
        )

        self._general_controller.set_view(self._view.general_view)
        self._presets_controller.set_view(self._view.presets_view)

        self._presets_controller.connect(self._presets_controller.PRESETS_LOADED, self._on_presets_loaded)
        self._presets_controller.connect(self._presets_controller.PRESETS_CHANGED, self._on_presets_loaded)
        # TODO: Janky solution, try to use the 'activate' signal when it actually works

        self._view.general_view.presets_dropdown_model.append("Load Preset")
        self._view.general_view.presets_dropdown.connect("notify::selected-item", self._on_dropdown_selected)
        # self._view.general_view.presets_dropdown.connect("activate", self._on_presets_loaded)

    def on_shutdown(self):
        self._presets_controller.commit_presets()

    def _on_stop_anime(self, action: Gio.SimpleAction, params):
        self._cli.terminate()
        self._view.start_btn.set_visible(True)

    def _on_start_anime(self, action: Gio.SimpleAction, params):
        data = self._general_controller.get_data()
        data.angle = math.radians(data.angle)  # Convert from degrees to radians

        for key, value in data:
            self._cli.set_arg(key, value)

        self._cli.run()
        self._view.stop_btn.set_visible(True)

    def _on_clear_anime(self, action: Gio.SimpleAction, params):
        while self._cli.is_running():
            self._cli.terminate()
        self._cli.clear()
        self._view.start_btn.set_visible(True)

    def _on_presets_loaded(self, controller: PresetsController, presets: list[PresetData]):
        self._view.general_view.presets_dropdown.freeze_notify()
        self._general_controller.clear_preset_selector()
        self._general_controller.update_preset_selector(presets)
        self._view.general_view.presets_dropdown.thaw_notify()

    def _on_dropdown_selected(self, dropdown: Gtk.DropDown, _):
        value: str = dropdown.get_selected_item().get_string()
        if value != "Load Preset":
            preset = self._presets_controller.get_preset(value)
            self._general_controller.load_preset(preset)

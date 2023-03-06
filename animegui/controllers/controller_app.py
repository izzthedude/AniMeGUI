from gi.repository import Gio, GObject

from animegui.animepy.cli import AniMeCLI
from animegui.controllers.controller_base import BaseController
from animegui.controllers.controller_general import GeneralController
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

    def _on_stop_anime(self, action: Gio.SimpleAction, params):
        self._cli.terminate()
        self._view.start_btn.set_visible(True)

    def _on_start_anime(self, action: Gio.SimpleAction, params):
        data = self._general_controller.get_data()
        for key, value in data:
            self._cli.set_arg(key, value)

        self._cli.run()
        self._view.stop_btn.set_visible(True)

    def _on_clear_anime(self, action: Gio.SimpleAction, params):
        while self._cli.is_running():
            self._cli.terminate()
        self._cli.clear()
        self._view.start_btn.set_visible(True)

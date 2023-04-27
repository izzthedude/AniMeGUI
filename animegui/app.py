# app.py
#
# Copyright 2022 Izzat Z.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gio, Adw, Gtk

from animegui.controllers.controller_app import AppController
from animegui.ui import AniMeGUIAppWindow
from animegui.utils.gi_helpers import create_action


class AniMeGUIApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="io.github.izzthedude.AniMeGUI",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        self.app_controller = AppController.instance()
        self.connect("shutdown", self.on_shutdown)

        create_action(self, "preferences", self.on_preferences_action, ["<primary>comma"])
        create_action(self, "about", self.on_about_action)
        create_action(self, "quit", self.on_quit_action, ["<primary>q"])

    def do_activate(self):
        app_window = self.props.active_window
        if not app_window:
            app_window = AniMeGUIAppWindow(application=self)
            self.app_controller.set_view(app_window)
            self.set_accels_for_action("win.show-help-overlay", ["<primary>question"])
        app_window.present()

    def on_shutdown(self, app):
        self.app_controller.on_shutdown()

    def on_preferences_action(self, action: Gio.SimpleAction, param):
        print("app.preferences action activated")

    def on_about_action(self, action: Gio.SimpleAction, param):
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="AniMeGUI",
            application_icon="io.github.izzthedude.AniMeGUI",
            developer_name="Izzat Z.",
            version="0.1.0",
            developers=["Izzat Z. https://github.com/izzthedude"],
            copyright="© 2022 Izzat Z.",
            license_type=Gtk.License.GPL_3_0,
            website="https://github.com/izzthedude/AniMeGUI",
            issue_url="https://github.com/izzthedude/AniMeGUI/issues",
        )
        about.present()

    def on_quit_action(self, action: Gio.SimpleAction, param):
        self.quit()


def main(version):
    app = AniMeGUIApplication()
    return app.run(sys.argv)

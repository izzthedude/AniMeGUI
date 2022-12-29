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
from gi.repository import Gio, Adw

from animegui.ui import AniMeGUIAppWindow


class AniMeGUIApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="com.github.izzthedude.AniMeGUI",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

        self.create_action("preferences", self.on_preferences_action, ["<primary>comma"])
        self.create_action("about", self.on_about_action)
        self.create_action("quit", self.on_quit_action, ["<primary>q"])

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = AniMeGUIAppWindow(application=self)
            self.set_accels_for_action("win.show-help-overlay", ["<primary>question"])
        win.present()

    def on_preferences_action(self, action: Gio.SimpleAction, param):
        print("app.preferences action activated")

    def on_about_action(self, action: Gio.SimpleAction, param):
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="animegui",
            application_icon="com.github.izzthedude.AniMeGUI",
            developer_name="Izzat Z.",
            version="0.1.0",
            developers=["Izzat Z."],
            copyright="© 2022 Izzat Z.")
        about.present()

    def on_quit_action(self, action: Gio.SimpleAction, param):
        self.quit()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    app = AniMeGUIApplication()
    return app.run(sys.argv)

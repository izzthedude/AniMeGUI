# window_app.py
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

from gi.repository import Adw, Gtk

from animegui.ui.view_base import BasePageView
from animegui.ui.view_page_general import GeneralPageView
from animegui.ui.view_page_live import LivePageView
from animegui.ui.view_page_presets import PresetsPageView


@Gtk.Template(resource_path="/com/github/izzthedude/AniMeGUI/ui/app-window")
class AniMeGUIAppWindow(Adw.ApplicationWindow):
    __gtype_name__ = "AniMeGUIAppWindow"

    header_bar: Adw.HeaderBar = Gtk.Template.Child()
    header_title_box: Gtk.Box = Gtk.Template.Child()

    switcher_title: Adw.ViewSwitcherTitle = Gtk.Template.Child()
    content_stack: Adw.ViewStack = Gtk.Template.Child()

    general_view: GeneralPageView = GeneralPageView()
    presets_view: PresetsPageView = PresetsPageView()
    live_view: LivePageView = LivePageView()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._setup_help_overlay()
        self._add_views(self.general_view, self.presets_view, self.live_view)

    def _add_views(self, *args: BasePageView):
        for view in args:
            name, title, icon = view._define_stackpage()
            self.content_stack.add_titled_with_icon(view, name, title, icon)

    def _setup_help_overlay(self):
        builder: Gtk.Builder = Gtk.Builder.new_from_resource("/com/github/izzthedude/AniMeGUI/ui/help-overlay")
        shortcuts_window: Gtk.ShortcutsWindow = builder.get_object("help_overlay")
        self.set_help_overlay(shortcuts_window)

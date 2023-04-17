import os

import cairo as cr
from gi.repository import Adw, Gtk, Gdk, GdkPixbuf

from animegui.enums import Paths
from animegui.ui.view_page_base import BasePageView
from animegui.utils.gi_helpers import fill_rect
from animegui.widgets.rows import SpinButtonActionRow, SwitchActionRow


class LivePageView(BasePageView):
    __gtype_name__ = "LivePageView"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_preview_section()
        self._init_settings_section()

    def _init_preview_section(self):
        self.preview_box: Gtk.Box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
            hexpand=True,
        )
        self.add_widget(self.preview_box)

        self.draw_area: Gtk.DrawingArea = Gtk.DrawingArea()
        self.draw_area.set_size_request(self.draw_area.get_width(), 420)
        self.draw_area.set_draw_func(self._draw_func)

        self.preview_label = Gtk.Label(label="Preview")
        self.preview_label.add_css_class("title-2")

        self.preview_box.append(self.draw_area)
        self.preview_box.append(self.preview_label)

    def _init_settings_section(self):
        self.settings_group: Adw.PreferencesGroup = Adw.PreferencesGroup()
        self.add_widget(self.settings_group)

        # Enable Live Mode
        self.enable_row: SwitchActionRow = SwitchActionRow(
            self.settings_group,
            "Live Mode",
            "Enable Live Mode. This will immediately write to AniMe as soon as it is enabled."
        )
        self.enable_switch: Gtk.Switch = self.enable_row.switch

        # Camera Device Chooser
        # Due to technical limitations, this will be commented out
        # self.device_chooser_row: Adw.ComboRow = Adw.ComboRow(
        #     title="Device",
        #     subtitle="Choose camera device"
        # )
        # self.settings_group.add(self.device_chooser_row)

        # Refresh Rate
        self.fps_row: SpinButtonActionRow = SpinButtonActionRow(
            self.settings_group,
            "Refresh Rate",
            "The refresh rate of the camera in frames per second"
        )
        self.fps_spin: Gtk.SpinButton = self.fps_row.spin_button

    def _draw_func(self, area: Gtk.DrawingArea, cairo: cr.Context, width: int, height: int):
        # Draw background
        fill_rect(cairo, width, height, 0, 0, "black")

        # Draw current frame
        if os.path.exists(Paths.FRAME_CACHE):
            Gdk.cairo_set_source_pixbuf(
                cairo, GdkPixbuf.Pixbuf.new_from_file(Paths.FRAME_CACHE),
                0, 0
            )
            cairo.paint()

    def _define_stackpage(self) -> tuple[str, str, str]:
        return "live_page_view", "Live", "camera-photo-symbolic"

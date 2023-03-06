from animegui.ui.view_page_base import BasePageView
from animegui.widgets.rows import *


class PresetsPageView(BasePageView):
    __gtype_name__ = "PresetsPageView"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.debug_label.set_visible(True)

        self._init_presets_group()

    def _init_presets_group(self):
        self.presets_group: Adw.PreferencesGroup = Adw.PreferencesGroup(
            title="Presets",
            description="User-configurable presets of AniMe animations"
        )
        self.presets_group_suffix_box: Gtk.Box = Gtk.Box(valign=Gtk.Align.CENTER)
        self.presets_add_button: Gtk.Button = Gtk.Button(icon_name="list-add-symbolic")
        self.presets_group_suffix_box.append(self.presets_add_button)
        self.presets_group.set_header_suffix(self.presets_group_suffix_box)
        self.add_widget(self.presets_group)

        debug_preset: PresetExpanderRow = PresetExpanderRow(
            self.presets_group,
            "Debug Preset",
            "/home/user/Downloads/debug.png",
            1.0,
            0,
            0,
            0,
            1.0,
            10
        )

    def _define_stackpage(self) -> tuple[str, str, str]:
        return "presets_page_view", "Presets", "open-book-symbolic"

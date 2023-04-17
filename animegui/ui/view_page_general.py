from animegui.ui.view_page_base import BasePageView
from animegui.widgets.rows import *


class GeneralPageView(BasePageView):
    __gtype_name__ = "GeneralPageView"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.debug_label.set_visible(True)

        self._init_global_group()
        self._init_parameters_group()

    def _init_global_group(self):
        # Initialise Global settings group
        self.global_group: Adw.PreferencesGroup = Adw.PreferencesGroup(
            title="Global",
            description="Global settings for AniMe"
        )
        self.add_widget(self.global_group)

        # Initialise Enable AniMe row
        self.enable_anime_row: SwitchActionRow = SwitchActionRow(
            self.global_group,
            "Enable AniMe",
            "Toggle AniMe display on/off (does not erase the last image)"
        )
        self.enable_anime_switch: Gtk.Switch = self.enable_anime_row.switch

        # Initialise system animations row
        self.enable_animations_row: SwitchActionRow = SwitchActionRow(
            self.global_group,
            "Enable system animations",
            "Toggle system animations (boot/sleep/shutdown)"
        )
        self.enable_animations_switch: Gtk.Switch = self.enable_animations_row.switch

        # Initialise global brightness row
        self.global_brightness_row: BrightnessParameter = BrightnessParameter(self.global_group)
        self.global_brightness_row.set_subtitle("Set global brightness of the AniMe display")
        self.global_brightness_scale: Gtk.Scale = self.global_brightness_row.scale

    def _init_parameters_group(self):
        # Initialise Parameters group
        self.parameters_group: Adw.PreferencesGroup = Adw.PreferencesGroup(
            title="Parameters",
            description="Values to set for the AniMe display animation"
        )

        self.presets_dropdown: Gtk.DropDown = Gtk.DropDown()
        self.presets_dropdown_model: Gtk.StringList = Gtk.StringList()
        self.presets_dropdown.set_model(self.presets_dropdown_model)

        self.parameters_group.set_header_suffix(self.presets_dropdown)
        self.add_widget(self.parameters_group)

        # Initialise file chooser row
        self.file_chooser_row: ImagePathParameter = ImagePathParameter(self.parameters_group)
        self.file_chooser_button: Gtk.Button = self.file_chooser_row.button

        # Initialise scale row
        self.image_scale: ScaleParameter = ScaleParameter(self.parameters_group)
        self.image_scale_button: Gtk.SpinButton = self.image_scale.spin_button

        # Initialise X Offset row
        self.offset_x_row: XOffsetParameter = XOffsetParameter(self.parameters_group)
        self.offset_x_button: Gtk.SpinButton = self.offset_x_row.spin_button

        # Initialise X Offset row
        self.offset_y_row: YOffsetParameter = YOffsetParameter(self.parameters_group)
        self.offset_y_button: Gtk.SpinButton = self.offset_y_row.spin_button

        # Initialise Angle row
        self.angle_row: AngleParameter = AngleParameter(self.parameters_group)
        self.angle_scale: Gtk.Scale = self.angle_row.scale

        # Initialise Brightness row
        self.brightness_row: BrightnessParameter = BrightnessParameter(self.parameters_group)
        self.brightness_scale: Gtk.Scale = self.brightness_row.scale

        # Initialise Loops row
        self.loops_row: LoopsParameter = LoopsParameter(self.parameters_group)
        self.loops_button: Gtk.SpinButton = self.loops_row.spin_button
        self.loops_row.set_visible(False)

    def _define_stackpage(self) -> tuple[str, str, str]:
        return "general_page-view", "General", "tv-symbolic"

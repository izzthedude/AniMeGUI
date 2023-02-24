from animegui.ui.view_page_base import BasePageView
from animegui.widgets.action_rows import *


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
        self.global_brightness_row: ScaleActionRow = ScaleActionRow(
            self.global_group,
            "Brightness",
            "Set global brightness of the AniMe display"
        )
        self.global_brightness_scale: Gtk.Scale = self.global_brightness_row.scale

    def _init_parameters_group(self):
        # Initialise Parameters group
        self.parameters_group: Adw.PreferencesGroup = Adw.PreferencesGroup(
            title="Parameters",
            description="Values to set for the AniMe display animation"
        )
        self.presets_dropdown: Gtk.DropDown = Gtk.DropDown()
        self.presets_dropdown_model: Gtk.StringList = Gtk.StringList()
        self.presets_dropdown_model.append("Load Preset")
        for i in range(3):
            self.presets_dropdown_model.append(f"Debug {i + 1}")
        self.presets_dropdown.set_model(self.presets_dropdown_model)

        self.parameters_group.set_header_suffix(self.presets_dropdown)
        self.add_widget(self.parameters_group)

        # Initialise file chooser row
        self.file_chooser_row: ButtonActionRow = ButtonActionRow(
            self.parameters_group,
            "Image/GIF Path",
            "Path to the image or GIF file that will be displayed",
        )
        self.file_chooser_button: Gtk.Button = self.file_chooser_row.button
        self.file_chooser_button.set_icon_name("folder-symbolic")

        # Initialise scale row
        self.image_scale: SpinButtonActionRow = SpinButtonActionRow(
            self.parameters_group,
            "Scale",
            "Scale of the image or GIF",
        )
        self.image_scale_button: Gtk.SpinButton = self.image_scale.spin_button

        # Initialise X Offset row
        self.offset_x_row: SpinButtonActionRow = SpinButtonActionRow(
            self.parameters_group,
            "X Offset",
            "The offset of the image in the x-axis"
        )
        self.offset_x_button: Gtk.SpinButton = self.offset_x_row.spin_button
        self.offset_x_button.set_digits(0)
        self.offset_x_button.set_range(-500, 500)
        self.offset_x_button.set_increments(1, 1)

        # Initialise X Offset row
        self.offset_y_row: SpinButtonActionRow = SpinButtonActionRow(
            self.parameters_group,
            "Y Offset",
            "The offset of the image in the y-axis"
        )
        self.offset_y_button: Gtk.SpinButton = self.offset_y_row.spin_button
        self.offset_y_button.set_digits(0)
        self.offset_y_button.set_range(-500, 500)
        self.offset_y_button.set_increments(1, 1)

        # Initialise Angle row
        self.angle_row: ScaleActionRow = ScaleActionRow(
            self.parameters_group,
            "Angle (Degrees)",
            "The angle of the image or GIF in degrees"
        )
        self.angle_scale: Gtk.Scale = self.angle_row.scale
        self.angle_scale.set_digits(0)
        self.angle_scale.set_range(-180, 180)
        self.angle_scale.set_increments(1, 1)

        # Initialise Brightness row
        self.brightness_row: ScaleActionRow = ScaleActionRow(
            self.parameters_group,
            "Brightness",
            "Set brightness of the AniMe display"
        )
        self.brightness_scale: Gtk.Scale = self.brightness_row.scale

        # Initialise Loops row
        self.loops_row: SpinButtonActionRow = SpinButtonActionRow(
            self.parameters_group,
            "Loops",
            "The number of loops of an animation (only applicable to GIFs)"
        )
        self.loops_button: Gtk.SpinButton = self.loops_row.spin_button
        self.loops_button.set_digits(0)
        self.loops_button.set_range(0, 100)
        self.loops_button.set_increments(1, 1)

    def _define_stackpage(self) -> tuple[str, str, str]:
        return "general_page-view", "General", "tv-symbolic"

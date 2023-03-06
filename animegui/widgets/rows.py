import os

from gi.repository import Adw, Gtk, GObject

from animegui.utils.gi_helpers import create_signal


class BaseActionRow(Adw.ActionRow):
    def __init__(
            self,
            parent_group: Adw.PreferencesGroup | Adw.ExpanderRow,
            title: str,
            subtitle: str,
            suffix_widget: Gtk.Widget,
            activatable_widget: Gtk.Widget,
            **kwargs):
        super().__init__(**kwargs)

        # Set some stuff
        self.set_title(title)
        self.set_subtitle(subtitle)
        self.set_activatable(True)

        # Add widgets
        self.add_suffix(suffix_widget)
        self.set_activatable_widget(activatable_widget)

        if isinstance(parent_group, Adw.PreferencesGroup):
            parent_group.add(self)
        elif isinstance(parent_group, Adw.ExpanderRow):
            parent_group.add_row(self)


class SwitchActionRow(BaseActionRow):
    def __init__(
            self,
            parent_group: Adw.PreferencesGroup | Adw.ExpanderRow,
            title: str,
            subtitle: str,
            **kwargs):
        self.switch_box: Gtk.Box = Gtk.Box(valign=Gtk.Align.CENTER)
        self.switch: Gtk.Switch = Gtk.Switch()
        self.switch_box.append(self.switch)

        super().__init__(parent_group, title, subtitle, self.switch_box, self.switch, **kwargs)


class ScaleActionRow(BaseActionRow):
    def __init__(
            self,
            parent_group: Adw.PreferencesGroup | Adw.ExpanderRow,
            title: str,
            subtitle: str,
            **kwargs):
        self.box: Gtk.Box = Gtk.Box()

        self.scale: Gtk.Scale = Gtk.Scale(hexpand=True)
        self.scale.set_digits(1)
        self.scale.set_range(0, 1)
        self.scale.set_increments(0.1, 0.1)
        self.scale.set_draw_value(True)
        self.box.append(self.scale)

        super().__init__(parent_group, title, subtitle, self.box, None, **kwargs)


class ButtonActionRow(BaseActionRow):
    def __init__(
            self,
            parent_group: Adw.PreferencesGroup | Adw.ExpanderRow,
            title: str,
            subtitle: str,
            **kwargs):
        self.box: Gtk.Box = Gtk.Box(
            valign=Gtk.Align.CENTER,
            spacing=10
        )
        self.label: Gtk.Label = Gtk.Label()
        self.label.add_css_class("dim-label")
        self.button: Gtk.Button = Gtk.Button()

        self.box.append(self.label)
        self.box.append(self.button)

        super().__init__(parent_group, title, subtitle, self.box, self.button, **kwargs)


class SpinButtonActionRow(BaseActionRow):
    def __init__(
            self,
            parent_group: Adw.PreferencesGroup | Adw.ExpanderRow,
            title: str,
            subtitle: str,
            **kwargs):
        self.box: Gtk.Box = Gtk.Box(valign=Gtk.Align.CENTER)

        self.spin_button: Gtk.SpinButton = Gtk.SpinButton()
        self.spin_button.set_digits(1)
        self.spin_button.set_range(0.1, 20.0)
        self.spin_button.set_increments(0.1, 0.1)

        self.box.append(self.spin_button)

        super().__init__(parent_group, title, subtitle, self.box, None, **kwargs)


class EntryActionRow(BaseActionRow):
    def __init__(
            self,
            parent_group: Adw.PreferencesGroup | Adw.ExpanderRow,
            title: str,
            subtitle: str,
            **kwargs):
        self.box: Gtk.Box = Gtk.Box(valign=Gtk.Align.CENTER)
        self.entry: Gtk.Entry = Gtk.Entry()
        self.box.append(self.entry)

        super().__init__(parent_group, title, subtitle, self.box, None)


class NameParameter(EntryActionRow):
    def __init__(
            self,
            parent_group: Adw.ExpanderRow,
            **kwargs):
        super().__init__(
            parent_group,
            "Name",
            "Name of this preset"
        )


class ImagePathParameter(ButtonActionRow):
    FILE_SELECTED = "gummy-calcium"

    def __init__(self, parent_group: Adw.PreferencesGroup | Adw.ExpanderRow, **kwargs):
        super().__init__(
            parent_group,
            "Image/GIF Path",
            "Path to the image or GIF file that will be displayed",
            **kwargs
        )
        if not GObject.signal_list_names(self):
            create_signal(self, self.FILE_SELECTED, [str])

        self.parent_window = None
        self.button.set_icon_name("folder-symbolic")
        self.button.connect("clicked", self._on_button_clicked)
        self.path: str = ""

    def get_path(self):
        return self.path

    def set_path(self, path: str):
        self.label.set_label(os.path.basename(path))
        self.label.set_tooltip_text(path)

    def set_transient_for(self, window: Adw.ApplicationWindow):
        self.parent_window = window

    def _on_button_clicked(self, button: Gtk.Button):
        self._dialog = Gtk.FileChooserDialog(
            title="Choose PNG image or GIF",
            transient_for=self.parent_window,
            action=Gtk.FileChooserAction.OPEN,
        )
        self._dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self._dialog.add_button("_Select", Gtk.ResponseType.ACCEPT)

        png_filter = Gtk.FileFilter()
        png_filter.set_name("PNG")
        png_filter.add_mime_type("image/png")
        gif_filter = Gtk.FileFilter()
        gif_filter.set_name("GIF")
        gif_filter.add_mime_type("image/gif")
        self._dialog.add_filter(png_filter)
        self._dialog.add_filter(gif_filter)

        self._dialog.connect("response", self._on_file_chooser_response)
        self._dialog.show()

    def _on_file_chooser_response(self, dialog: Gtk.FileChooserNative, response: int):
        if response == Gtk.ResponseType.ACCEPT:
            self.path = dialog.get_file().get_path()
            self.set_path(self.path)
            self.emit(self.FILE_SELECTED, self.path)

        dialog.destroy()
        del self._dialog


class ScaleParameter(SpinButtonActionRow):
    def __init__(
            self,
            parent_group: Adw.PreferencesGroup | Adw.ExpanderRow,
            **kwargs,
    ):
        super().__init__(
            parent_group,
            "Scale",
            "Scale of the image or GIF",
            **kwargs
        )


class XOffsetParameter(SpinButtonActionRow):
    def __init__(
            self,
            parent_group: Adw.PreferencesGroup | Adw.ExpanderRow,
            **kwargs,
    ):
        super().__init__(
            parent_group,
            "X Offset",
            "The offset of the image in the x-axis",
            **kwargs
        )


class YOffsetParameter(SpinButtonActionRow):
    def __init__(
            self,
            parent_group: Adw.PreferencesGroup | Adw.ExpanderRow,
            **kwargs,
    ):
        super().__init__(
            parent_group,
            "Y Offset",
            "The offset of the image in the y-axis",
            **kwargs
        )


class AngleParameter(ScaleActionRow):
    def __init__(
            self,
            parent_group: Adw.PreferencesGroup | Adw.ExpanderRow,
            **kwargs,
    ):
        super().__init__(
            parent_group,
            "Angle (Degrees)",
            "The angle of the image or GIF in degrees",
            **kwargs
        )
        self.scale.set_digits(0)
        self.scale.set_range(-180, 180)
        self.scale.set_increments(1, 1)


class BrightnessParameter(ScaleActionRow):
    def __init__(
            self,
            parent_group: Adw.PreferencesGroup | Adw.ExpanderRow,
            **kwargs,
    ):
        super().__init__(
            parent_group,
            "Brightness",
            "Set brightness of the AniMe display",
            **kwargs,
        )


class LoopsParameter(SpinButtonActionRow):
    def __init__(
            self,
            parent_group: Adw.PreferencesGroup | Adw.ExpanderRow,
            **kwargs,
    ):
        super().__init__(
            parent_group,
            "Loops",
            "The number of loops of an animation (only applicable to GIFs)",
            **kwargs
        )
        self.spin_button.set_digits(0)
        self.spin_button.set_range(0, 100)
        self.spin_button.set_increments(1, 1)


class PresetExpanderRow(Adw.ExpanderRow):
    def __init__(
            self,
            parent_group: Adw.PreferencesGroup,
            name: str,
            path: str,
            scale: float,
            x_pos: float,
            y_pos: float,
            angle: int,
            bright: float,
            loops: int,
            **kwargs):
        super().__init__(**kwargs)

        self.set_title(name)

        # Initialise rows
        self.name_row: NameParameter = NameParameter(self)
        self.path_row: ImagePathParameter = ImagePathParameter(self)
        self.scale_row: ScaleParameter = ScaleParameter(self)
        self.offset_x_row: XOffsetParameter = XOffsetParameter(self)
        self.offset_y_row: YOffsetParameter = YOffsetParameter(self)
        self.angle_row: AngleParameter = AngleParameter(self)
        self.brightness_row: BrightnessParameter = BrightnessParameter(self)
        self.loops_row: LoopsParameter = LoopsParameter(self)

        # Set values
        self.name_row.entry.set_text(name)
        self.path_row.set_path(path)
        self.scale_row.spin_button.set_value(scale)
        self.offset_x_row.spin_button.set_value(x_pos)
        self.offset_y_row.spin_button.set_value(y_pos)
        self.angle_row.scale.set_value(angle)
        self.brightness_row.scale.set_value(bright)
        self.loops_row.spin_button.set_value(loops)

        parent_group.add(self)

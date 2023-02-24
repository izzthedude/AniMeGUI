from gi.repository import Adw, Gtk


class BaseActionRow(Adw.ActionRow):
    def __init__(
            self,
            parent_group: Adw.PreferencesGroup,
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
        parent_group.add(self)


class SwitchActionRow(BaseActionRow):
    def __init__(
            self,
            parent_group: Adw.PreferencesGroup,
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
            parent_group: Adw.PreferencesGroup,
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
            parent_group: Adw.PreferencesGroup,
            title: str,
            subtitle: str,
            **kwargs):
        self.box: Gtk.Box = Gtk.Box(
            valign=Gtk.Align.CENTER,
            spacing=5
        )
        self.label: Gtk.Label = Gtk.Label()
        self.label.add_css_class("dim-label")
        self.button: Gtk.Button = Gtk.Button()

        self.box.append(self.label)
        self.box.append(self.button)

        super().__init__(parent_group, title, subtitle, self.box, None, **kwargs)


class SpinButtonActionRow(BaseActionRow):
    def __init__(
            self,
            parent_group: Adw.PreferencesGroup,
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

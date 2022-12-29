from gi.repository import Gio, GLib, Gtk


def create_action(self: Gtk.Application | Gtk.ApplicationWindow, name: str, callback, shortcuts: list = None):
    action = Gio.SimpleAction.new(name, None)
    action.connect("activate", callback)
    self.add_action(action)

    if shortcuts:
        app = self
        origin = "app"
        if isinstance(app, Gtk.ApplicationWindow):
            app = self.get_application()
            origin = "win"

        app.set_accels_for_action(f"{origin}.{name}", shortcuts)


def get_variant(value):
    if isinstance(value, bool):
        return GLib.Variant.new_boolean(value)

    if isinstance(value, float):
        return GLib.Variant.new_double(value)

    if isinstance(value, int):
        return GLib.Variant.new_int16(value)

import cairo as cr
from gi.repository import Gio, GLib, Gtk, GObject, Gdk


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


def create_signal(source: GObject.Object, name: str, param_types: list = []):
    GObject.signal_new(
        name,  # Signal message
        source,  # A Python GObject instance or type that the signal is associated with
        GObject.SignalFlags.RUN_LAST,  # Signal flags
        GObject.TYPE_BOOLEAN,  # Return type of the signal handler
        param_types  # Parameter types
    )


def fill_rect(context: cr.Context, x: int, y: int, width: int, height: int, color: str = "black"):
    rgba = Gdk.RGBA()
    rgba.parse(color)
    context.set_source_rgba(rgba.red, rgba.green, rgba.blue, rgba.alpha)
    context.rectangle(x, y, width, height)
    context.fill()


def get_variant(value):
    if isinstance(value, bool):
        return GLib.Variant.new_boolean(value)

    if isinstance(value, float):
        return GLib.Variant.new_double(value)

    if isinstance(value, int):
        return GLib.Variant.new_int16(value)

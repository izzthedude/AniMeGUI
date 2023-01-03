from gi.repository import Gio, GLib, GObject

from animegui.utils.gi_helpers import get_variant


class AniMeDBus:
    DBUS_NAME = "org.asuslinux.Daemon"
    OBJECT_PATH = "/org/asuslinux/Anime"

    def __init__(self):
        self.proxy: Gio.DBusProxy = Gio.DBusProxy.new_for_bus(
            Gio.BusType.SYSTEM,
            Gio.DBusProxyFlags.NONE,
            None,
            self.DBUS_NAME,
            self.OBJECT_PATH,
            self.DBUS_NAME,
            None,
            self._on_proxy_ready,
            None
        )

    def RunMainLoop(self, start: bool):
        self._call("RunMainLoop", start)

    def SetBootOnOff(self, on: bool):
        self._call("SetBootOnOff", on)

    def SetBrightness(self, brightness: float):
        self._call("SetBrightness", brightness)

    def SetOnOff(self, status: bool):
        self._call("SetOnOff", status)

    # def Write(self, data: object):
    #     pass

    def AwakeEnabled(self):
        return self.proxy.get_cached_property("AwakeEnabled")

    def BootEnabled(self):
        return self.proxy.get_cached_property("BootEnabled")

    def _on_proxy_ready(self, proxy: Gio.DBusProxy, task: Gio.Task, data):
        self.proxy = proxy

    def _call(self, name, *args):
        variant_args = tuple(get_variant(p) for p in args)
        parameters = GLib.Variant.new_tuple(*variant_args) if args else None

        try:
            self.proxy.call(
                name,
                parameters,
                Gio.DBusCallFlags.NONE,
                GObject.G_MAXINT,
                None,
                self._on_call_finished,
                None
            )

        except Exception as err:
            print(err)

    def _on_call_finished(self, proxy: Gio.DBusProxy, task: Gio.Task, data):
        pass

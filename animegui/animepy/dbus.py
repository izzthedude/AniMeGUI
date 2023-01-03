from gi.repository import Gio, GLib, GObject

from animegui.utils.gi_helpers import get_variant


class AniMeDBus:
    DBUS_NAME = "org.asuslinux.Daemon"
    OBJECT_PATH = "/org/asuslinux/Anime"

    def __init__(self):
        self.proxy: Gio.DBusProxy = None

        Gio.DBusProxy.new_for_bus(
            Gio.BusType.SYSTEM,
            Gio.DBusProxyFlags.NONE,
            None,
            self.DBUS_NAME,
            self.OBJECT_PATH,
            self.DBUS_NAME,
            None,
            self.__on_proxy_ready,
            None
        )

    def RunMainLoop(self, start: bool):
        self.__call("RunMainLoop", start)

    def SetBootOnOff(self, on: bool):
        self.__call("SetBootOnOff", on)

    def SetBrightness(self, brightness: float):
        self.__call("SetBrightness", brightness)

    def SetOnOff(self, status: bool):
        self.__call("SetOnOff", status)

    # def Write(self, data: object):
    #     pass

    def AwakeEnabled(self):
        return self.proxy.get_cached_property("AwakeEnabled")

    def BootEnabled(self):
        return self.proxy.get_cached_property("BootEnabled")

    def __on_proxy_ready(self, source: Gio.DBusProxy, result: Gio.Task, data):
        self.proxy: Gio.DBusProxy = Gio.DBusProxy.new_for_bus_finish(result)

    def __call(self, name, *args):
        variant_args = tuple(get_variant(p) for p in args)
        parameters = GLib.Variant.new_tuple(*variant_args) if args else None

        try:
            self.proxy.call(
                name,
                parameters,
                Gio.DBusCallFlags.NONE,
                GObject.G_MAXINT,
                None,
                self.__on_call_finished,
                None
            )

        except Exception as err:
            print(err)

    def __on_call_finished(self, source: Gio.DBusProxy, result: Gio.Task, data):
        pass

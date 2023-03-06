from gi.repository import Gio, GLib, GObject

from animegui.utils.gi_helpers import get_variant


class AniMeDBus:
    DBUS_NAME = "org.asuslinux.Daemon"
    OBJECT_PATH = "/org/asuslinux/Anime"

    __instance = None

    @staticmethod
    def instance():
        if not AniMeDBus.__instance:
            AniMeDBus.__instance = AniMeDBus()
        return AniMeDBus.__instance

    def __init__(self):
        if AniMeDBus.__instance:
            raise Exception("An instance of this class already exists. Use AniMeDBus.instance() to get it.")

        self.proxy: Gio.DBusProxy = Gio.DBusProxy.new_for_bus_sync(
            Gio.BusType.SYSTEM,
            Gio.DBusProxyFlags.NONE,
            None,
            self.DBUS_NAME,
            self.OBJECT_PATH,
            self.DBUS_NAME,
            None,
        )

    def RunMainLoop(self, start: bool):
        self._call("RunMainLoop", start)

    def SetBootOnOff(self, on: bool):
        self._call("SetBootOnOff", on)

    def SetBrightness(self, brightness: float):
        self._call("SetBrightness", brightness)

    def SetOnOff(self, status: bool):
        self._call("SetOnOff", status)

    def AwakeEnabled(self):
        result = self.proxy.get_cached_property("AwakeEnabled")
        return bool(result)

    def BootEnabled(self):
        result = self.proxy.get_cached_property("BootEnabled")
        return bool(result)

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
                self.__on_call_finished,
                None
            )

        except Exception as err:
            print(err)

    def __on_call_finished(self, source: Gio.DBusProxy, result: Gio.Task, data):
        pass


AniMeDBus.instance()

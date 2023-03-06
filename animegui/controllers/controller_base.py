from gi.repository import GObject


class BaseController(GObject.Object):
    __gtype_name__ = "BaseController"

    __instance = None

    @classmethod
    def instance(cls):
        if not cls.__instance:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self, **kwargs):
        if BaseController.__instance:
            raise Exception("An instance of this class already exists. Use instance() to get it.")
        super().__init__(**kwargs)
        self._view = None

    def get_view(self):
        return self._view

    def set_view(self, view):
        self._view = view

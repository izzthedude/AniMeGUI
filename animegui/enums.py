import os


class Paths:
    XDG_CONFIG = os.environ.get("XDG_CONFIG_HOME")
    XDG_CACHE = os.environ.get("XDG_CACHE_HOME")
    XDG_DATA = os.environ.get("XDG_DATA_HOME")
    USER_PRESETS = os.path.join(XDG_CONFIG, "presets.json")
    FRAME_CACHE = os.path.join(XDG_CACHE, "frame.png")

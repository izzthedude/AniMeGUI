import os


class Paths:
    XDG_CONFIG = os.environ.get("XDG_CONFIG_HOME")
    USER_PRESETS = os.path.join(XDG_CONFIG, "presets.json")

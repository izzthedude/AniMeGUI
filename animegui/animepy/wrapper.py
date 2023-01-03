import subprocess
from dataclasses import dataclass, asdict, astuple
from pathlib import Path


@dataclass
class AniMeData:
    path: str
    scale: float
    x_pos: float
    y_pos: float
    angle: float
    bright: float
    loops: int

    def as_dict(self):
        return asdict(self)

    def as_tuple(self):
        return astuple(self)

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        return setattr(self, item, value)


class AniMeCLI:
    """
    AniMeCLI is a singleton class that acts as a wrapper that writes commands for ``asusctl anime image`` and ``gif``.
    """

    __instance = None

    @staticmethod
    def instance(
            path: str,
            scale: float = 1.0,
            x_pos: float = 0.0,
            y_pos: float = 0.0,
            angle: float = 0.0,
            bright: float = 1.0,
            loops: int = 1
    ):
        """
        Get an AniMeCLI instance.

        Parameters
        ----------
        path
            The full file path to a ``.png`` or ``.gif`` file
        scale
            The scale of the output. 1.0 is the normal value
        x_pos
            The offset of the output on the x-axis
        y_pos
            The offset of the output on the y-axis
        angle
            The angle of the output in radians
        bright
            The brightness of the output between 0.0 - 1.0
        loops
            The number of loops that the given GIF will play. This only applies to ``.gif`` files. Set this to 0 for
            endless looping.
        """
        if not AniMeCLI.__instance:
            AniMeCLI.__instance = AniMeCLI(path, scale, x_pos, y_pos, angle, bright, loops)

        return AniMeCLI.__instance

    def __init__(self, path: str, scale: float, x_pos: float, y_pos: float, angle: float, bright: float, loops: int):
        if AniMeCLI.__instance:
            raise Exception("An instance of this class already exists. Use AniMeCLI.instance() to get it.")

        self._data: AniMeData = AniMeData(path, scale, x_pos, y_pos, angle, bright, loops)

        # Check if running inside flatpak
        self._initial_args: list = ["flatpak-spawn", "--host", "test"]
        try:
            subprocess.check_call(self._initial_args)

        except FileNotFoundError as err:
            # Just run straight from "asusctl blablabla" instead of "flatpak-spawn --host"
            self._initial_args.clear()

        except Exception as err:
            print(err)

        self._initial_args.remove("test")
        self._initial_args += ["asusctl", "anime", self.__check_path_type()]

    def run(self):
        """
        Start running the AniMe display with the arguments defined.
        """
        args = self.__generate_args()
        subprocess.check_call(args)

    def get_all_args(self) -> dict:
        return self._data.as_dict()

    def get_arg(self, arg: str):
        return self._data[arg]

    def set_arg(self, arg: str, value):
        self._data[arg] = value

    def __check_path_type(self) -> str:
        path = Path(self._data.path)
        suffix = path.suffix[1:]

        if suffix == "png":
            return "image"
        elif suffix == "gif":
            return "gif"
        else:
            raise TypeError(f"asusctl only supports png and gif files. '{suffix}' was given.")

    def __generate_args(self) -> list:
        args = self._initial_args[0:]

        for arg, value in self._data.as_dict().items():
            arg = arg.replace("_", "-")
            if "image" in self._initial_args and arg == "loops":
                continue

            args.append(f"--{arg}")
            args.append(f"{value}")

        return args

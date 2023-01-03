import subprocess
from pathlib import Path
from subprocess import Popen

from animegui.animepy.data import AniMeData


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

        self.__data: AniMeData = AniMeData(path, scale, x_pos, y_pos, angle, bright, loops)
        self.__runner: Popen = None

        # Check if running inside flatpak
        self.__initial_command: list = ["flatpak-spawn", "--host", "test"]
        try:
            subprocess.run(self.__initial_command, check=True)

        except FileNotFoundError as err:
            # Just run straight from "asusctl blablabla" instead of "flatpak-spawn --host"
            self.__initial_command.clear()

        except Exception as err:
            print(err)

        self.__initial_command += ["asusctl", "anime", self.__check_path_type()]
        if "test" in self.__initial_command:
            self.__initial_command.remove("test")

    def run(self):
        """
        Start running the AniMe display with the arguments defined.
        """
        if not self.__runner or not self.is_running():
            args = self.__generate_cli_args()
            command = self.__initial_command + args
            self.__runner = Popen(command)
            return self.__runner

    def terminate(self) -> int:
        """
        Terminate the running AniMe process.

        Returns
        -------
        int
            The return code of the runner.
        """
        self.__runner.terminate()
        return self.__runner.returncode

    def is_running(self) -> bool:
        """
        Check if the AniMe process is currently running.
        """
        return self.__runner and self.__runner.poll() is None

    def get_all_args(self) -> dict:
        return self.__data.as_dict()

    def get_arg(self, arg: str):
        return self.__data[arg]

    def set_arg(self, arg: str, value):
        self.__data[arg] = value

    def __check_path_type(self) -> str:
        path = Path(self.__data.path)
        suffix = path.suffix

        if suffix == ".png":
            return "image"
        elif suffix == ".gif":
            return "gif"
        else:
            raise TypeError(f"asusctl only supports .png and .gif files: '{suffix}' was given.")

    def __generate_cli_args(self) -> list:
        args = []

        for key, value in self.__data:
            key = key.replace("_", "-")
            if "image" in self.__initial_command and key == "loops":
                continue

            args.append(f"--{key}")
            args.append(f"{value}")

        return args

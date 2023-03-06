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
    def instance():
        if not AniMeCLI.__instance:
            AniMeCLI.__instance = AniMeCLI()
        return AniMeCLI.__instance

    def __init__(self):
        if AniMeCLI.__instance:
            raise Exception("An instance of this class already exists. Use AniMeCLI.instance() to get it.")

        self._data: AniMeData = AniMeData()
        self._runner: Popen | None = None
        self.__initial_command = ["flatpak-spawn", "--host", "test", "asusctl", "anime"]

    def run(self):
        """
        Start running the AniMe display with the arguments defined.
        """
        if not self._runner or not self.is_running():
            args = self.__generate_cli_args()
            command = self.__initial_command + args
            self._runner = Popen(command)
            return self._runner

    def terminate(self) -> int:
        """
        Terminate the running AniMe process.

        Returns
        -------
        int
            The return code of the runner.
        """
        self._runner.terminate()
        return self._runner.returncode

    def clear(self) -> int:
        """
        Clear the AniMe display.

        Returns
        -------
        int
            The return code of the clear command.
        """
        command = self.__initial_command[0:-1] + ["--clear"]
        return subprocess.run(command).returncode

    def is_running(self) -> bool:
        """
        Check if the AniMe process is currently running.
        """
        return self._runner and self._runner.poll() is None

    def get_all_args(self) -> dict:
        return self._data.as_dict()

    def get_arg(self, arg: str):
        return self._data[arg]

    def get_path(self):
        return self._data.path

    def get_scale(self):
        return self._data.scale

    def get_x(self):
        return self._data.x_pos

    def get_y(self):
        return self._data.y_pos

    def get_angle(self):
        return self._data.angle

    def get_brightness(self):
        return self._data.bright

    def get_loops(self):
        return self._data.loops

    def set_path(self):
        return self._data.path

    def set_arg(self, arg: str, value):
        self._data[arg] = value

    def set_scale(self):
        return self._data.scale

    def set_x(self):
        return self._data.x_pos

    def set_y(self):
        return self._data.y_pos

    def set_angle(self):
        return self._data.angle

    def set_brightness(self):
        return self._data.bright

    def set_loops(self):
        return self._data.loops

    def _check_path_type(self) -> str:
        path = Path(self._data.path)
        suffix = path.suffix

        if suffix == ".png":
            return "image"
        elif suffix == ".gif":
            return "gif"
        else:
            raise TypeError(f"asusctl only supports .png and .gif files: '{suffix}' was given.")

    def __generate_cli_args(self) -> list:
        args = [self._check_path_type()]

        for key, value in self._data:
            key = key.replace("_", "-")
            if "image" in self.__initial_command and key == "loops":
                continue

            args.append(f"--{key}")
            args.append(f"{value}")

        return args


AniMeCLI.instance()

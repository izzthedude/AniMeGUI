import json
import os
from dataclasses import dataclass

from animegui.animepy.data import BaseData, AniMeData
from animegui.enums import Paths


@dataclass
class PresetData(BaseData):
    name: str
    anime: AniMeData

    @staticmethod
    def placeholder():
        return PresetData("Placeholder", AniMeData())

    @staticmethod
    def convert_from_dict(data: dict):
        """
        Converts a dictionary into a PresetData.

        Parameters
        ----------
        data: dict
            A dictionary of preset data

        Returns
        -------
        PresetData
            A PresetData with values taken from the given dictionary
        """
        name, *anime = data.items()
        name = dict([name])
        anime = dict(anime)
        preset_dict = {
            **name,
            "anime": AniMeData(**anime)
        }
        preset = PresetData(**preset_dict)
        return preset

    def convert_to_dict(self) -> dict:
        """
        Converts Preset data into a dictionary, where the AniMeData is expanded.
        E.g: {"name": "Name", "path": "/path/", "scale": 1.0, ...,}

        Returns
        -------
        dict
            A dictionary of the expanded PresetData
        """
        data = {"name": self.name}
        for key, value in self.anime:
            data[key] = value
        return data


def load_presets() -> list[PresetData]:
    """
    Load presets from the presets file.

    Returns
    -------
    list[PresetData]
        A list of PresetData
    """
    # Create an empty presets file if it doesn't exist
    if not os.path.exists(Paths.USER_PRESETS):
        with open(Paths.USER_PRESETS, "w") as file:
            json.dump([], file)

    with open(Paths.USER_PRESETS, "r") as file:
        json_data = json.load(file)  # Expected to be list[dict]
        presets = [PresetData.convert_from_dict(data) for data in json_data]
        return presets


def commit_presets(presets: list[PresetData]):
    """
    Save the given list of PresetData to the presets file.

    Parameters
    ----------
    presets: list[PresetData]
        A list of PresetData
    """
    data = [preset.convert_to_dict() for preset in presets]
    with open(Paths.USER_PRESETS, "w") as file:
        json.dump(data, file)

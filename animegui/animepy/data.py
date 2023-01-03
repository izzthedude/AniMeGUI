from dataclasses import dataclass, asdict, astuple
from enum import Enum

BLOCK_START: int = 7
BLOCK_END: int = 634
PANE_LEN: int = BLOCK_END - BLOCK_START


class BaseData:
    def as_dict(self):
        return asdict(self)

    def as_tuple(self):
        return astuple(self)

    def __iter__(self):
        for key, value in self.as_dict().items():
            yield key, value

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        return setattr(self, item, value)


@dataclass
class AniMeData(BaseData):
    path: str
    scale: float
    x_pos: float
    y_pos: float
    angle: float
    bright: float
    loops: int


class AniMeType(Enum):
    GA401 = 1
    GA402 = 2

    def width(self):
        match self:
            case AniMeType.GA401 | AniMeType.GA402:
                return 74

    def height(self):
        match self:
            case AniMeType.GA401:
                return 36
            case AniMeType.GA402:
                return 39

    def data_length(self):
        match self:
            case AniMeType.GA401:
                return PANE_LEN * 2
            case AniMeType.GA402:
                return PANE_LEN * 3


class AniMeDataBuffer:
    def __init__(self, anime: AniMeType):
        self.__data: list[int] = []
        self.__anime: AniMeType = anime

        length = anime.data_length()
        self.__data = [0 for _ in range(length)]

    def data(self) -> list[int]:
        return self.__data

    def data_mut(self) -> list[int]:
        return self.__data

    @staticmethod
    def from_vec(anime: AniMeType, data: list[int]):
        if len(data) != anime.data_length():
            return Exception(f"Data length not the same")

        buffer = AniMeDataBuffer(anime)
        buffer.__data = data
        return buffer

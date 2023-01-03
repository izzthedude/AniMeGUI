from dataclasses import dataclass, asdict, astuple


class BaseData:
    def as_dict(self):
        return asdict(self)

    def as_tuple(self):
        return astuple(self)

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

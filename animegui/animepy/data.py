from dataclasses import dataclass, asdict, astuple


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
    path: str = ""
    scale: float = 1.0
    x_pos: float = 0.0
    y_pos: float = 0.0
    angle: float = 0.0
    bright: float = 1.0
    loops: int = 0

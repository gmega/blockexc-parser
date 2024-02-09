import re
from dataclasses import dataclass


@dataclass(frozen=True)
class TreeBlockAddress:
    tree_cid: str
    index: int

    def __post_init__(self):
        object.__setattr__(self, 'index', int(self.index))


@dataclass(frozen=True)
class SimpleBlockAddress:
    cid: str


BlockAddress = SimpleBlockAddress | TreeBlockAddress

PARSER = [
    (re.compile(r'"?cid: (?P<cid>[^"]+)"?'), SimpleBlockAddress),
    (re.compile(r'"?treeCid: (?P<tree_cid>[^"]+), index: (?P<index>\d+)"?'), TreeBlockAddress),
]


def parse(address: str) -> BlockAddress:
    for pattern, cls in PARSER:
        match = pattern.match(address)
        if match:
            return cls(**match.groupdict())
    raise ValueError(f'Unknown block address format: {address}')

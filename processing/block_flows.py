from datetime import datetime
from dataclasses import dataclass
from typing import Dict

from logtools.log.base import LineNumberLocation
from logtools.log.sources.parse.chronicles_raw_source import ChroniclesRawSource

from processing import block_address
from processing.block_address import TreeBlockAddress, SimpleBlockAddress, BlockAddress
from sources.muxed_log_source import MuxedLocation


@dataclass(frozen=True)
class Event:
    peer: str
    timestamp: datetime


@dataclass(frozen=True)
class ReadAttempt(Event):
    address: BlockAddress


@dataclass(frozen=True)
class LocalRead(Event):
    address: SimpleBlockAddress


@dataclass(frozen=True)
class MappedBlockAddress(TreeBlockAddress, SimpleBlockAddress):
    pass


class Peer:
    def __init__(self, peer_id: str, name: str):
        self.id = peer_id
        self.name = name
        self.block_map: Dict[str, TreeBlockAddress] = {}

    def add_block_mapping(self, block_cid: str, tree_cid: str, index: int):
        self.block_map[block_cid] = TreeBlockAddress(tree_cid=tree_cid, index=index)

    def get_block_address(self, block_cid: str) -> SimpleBlockAddress | MappedBlockAddress:
        if block_cid in self.block_map:
            return MappedBlockAddress(cid=block_cid, **self.block_map[block_cid].__dict__)
        return SimpleBlockAddress(cid=block_cid)


class CodexNetwork:
    def __init__(self, peer_map: dict[str, str]):
        self.peers = {name: Peer(peer_id, name) for name, peer_id in peer_map.items()}

    def parse(self, log: ChroniclesRawSource[MuxedLocation[LineNumberLocation]]):
        for line in log:
            if line.message.startswith('Getting block from local store or network'):
                yield ReadAttempt(
                    peer=line.location.source,
                    timestamp=line.timestamp,
                    address=block_address.parse(line.fields['address'])
                )

            elif line.message.startswith('Got cid for block'):
                peer = self.peers[line.location.source]
                peer.add_block_mapping(line.fields['cid'], line.fields['treeCid'], int(line.fields['index']))

            elif line.message.startswith('Got block for cid'):
                yield LocalRead(
                    peer=line.location.source,
                    timestamp=line.timestamp,
                    address=self.peers[line.location.source].get_block_address(line.fields['cid'])
                )

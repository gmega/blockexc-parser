from typing import Dict

from logtools.log.sources.parse.chronicles_raw_source import ChroniclesRawSource

from sources.muxed_log_source import MuxedLocation

MAX_LINES = 10_000


def extract_peer_list(log: ChroniclesRawSource[MuxedLocation]) -> Dict[str, str]:
    peers: Dict[str, str] = {}
    for i, line in enumerate(log):
        if i == MAX_LINES:
            break

        if line.message.startswith('Started codex node'):
            peers[line.location.source] = line.fields['id']

    return peers

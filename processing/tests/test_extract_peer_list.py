from logtools.log.sources.input.string_log_source import StringLogSource
from logtools.log.sources.parse.chronicles_raw_source import ChroniclesRawSource

from processors.extract_peer_list import extract_peer_list
from sources.muxed_log_source import MuxedLogSource

STARTUP_LOG = """[node1]: TRC 2024-02-02 20:37:18.321+00:00 Cleaning up query iterator          tid=1 count=31
[node1]: TRC 2024-02-02 20:37:18.321+00:00 Cleaning up orphaned records        tid=1 count=32
[node1]: TRC 2024-02-02 20:37:18.321+00:00 Cleaning up orphaned query iterator tid=1 count=33
[node1]: NOT 2024-02-02 20:37:18.321+00:00 Started codex node                 topics="codex node" id=16U*bvr7iS count=34
[node1]: NOT 2024-02-02 20:37:18.322+00:00 REST service started                tid=1 address=0.0.0.0:30001 count=35
[node1]: TRC 2024-02-02 20:37:18.322+00:00 Iterating blocks finished.          topics="codex discoveryengine" count=36
[node1]: TRC 2024-02-02 20:37:18.322+00:00 About to sleep advertise loop       topics="codex discoveryengine" count=37
[node2]: TRC 2024-02-02 20:37:33.415+00:00 Cleaned up expired records          tid=1 size=0 count=30
[node2]: TRC 2024-02-02 20:37:33.416+00:00 routingTable.getNode failed to find tid=1 count=52
[node1]: TRC 2024-02-02 20:37:33.415+00:00 Cleaning up query iterator          tid=1 count=31
[node2]: TRC 2024-02-02 20:37:33.415+00:00 Cleaning up orphaned records        tid=1 count=32
[node2]: TRC 2024-02-02 20:37:33.415+00:00 Cleaning up orphaned query iterator tid=1 count=33
[node2]: NOT 2024-02-02 20:37:33.416+00:00 Started codex node                 topics="codex node" id=16U*e1k75X count=34
[node2]: NOT 2024-02-02 20:37:33.416+00:00 REST service started                tid=1 address=0.0.0.0:30003 count=35"""


def test_should_recognize_peer_ids_in_log():
    peer_list = extract_peer_list(ChroniclesRawSource(
        MuxedLogSource(
            StringLogSource(lines=STARTUP_LOG)
        )
    ))

    assert peer_list == {
        'node1': '16U*bvr7iS',
        'node2': '16U*e1k75X',
    }

from dateutil import parser
from logtools.log.sources.input.string_log_source import StringLogSource
from logtools.log.sources.parse.chronicles_raw_source import ChroniclesRawSource

from processing.block_address import SimpleBlockAddress
from processing.block_flows import CodexNetwork, ReadAttempt, LocalRead, MappedBlockAddress
from sources.muxed_log_source import MuxedLogSource


def log_from_str(log_str: str):
    return ChroniclesRawSource(
        MuxedLogSource(
            StringLogSource(
                lines=log_str
            )
        )
    )


def test_should_identify_block_read_attempts():
    log = log_from_str(
        '[node1]: TRC 2024-02-06 09:43:04.549-03:00 Getting block from local store or network  '
        'topics="codex networkstore" tid=29479 address="cid: zDv*Nrc2CZ" count=1\n'
    )

    network = CodexNetwork(peer_map={'node1': '16U*bvr7iS', 'node2': '16U*e1k75X'})
    assert list(network.parse(log)) == [
        ReadAttempt(
            peer='node1',
            timestamp=parser.parse('2024-02-06 09:43:04.549-03:00'),
            address=SimpleBlockAddress(cid='zDv*Nrc2CZ'),
        )
    ]


def test_should_identify_block_reads():
    log = log_from_str(
        '[node1]: TRC 2024-02-06 09:43:04.549-03:00 Getting block from local store or network  '
        'topics="codex networkstore" tid=29479 address="cid: zDv*Nrc2CZ" count=1\n'
        
        '[node1]: TRC 2024-02-06 17:40:54.500-03:00 Got block for cid                          '
        'topics="codex repostore" tid=318927 cid=zDv*Nrc2CZ count=2\n'
    )

    network = CodexNetwork(peer_map={'node1': '16U*bvr7iS', 'node2': '16U*e1k75X'})

    assert list(network.parse(log)) == [
        ReadAttempt(
            peer='node1',
            timestamp=parser.parse('2024-02-06 09:43:04.549-03:00'),
            address=SimpleBlockAddress(cid='zDv*Nrc2CZ'),
        ),
        LocalRead(
            peer='node1',
            timestamp=parser.parse('2024-02-06 17:40:54.500-03:00'),
            address=SimpleBlockAddress(cid='zDv*Nrc2CZ')
        )
    ]


def test_should_identify_mapped_block_reads():
    log = log_from_str(
        '[node1]: TRC 2024-02-06 09:43:04.549-03:00 Getting block from local store or network  '
        'topics="codex networkstore" tid=29479 address="cid: zDv*Nrc2CZ" count=1\n'
        
        '[node1]: TRC 2024-02-06 17:40:54.500-03:00 Got cid for block                          '
        'topics="codex repostore" tid=318927 treeCid=zDz*zzUhHc index=0 cid=zDx*tBUsER count=2\n'
        
        '[node1]: TRC 2024-02-06 17:40:54.500-03:00 Got block for cid                          '
        'topics="codex repostore" tid=318927 cid=zDx*tBUsER count=3\n'
    )

    network = CodexNetwork(peer_map={'node1': '16U*bvr7iS', 'node2': '16U*e1k75X'})

    assert list(network.parse(log)) == [
        ReadAttempt(
            peer='node1',
            timestamp=parser.parse('2024-02-06 09:43:04.549-03:00'),
            address=SimpleBlockAddress(cid='zDv*Nrc2CZ'),
        ),
        LocalRead(
            peer='node1',
            timestamp=parser.parse('2024-02-06 17:40:54.500-03:00'),
            address=MappedBlockAddress(
                cid='zDx*tBUsER',
                tree_cid='zDz*zzUhHc',
                index=0
            )
        )
    ]

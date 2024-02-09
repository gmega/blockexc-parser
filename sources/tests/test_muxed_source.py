from logtools.log.sources.input.string_log_source import StringLogSource
from logtools.log.sources.parse.chronicles_raw_source import ChroniclesRawSource

from sources.muxed_log_source import MuxedLogSource


def test_should_identify_the_original_source():
    log = ChroniclesRawSource(MuxedLogSource(StringLogSource(
        """[codex2-4-67768c5585-r76lf]: TRC 2024-02-02 20:49:12.167+00:00 one  topics="codex blockexcengine"  count=1
        [codex2-4-67768c5585-r76lf]: TRC 2024-02-02 20:49:12.167+00:00 two     topics="codex blockexcengine"  count=2
        [bootstrap-2-ddc6bcd84-k7bdx]: TRC 2024-02-02 20:49:12.168+00:00 one   topics="codex discoveryengine" count=1
        [codex1-3-856b59d5b-wrrdm]: DBG 2024-02-02 20:49:12.214+00:00 one      topics="codex blockexcnetwork" count=1
        [codex1-3-856b59d5b-wrrdm]: TRC 2024-02-02 20:49:12.214+00:00 two      topics="codex blockexcengine"  count=2"""
    )))

    lines = list(log)

    assert [line.location.source for line in lines] == [
        'codex2-4-67768c5585-r76lf', 'codex2-4-67768c5585-r76lf', 'bootstrap-2-ddc6bcd84-k7bdx',
        'codex1-3-856b59d5b-wrrdm', 'codex1-3-856b59d5b-wrrdm'
    ]

    assert [line.fields['count'] for line in lines] == [1, 2, 1, 1, 2]

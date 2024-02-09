import sys
from dataclasses import dataclass
from typing import Generic, Iterator

from ansiwrap import strip_color
from logtools.log.base import TLocation, LogSource, RawLogLine


@dataclass
class MuxedLocation(Generic[TLocation]):
    source: str
    location: TLocation


class MuxedLogSource(LogSource[RawLogLine[MuxedLocation[TLocation]]]):
    """A "muxed" log source is a log source that contains multiple logs merged from different sources. Sources are
    identified by a prefix tag in the log line, which this source will strip and insert into the location.
    """

    def __init__(self, source: LogSource[RawLogLine[TLocation]], strip_ansi_colors=True):
        self.source = source
        self.strip_ansi_colors = strip_ansi_colors

    def __iter__(self) -> Iterator[RawLogLine[MuxedLocation[TLocation]]]:
        for line in self.source:
            raw = strip_color(line.raw)
            brk = raw.find(':')

            if brk == -1:
                print(f'Skip unparseable line: {raw}', file=sys.stderr)
                continue

            source = raw[:brk][1:-1]
            yield RawLogLine(
                location=MuxedLocation(
                    source=source,
                    location=line.location,
                ),
                raw=raw[brk + 1:].strip()
            )

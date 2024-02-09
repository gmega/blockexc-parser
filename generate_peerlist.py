import argparse
import json
import sys
from csv import DictWriter
from typing import Dict, TextIO

from logtools.log.sources.parse.chronicles_raw_source import ChroniclesRawSource

from processing.extract_peer_list import extract_peer_list
from sources.muxed_log_source import MuxedLogSource
from logtools.log.sources.input.textio_log_source import TextIOLogSource


def main(infile: TextIO, outfile: TextIO):
    peers = extract_peer_list(ChroniclesRawSource(MuxedLogSource(TextIOLogSource(infile))))
    if not peers:
        print('No peers found', file=sys.stderr)
        return

    json.dump(peers, outfile, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r', encoding='utf-8'),
                        default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w', encoding='utf-8'),
                        default=sys.stdout)

    args = parser.parse_args()
    main(args.infile, args.outfile)

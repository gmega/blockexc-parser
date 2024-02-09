import json
import sys
from csv import DictWriter
from typing import TextIO, Dict

from logtools.log.sources.input.textio_log_source import TextIOLogSource
from logtools.log.sources.parse.chronicles_raw_source import ChroniclesRawSource

from processing.block_flows import CodexNetwork
from sources.muxed_log_source import MuxedLogSource


def main(run: str, infile: TextIO, outfile: TextIO, peer_list: Dict[str, str], print_header: bool):
    writer = DictWriter(
        outfile, fieldnames=['run', 'peer', 'timestamp', 'operation', 'cid', 'tree_cid', 'index']
    )

    if print_header:
        writer.writeheader()

    network = CodexNetwork(peer_map=peer_list)
    for line in network.parse(ChroniclesRawSource(MuxedLogSource(TextIOLogSource(infile)))):
        writer.writerow(
            {
                'run': run,
                'peer': line.peer,
                'timestamp': line.timestamp,
                'operation': line.__class__.__name__,
                'cid': getattr(line.address, 'cid', ''),
                'tree_cid': getattr(line.address, 'tree_cid', ''),
                'index': getattr(line.address, 'index', ''),
            }
        )


if __name__ == '__main__':
    with open(sys.argv[1], 'r', encoding='utf-8') as peer_list_file:
        peer_list = json.load(peer_list_file)

    for runfile in sys.argv[2:]:
        with open(runfile, 'r', encoding='utf-8') as infile:
            main(runfile, infile, sys.stdout, peer_list, runfile == sys.argv[2])

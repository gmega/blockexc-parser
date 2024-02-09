from processing import block_address
from processing.block_address import SimpleBlockAddress, TreeBlockAddress


def test_should_parse_simple_block_address():
    assert block_address.parse('"cid: zDv*Nrc2CZ"') == SimpleBlockAddress(cid='zDv*Nrc2CZ')


def test_should_parse_tree_block_address():
    assert block_address.parse('"treeCid: zDz*zzUhHc, index: 0"') == TreeBlockAddress(tree_cid='zDz*zzUhHc', index=0)

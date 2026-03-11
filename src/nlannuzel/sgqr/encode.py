from nlannuzel.sgqr.crc import CRC_ID, append_crc
from nlannuzel.sgqr.detokenizer import DeTokenizer

def _detokenize(entries: list[dict], level = 0) -> str:
    detok = DeTokenizer()
    for ent in entries:
        if level != 0 or ent['id'] != CRC_ID:
            v = ent['value'] if type(ent['value']) is str else _detokenize(ent['value'], 1 + level)
            detok.put_tokens(ent['id'], v)
    return detok.s

def encode_sgqr(input: list[dict]) -> str:
    return append_crc(_detokenize(input))

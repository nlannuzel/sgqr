from nlannuzel.sgqr.crc import check_crc
from nlannuzel.sgqr.templates import Template, parse_str

def decode_sgqr(input: str) -> list[dict]:
    input = input.rstrip()
    check_crc(input)
    return parse_str(Template.ROOT, input)

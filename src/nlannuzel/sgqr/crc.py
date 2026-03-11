CRC_ID = '63'
CRC_LEN = '04'

def calculate_crc(input: str) -> str:
    crc = 0xFFFF
    poly = 0x1021

    for b in input.encode("utf-8"):
        crc ^= (b << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) & 0xFFFF) ^ poly
            else:
                crc = (crc << 1) & 0xFFFF
    return f"{crc:04X}"

def append_crc(s: str) -> str:
    s += CRC_ID + CRC_LEN
    s += calculate_crc(s)
    return s

def check_crc(input: str) -> None:
    crc_data = input[:-4]
    given_crc = input[-4:]
    calculated_crc = calculate_crc(crc_data)
    assert given_crc == calculated_crc

import yaml
from datetime import datetime, timezone, timedelta
from nlannuzel.sgqr.templates import parse_str

def d(i, v):
    return {'id': i, 'value': v}

def a2d(a):
    return [ d(i, v) for i, v in a ]

def paynow_phone(recipient: str, amount: float, comment: str=None, ttl: int=None, editable_amount: bool=False):
    decoded = a2d([
        ['00', '01'],
        ['01', '12'],
        ['26', a2d([
            ['00', 'SG.PAYNOW'],
            ['01', '0'],
            ['02', recipient],
            ['03', '1' if editable_amount is True else '0'],
        ])],
        ['52', '3000'],
        ['53', '702'],
        ['54', str(amount)],
        ['58', 'SG'],
        ['60', 'Singapore'],
    ])

    if ttl is not None:
        tz_sg = timezone(offset=timedelta(hours=8))
        dt = datetime.now(tz_sg) + timedelta(seconds=ttl)
        expiry = dt.strftime('%Y%m%d%H%M%S')
        decoded[2]['value'].append(d('04', expiry))

    if comment is not None:
        decoded.append(d('62', a2d([['01', comment]])))

    return decoded

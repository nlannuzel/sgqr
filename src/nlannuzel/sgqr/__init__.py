import yaml
import argparse
from nlannuzel.sgqr.encode import encode_sgqr
from nlannuzel.sgqr.decode import decode_sgqr
from datetime import datetime, timezone, timedelta

def encode():
    with open("/dev/stdin") as f:
        print(encode_sgqr(yaml.load(f, Loader=yaml.Loader)), end='')

def decode():
    with open("/dev/stdin") as f:
        print(yaml.dump(decode_sgqr(f.read())), end='')

def paynow():
    parser = argparse.ArgumentParser(
                    prog='paynow-sgqr',
                    description='encode a EMV string for PayNow')
    parser.add_argument('-r', '--recipient', required=True, help="payee's phone number")
    parser.add_argument('-a', '--amount', required=True, type=float, help='amount in SGD')
    parser.add_argument('-c', '--comment', required=False, help='comment for the recipient')
    parser.add_argument('-t', '--time-to-live', required=False, type=int, help='how many seconds the code should be valid')
    parser.add_argument('-e', '--editable_amount', required=False, action='store_true', help='allow the amount to be edited')
    args = parser.parse_args()

    def d(i, v):
        return {'id': i, 'value': v}
    def a2d(a):
        return [ d(i, v) for i, v in a ]

    decoded = a2d([
        ['00', '01'],
        ['01', '12'],
        ['26', a2d([
            ['00', 'SG.PAYNOW'],
            ['01', '0'],
            ['02', args.recipient],
            ['03', '0' if args.editable_amount is None else '1'],
        ])],
        ['52', '3000'],
        ['53', '702'],
        ['54', str(args.amount)],
        ['58', 'SG'],
        ['60', 'Singapore'],
    ])

    if args.time_to_live is not None:
        tz_sg = timezone(offset=timedelta(hours=8))
        dt = datetime.now(tz_sg) + timedelta(seconds=args.time_to_live)
        expiry = dt.strftime('%Y%m%d%H%M%S')
        decoded[2]['value'].append(d('04', expiry))

    if args.comment is not None:
        decoded.append(d('62', a2d([['01', args.comment]])))
    print(encode_sgqr(decoded), end='')

if __name__ == '__main__':
    paynow()

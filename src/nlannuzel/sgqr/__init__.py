import yaml
import argparse
from nlannuzel.sgqr.encode import encode_sgqr
from nlannuzel.sgqr.decode import decode_sgqr
from datetime import datetime, timezone, timedelta
from nlannuzel.sgqr.factory import paynow_phone, paynow_uen

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
    parser.add_argument('-r', '--recipient', required=True, help="payee's phone number or UEN")
    parser.add_argument('-u', '--uen', required=False, action='store_true', help="pay to a UEN instead of a phone")
    parser.add_argument('-a', '--amount', required=True, type=float, help='amount in SGD')
    parser.add_argument('-c', '--comment', required=False, help='comment or bill number for the recipient')
    parser.add_argument('-t', '--time-to-live', required=False, type=int, help='how many seconds the code should be valid')
    parser.add_argument('-e', '--editable_amount', required=False, action='store_true', help='allow the amount to be edited')
    args = parser.parse_args()

    func = pay_uen if args.uen else pay_phone
    print(
        yaml.dump(
            func(
                phone=args.recipient,
                amount=args.amount,
                comment=args.comment,
                ttl=args.time_to_live,
                editable_amount=args.editable_amount,
            )))

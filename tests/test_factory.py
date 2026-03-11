import os
import yaml
import unittest
from nlannuzel.sgqr.factory import paynow_phone, paynow_uen

class TestPaynow(unittest.TestCase):
    def test_paynow_1(self):
        entries = paynow_phone(recipient='+6599999999', amount=888.88)
        self.assertEqual(type(entries), list)
        self.assertEqual([e['id'] for e in entries], ['00', '01', '26', '52', '53', '54', '58', '60'])
        self.assertEqual([e['value'] for e in entries if e['id'] != '26'], ['01', '12', '3000', '702', '888.88', 'SG', 'Singapore'])
        self.assertEqual([e['id'] for e in entries[2]['value']], ['00', '01', '02', '03'])
        self.assertEqual([e['value'] for e in entries[2]['value']], ['SG.PAYNOW', '0', '+6599999999', '0'])

    def test_paynow_2(self):
        entries = paynow_phone(recipient='+6599999999', amount=888, comment='hello')
        self.assertEqual(type(entries), list)
        self.assertEqual([e['id'] for e in entries], ['00', '01', '26', '52', '53', '54', '58', '60', '62'])
        self.assertEqual([e['value'] for e in entries if e['id'] not in ['26', '62']], ['01', '12', '3000', '702', '888', 'SG', 'Singapore'])
        self.assertEqual([e['id'] for e in entries[2]['value']], ['00', '01', '02', '03'])
        self.assertEqual([e['value'] for e in entries[2]['value']], ['SG.PAYNOW', '0', '+6599999999', '0'])
        self.assertEqual([e['id'] for e in entries[8]['value']], ['01'])
        self.assertEqual([e['value'] for e in entries[8]['value']], ['hello'])

    def test_paynow_3(self):
        entries = paynow_phone(recipient='+6599999999', amount=888.88, comment='hello world', ttl=300)
        self.assertEqual(type(entries), list)
        self.assertEqual([e['id'] for e in entries], ['00', '01', '26', '52', '53', '54', '58', '60', '62'])
        self.assertEqual([e['value'] for e in entries if e['id'] not in ['26', '62']], ['01', '12', '3000', '702', '888.88', 'SG', 'Singapore'])
        self.assertEqual([e['id'] for e in entries[2]['value']], ['00', '01', '02', '03', '04'])
        self.assertEqual(len(entries[2]['value'][4]['value']), 14, 'expiry format')
        self.assertEqual([e['value'] for e in entries[2]['value'] if e['id'] != '04'], ['SG.PAYNOW', '0', '+6599999999', '0'])
        self.assertEqual([e['id'] for e in entries[8]['value']], ['01'])
        self.assertEqual([e['value'] for e in entries[8]['value']], ['hello world'])

    def test_paynow_uen_1(self):
        entries = paynow_uen(recipient='123456789', amount=888.88, comment='hello world', ttl=300)
        self.assertEqual(type(entries), list)
        self.assertEqual([e['id'] for e in entries], ['00', '01', '26', '52', '53', '54', '58', '60', '62'])
        self.assertEqual([e['value'] for e in entries if e['id'] not in ['26', '62']], ['01', '12', '3000', '702', '888.88', 'SG', 'Singapore'])
        self.assertEqual([e['id'] for e in entries[2]['value']], ['00', '01', '02', '03', '04'])
        self.assertEqual(len(entries[2]['value'][4]['value']), 14, 'expiry format')
        self.assertEqual([e['value'] for e in entries[2]['value'] if e['id'] != '04'], ['SG.PAYNOW', '2', '123456789', '0'])
        self.assertEqual([e['id'] for e in entries[8]['value']], ['01'])
        self.assertEqual([e['value'] for e in entries[8]['value']], ['hello world'])

    def test_paynow_uen_no_bill_nbr(self):
        entries = paynow_uen(recipient='123456789', amount=888.88, ttl=300)
        self.assertEqual(type(entries), list)
        self.assertEqual([e['id'] for e in entries], ['00', '01', '26', '52', '53', '54', '58', '60', '62'])
        self.assertEqual([e['value'] for e in entries if e['id'] not in ['26', '62']], ['01', '12', '3000', '702', '888.88', 'SG', 'Singapore'])
        self.assertEqual([e['id'] for e in entries[2]['value']], ['00', '01', '02', '03', '04'])
        self.assertEqual(len(entries[2]['value'][4]['value']), 14, 'expiry format')
        self.assertEqual([e['value'] for e in entries[2]['value'] if e['id'] != '04'], ['SG.PAYNOW', '2', '123456789', '0'])
        self.assertEqual([e['id'] for e in entries[8]['value']], ['01'])
        self.assertEqual([e['value'] for e in entries[8]['value']], ['NA'])

if __name__ == '__main__':
    unittest.main()

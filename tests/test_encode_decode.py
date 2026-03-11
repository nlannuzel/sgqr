import os
import yaml
import unittest
from nlannuzel.sgqr.encode import encode_sgqr
from nlannuzel.sgqr.decode import decode_sgqr
from nlannuzel.sgqr.tests.samples_reader import read_test_samples

class TestEncode(unittest.TestCase):
    def test_encode(self):
        def cb(encoded: str, decoded: list, directory: str) -> None:
            self.assertEqual(encode_sgqr(decoded), encoded, f"encode {directory}")
        read_test_samples(cb)

class TestDecode(unittest.TestCase):
    def test_encode(self):
        def remove_name(decoded: list):
            decoded2 = []
            for entry in decoded:
                decoded2.append({'id': entry['id'], 'value': entry['value']})
            return decoded2

        def cb(encoded: str, decoded: list, directory: str) -> None:
            self.assertEqual(remove_name(decode_sgqr(encoded)), remove_name(decoded), f"decode {directory} ignore name")
            self.assertEqual(decode_sgqr(encoded), decoded, f"decode {directory}")

        read_test_samples(cb)

if __name__ == '__main__':
    unittest.main()

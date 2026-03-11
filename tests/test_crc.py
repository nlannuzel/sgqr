import unittest
from nlannuzel.sgqr.crc import calculate_crc, check_crc
from nlannuzel.sgqr.tests.samples_reader import read_test_samples

class TestCRC(unittest.TestCase):
    def test_crc1(self):
        def cb(encoded: str, decoded: list, directory: str):
            given_crc = encoded[-4:]
            crc_data = encoded[:-4]
            calculated_crc = calculate_crc(crc_data)
            self.assertEqual(given_crc, calculated_crc)
        read_test_samples(cb)

    def test_crc2(self):
        def cb(encoded: str, decoded: list, directory: str):
            check_crc(encoded)
        read_test_samples(cb)

    def test_crc3(self):
        def cb(encoded: str, decoded: list, directory: str):
            crc_data = encoded[:-4]
            with self.assertRaises(AssertionError):
                check_crc(crc_data+'8888')
        read_test_samples(cb)

if __name__ == '__main__':
    unittest.main()

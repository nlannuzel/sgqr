import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from nlannuzel.sgqr.templates import SpecTable, Template


class TestSpecTable(unittest.TestCase):
    def test_packaged_specs_outside_checkout(self):
        original = Path.cwd()
        with TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                self.assertEqual(
                    SpecTable(Template.ROOT).lookup_field_name('00'),
                    'Payload Format Indicator',
                )
                for template in (
                    Template.MERCHANT_ACCOUNT_INFORMATION_PAYNOW,
                    Template.ADDITIONAL_DATA_FIELDS,
                    Template.MERCHANT_INFORMATION_LANGUAGE,
                    Template.UNRESERVED,
                ):
                    self.assertTrue(SpecTable(template).table)
            finally:
                os.chdir(original)

    def test_custom_specs_directory(self):
        with TemporaryDirectory() as directory:
            Path(directory, 'root-data.yaml').write_text(
                "- [Custom field, '00']\n", encoding='utf-8'
            )
            self.assertEqual(
                SpecTable(Template.ROOT, directory).lookup_field_name('00'),
                'Custom field',
            )

"""Ensure release checks block incorrectly versioned uploads."""

from pathlib import Path
import subprocess
import sys
import tomllib
from zipfile import ZipFile

import pytest


ROOT = Path(__file__).resolve().parents[1]
PROJECT = tomllib.loads((ROOT / 'pyproject.toml').read_text(encoding='utf-8'))['project']
VERSION = PROJECT['version']


def run_check(*arguments):
    return subprocess.run(
        [sys.executable, str(ROOT / 'ci/check_version.py'), *arguments],
        capture_output=True, text=True, check=False, timeout=10,
    )


@pytest.mark.parametrize('tag', ['', f'v{VERSION}'])
def test_matching_tag(tag):
    assert run_check('--tag', tag).returncode == 0


@pytest.mark.parametrize('tag', [VERSION, 'v999.0.0', f'vv{VERSION}'])
def test_wrong_tag(tag):
    result = run_check('--tag', tag)
    assert result.returncode != 0
    assert 'Release tag' in result.stderr


@pytest.mark.parametrize('filename_version,metadata_version,valid', [
    (VERSION, VERSION, True),
    ('999.0.0', VERSION, False),
    (f'v{VERSION}', VERSION, False),
    (VERSION, '999.0.0', False),
    (VERSION, f'v{VERSION}', False),
])
def test_wheel_version(tmp_path, filename_version, metadata_version, valid):
    wheel = tmp_path / f'nlannuzel_sgqr-{filename_version}-py3-none-any.whl'
    with ZipFile(wheel, 'w') as archive:
        archive.writestr(
            f'nlannuzel_sgqr-{filename_version}.dist-info/METADATA',
            f'Metadata-Version: 2.4\nName: {PROJECT["name"]}\nVersion: {metadata_version}\n',
        )
    result = run_check('--tag', f'v{VERSION}', '--wheel', str(wheel))
    assert (result.returncode == 0) == valid, result.stderr

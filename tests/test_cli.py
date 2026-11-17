"""Exercise installed console scripts from outside the source checkout."""

from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import subprocess
import sysconfig

import pytest
import yaml


@pytest.fixture
def run_cli(tmp_path):
    environment = os.environ.copy()
    environment.pop('PYTHONPATH', None)

    def run(command, *arguments, input=None):
        executable = Path(sysconfig.get_path('scripts'), command)
        return subprocess.run(
            [str(executable), *arguments],
            input=input,
            text=True,
            capture_output=True,
            check=True,
            timeout=10,
            cwd=tmp_path,
            env=environment,
        ).stdout

    return run


def fields(entries):
    return {entry['id']: entry['value'] for entry in entries}


@pytest.mark.parametrize('recipient,uen,proxy_type', [
    ('+6599999999', False, '0'),
    ('12345678', True, '2'),
])
@pytest.mark.parametrize('ttl', [None, 300])
@pytest.mark.parametrize('editable', [False, True])
def test_installed_cli_round_trip(run_cli, recipient, uen, proxy_type, ttl, editable):
    arguments = ['-r', recipient, '-a', '88.88', '-c', 'split bill restaurant']
    if uen:
        arguments.append('--uen')
    if ttl is not None:
        arguments.extend(['-t', str(ttl)])
    if editable:
        arguments.append('--editable_amount')

    singapore = timezone(timedelta(hours=8))
    before = datetime.now(singapore).replace(microsecond=0)
    generated = run_cli('paynow', *arguments)
    after = datetime.now(singapore).replace(microsecond=0)
    encoded = run_cli('encode-sgqr', input=generated)
    decoded = run_cli('decode-sgqr', input=encoded)

    assert encoded[-8:-4] == '6304'
    assert run_cli('encode-sgqr', input=decoded) == encoded

    # Check both the generated YAML and the decoded payment, including nested fields.
    for description in (generated, decoded):
        payment = fields(yaml.safe_load(description))
        account = fields(payment['26'])
        assert payment['54'] == '88.88'
        assert payment['53'] == '702'
        assert payment['58'] == 'SG'
        assert fields(payment['62'])['01'] == 'split bill restaurant'
        assert account['00'] == 'SG.PAYNOW'
        assert account['01'] == proxy_type
        assert account['02'] == recipient
        assert account['03'] == ('1' if editable else '0')
        if ttl is None:
            assert '04' not in account
        else:
            expiry = datetime.strptime(account['04'], '%Y%m%d%H%M%S').replace(tzinfo=singapore)
            assert before + timedelta(seconds=ttl) <= expiry <= after + timedelta(seconds=ttl)

    generated_account = fields(fields(yaml.safe_load(generated))['26'])
    decoded_account = fields(fields(yaml.safe_load(decoded))['26'])
    assert generated_account == decoded_account


@pytest.mark.parametrize('uen', [False, True])
def test_installed_cli_without_comment(run_cli, uen):
    arguments = ['-r', '12345678' if uen else '+6599999999', '-a', '88']
    if uen:
        arguments.append('--uen')
    generated = run_cli('paynow', *arguments)
    encoded = run_cli('encode-sgqr', input=generated)
    payment = fields(yaml.safe_load(run_cli('decode-sgqr', input=encoded)))
    if uen:
        assert fields(payment['62'])['01'] == 'NA'
    else:
        assert '62' not in payment

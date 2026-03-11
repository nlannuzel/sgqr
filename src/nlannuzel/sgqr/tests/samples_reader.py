import os
import yaml
from collections.abc import Callable

SAMPLES_PATH = 'samples'
DECODED_FILE = 'decoded.yaml'
ENCODED_FILE = 'encoded.txt'

def read_test_samples(callback: Callable[[str, list, str], bool]) -> None:
    for directory in os.listdir(SAMPLES_PATH):
        if directory == '.' or directory == '..':
            continue
        with open('/'.join([SAMPLES_PATH, directory, DECODED_FILE])) as f:
            decoded = yaml.load(f, Loader=yaml.Loader)
        with open('/'.join([SAMPLES_PATH, directory, ENCODED_FILE])) as f:
            encoded = f.read().rstrip()
        try:
            callback(encoded, decoded, directory)
        except Exception as e:
            raise RuntimeError(f"{directory}: {e}")

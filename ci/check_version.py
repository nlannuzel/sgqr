"""Check release tags and wheel versions against pyproject.toml."""

import argparse
from email.parser import BytesParser
from pathlib import Path
import re
import tomllib
from zipfile import ZipFile


def check_version(tag, wheels):
    project_file = Path(__file__).resolve().parents[1] / 'pyproject.toml'
    project = tomllib.loads(project_file.read_text(encoding='utf-8'))['project']
    version = project['version']
    if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', version):
        raise ValueError(f'Expected a package version without v, got {version!r}')
    if tag and tag != f'v{version}':
        raise ValueError(f'Release tag {tag!r} must be v{version}')

    def normalize(name):
        return re.sub(r'[-_.]+', '_', name).lower()

    for path in wheels:
        wheel = Path(path)
        distribution, wheel_version, *_ = wheel.name.split('-')
        if normalize(distribution) != normalize(project['name']) or wheel_version != version:
            raise ValueError(f'Wheel filename {wheel.name!r} does not match {project["name"]} {version}')
        with ZipFile(wheel) as archive:
            metadata_files = [name for name in archive.namelist() if name.endswith('.dist-info/METADATA')]
            if len(metadata_files) != 1:
                raise ValueError(f'Expected one METADATA file in {wheel.name}')
            metadata = BytesParser().parsebytes(archive.read(metadata_files[0]))
        if normalize(metadata.get('Name', '')) != normalize(project['name']) or metadata['Version'] != version:
            raise ValueError(f'Wheel metadata in {wheel.name!r} does not match {project["name"]} {version}')
    print(f'Validated {project["name"]} {version}' + (f' for {tag}' if tag else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tag', default='', help='GitHub release tag (vMAJOR.MINOR.PATCH)')
    parser.add_argument('--wheel', nargs='+', default=[], help='Built wheels to validate')
    arguments = parser.parse_args()
    try:
        check_version(arguments.tag, arguments.wheel)
    except ValueError as error:
        parser.exit(1, f'{error}\n')

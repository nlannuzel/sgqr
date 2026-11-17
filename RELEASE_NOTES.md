# Release notes for v0.0.2

This patch release fixes installed decoding and prepares SGQR for automated
PyPI publishing. It covers changes after commit
`7129c3b48b17ce4f321630569bf27e4094bbf736`.

## Highlights

- The wheel includes the YAML specifications. `decode-sgqr` and Python decoding
  can now run outside the source checkout without missing specification files.
- Package metadata declares the GPL-3.0-only license using PEP 639.
- CLI help and README examples explain that `paynow` produces YAML. Pipe it
  through `encode-sgqr` to generate the payment string. The README also documents
  UEN recipients with `--uen`.
- GitHub CI tests the installed wheel on Python 3.11–3.15, including payment
  round trips for phone and UEN recipients. Published GitHub releases trigger
  wheel validation and PyPI upload after the test matrix succeeds.

## Installation and compatibility

Python 3.11 or newer is required.

```shell
python -m pip install --upgrade nlannuzel.sgqr==0.0.2
```

Phone and UEN payments were already supported before this release. Existing
CLI commands remain the same. Code that uses `SpecTable.spec_file` directly
must handle a traversable resource or path instead of a string; custom
specification directories remain supported via `specs_dir`.

## Release conventions

- GitHub release title and Git tag: `v0.0.2`.
- `pyproject.toml`, installed package metadata, and pip requirement: `0.0.2`.
- Wheel filename: `nlannuzel_sgqr-0.0.2-py3-none-any.whl`.
- Source distribution filename: `nlannuzel_sgqr-0.0.2.tar.gz`.

Both build and publish jobs reject a release tag that differs from `v` plus
the version in `pyproject.toml`. Built wheel filenames and metadata must use
the package version without `v`.

The release tag must point to the commit containing these release changes.
Publishing the GitHub release starts the PyPI upload job, which requires the
repository secret `PYPI_API_TOKEN`. The workflow uploads the wheel; the source
distribution is built by CI but is not uploaded by the publish job.

See [CHANGELOG.md](CHANGELOG.md) for the full change summary.

# Changelog

## [0.0.2] - 2026-11-17

Changes after commit `7129c3b48b17ce4f321630569bf27e4094bbf736`.

### Fixed

- Include the YAML specification tables in built distributions and load them
  through `importlib.resources`. Installed decoding now works from any working
  directory, without a separate `specs/` directory.
- Declare the GPL-3.0-only license and license file in the project metadata using
  PEP 639, with `setuptools>=77.0.3` as the build backend requirement.
- Correct the `paynow` help text to describe its YAML output and command name.
- Correct the README project link and document PayNow UEN recipients and the
  `paynow | encode-sgqr` pipeline.

### Changed

- `SpecTable` loads bundled specifications by default. An explicit `specs_dir`
  still selects custom specifications; `spec_file` now returns a traversable
  resource or path instead of a string.
- Run GitHub CI on Python 3.11–3.15, with fatal lint checks and tests against an
  installed wheel. Add CLI round-trip coverage outside the checkout for phone
  and UEN recipients, expiry, editable amounts, and comments.
- Add wheel validation and PyPI upload when a GitHub release is published,
  after the build and test matrix succeeds.
- Check release tags against the package version before building, and check
  wheel filenames and metadata before installation or upload. Git tags use a
  leading `v`; Python package versions do not.
- Include release documents, the version checker, CI requirements, and test
  samples in source distributions.
- Replace Forgejo CI and Renovate configuration with GitHub Actions and weekly
  Dependabot updates. Update checkout and setup-python to pinned v7 actions.

[0.0.2]: https://github.com/nlannuzel/sgqr/releases/tag/v0.0.2

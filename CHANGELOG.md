# Changelog

All notable changes to this project are documented here.
This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html), and
the format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

Every release is archived on Zenodo. The **concept DOI**
[10.5281/zenodo.21757553](https://doi.org/10.5281/zenodo.21757553) always resolves to the latest
version; each release below also has its own version DOI.

## [0.1.0] - 2026-08-02

First public release.

### Added

- `aeo_audit_lite.py` — runs a buyer prompt against an AI engine repeatedly and
  reports how often a brand is mentioned versus named competitors, with a Wilson
  95% confidence interval and a share-of-model figure.
- Perplexity and OpenAI engines via `--engine`, and a `--mock` mode that is the
  default and needs no API key.
- `CITATION.cff` and `.zenodo.json`, so the repository is citable and archives
  automatically on release.

### Notes

- Version DOI: [10.5281/zenodo.21757554](https://doi.org/10.5281/zenodo.21757554)
- Published to PyPI as [`aeo-audit-lite`](https://pypi.org/project/aeo-audit-lite/) via Trusted Publishing, with provenance attestations.
- Mirrored to [Codeberg](https://codeberg.org/clear-cited/aeo-audit-lite), tags included.

[0.1.0]: https://github.com/Clear-Cited/aeo-audit-lite/releases/tag/v0.1.0

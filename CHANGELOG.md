# Changelog

## Unreleased

### Documentation
- README "Install": `pip install sf-smartfeed` now that the first release is on PyPI, with how to check its provenance;
  "Status" says where it is published. `names.json` marks `sf-smartfeed` as registered.
- `publish/server.json` (the MCP registry manifest) is back under its normal name; it is not submitted to the registry yet.
- `site/playground.html`: each tool's install line now names its `sf-` package on PyPI; the README family table also lists SmartDelegate, SmartFabric, SmartLLMCost and SmartPolicyTranslator.
- Release check: the wheel installed in a clean environment now runs the README's demo command from an empty folder, not only `--version`.

## 3.0.0 — first PyPI release as `sf-smartfeed` (2026-10-09)

Published to PyPI on 2026-10-09 from tag `v3.0.0` by `.github/workflows/release.yml`, with provenance attestations. The version number is the same as the 3.0.0 entry below; these are the changes made before that first upload.

### Security
- Install instructions no longer name packages the maintainers have not
  published. Until the first release, install from a clone (README, "Install").
- New `SECURITY.md` (private vulnerability reporting), `names.json` (the only
  official package names) and a CI check that fails when a document names any
  other package.
- Releases are built and published only by `.github/workflows/release.yml`
  through PyPI trusted publishing, with provenance attestations.

### Changed
- **Renamed (breaking), `sf-` = Smart Family:** repository `SmartTasksOrg/sf-smartfeed`, PyPI package `sf-smartfeed`, command `sf-smartfeed`, import package `sf_smartfeed`, MCP server `io.github.smarttasksorg/sf-smartfeed`. The unprefixed names are not used any more, so nobody can be sent to a look-alike.
- README: "Install" and "Status" sections; the MCP marker on line 1 is the bare server name.
- `pyproject.toml`: SPDX licence, `NOTICE` in the wheel, "3 - Alpha" classifier, Source/Issues/Security/Changelog URLs.
- `make test` runs pytest (it ran a file that executed no test).
- `MARKETING.md` moved out of the public repository.

## 3.0.0 — the family release
- **Joined the Smart\* family**: shared mascot, manifesto, and `FEED-*` rule-ID style.
- **IAIso conformance**: implements **§9 · Awareness**; see `spec/iaiso-map.json`.
- **Cross-tool stacking**: composes with sibling tools via shared receipts + standard.
- **UML data objects** exposed in `src/smartfeed/models.py` and `site/playground.html`.
- **Ships with a synthetic demo** so `smartfeed --demo` works on clone.
- MCP server, pre-commit hook, and multi-language install parity.

## 2.x — standalone tool (pre-family)
## 1.x — initial release

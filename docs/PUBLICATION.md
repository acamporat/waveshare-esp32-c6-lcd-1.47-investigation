# Public snapshot verification

Prepared on 2026-10-09 from the owner's existing local investigation workspace. This publication task did not reconnect, flash or otherwise operate the board.

- Documentation consolidates the chronological notes instead of publishing mutually conflicting historical “current installation” paragraphs as current truth.
- Public files were selected by explicit allowlist into a separate repository. Original workspace/backups were retained locally.
- Text was checked for owner-specific Windows paths, unique device identifiers, old-project branding and common credential patterns. A second agent reviewed the package and relative links. Synthetic unit-test data was retained.
- The included CAD preview is a generated enclosure render; its PNG has no textual/EXIF metadata. Raw board/webcam photos were omitted.
- All 10 usage-bridge unit tests passed in the publication snapshot. These are offline tests; no current account read or serial session was started.
- All three STL meshes passed the existing checks: watertight, consistent winding, one connected solid each and positive volume. This does not establish physical fit, strength or printability on a particular printer.
- ESPHome 2024.11.0 accepted the published YAML using `esphome config`. It emitted historical-version/unknown-board and GPIO15-strapping warnings. Validation succeeded; no new compile/flash test was performed for publication. The historical successful build/run is documented separately.
- Markdown relative link targets were checked. The package deliberately links historical external sources but does not promise their future availability.

The snapshot is intended for reuse as agent context, not as a self-contained copy of every original experiment. The [evidence index](../evidence/README.md) lists what is and is not included. No account credentials, private flash dumps, toolchains or runtime account-usage files belong in future commits.

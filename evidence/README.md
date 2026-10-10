# Public evidence and private archive boundary

## Included evidence

| File | What it supports | What it does not support |
|---|---|---|
| [esphome-final-serial.txt](esphome-final-serial.txt) | Final application completed setup, reported the target settings, kept running and logged DIMMED12 | Visible pixels, physical continuity or correct electrical signals at the panel |
| [native-clock-count-serial.txt](native-clock-count-serial.txt) | Three MCU PCNT observations of 8 and 3840 expected GPIO7 clocks | Arrival/timing integrity at LCD pads or MOSI data correctness |
| [native-readback-serial.txt](native-readback-serial.txt) | Register read attempts returned all FF under the recorded changes | Controller identity, functioning readback wiring or a broken panel |
| [esphome-build-manifests.json](esphome-build-manifests.json) | Historical image sizes/hashes and version provenance | A downloadable firmware release or byte-identical fresh rebuild |

Serial files are selected copies from the local archive. ANSI formatting and excess blank lines were removed; numeric test results were retained. The final ESPHome log retains the display-operation duration warnings because successful execution and those warnings coexisted.

## Optical observations

The final run captured six full webcam frames at approximately 2, 8, 16, 25, 35 and 45 seconds. The main agent viewed representative bright and dimmed frames; a second agent independently reviewed all six. Both found no circle or convincing drawn pixels. Backlight dimming was visible. Raw images are retained privately and are **not included here**, so a reader can audit the runtime log directly but must distinguish the summarized optical review from published image evidence.

Earlier optical and user-observed results are summarized in the [test matrix](../docs/TEST_MATRIX.md). Some runs received full review and some sampled review; neither is silently generalized to every image ever captured.

## Not published

- Original and later 4 MB flash dumps, including possible configuration/credentials from the pre-existing project.
- Raw webcam/phone photographs, personal filesystem paths, device-unique serial/MAC identifiers and account-specific usage samples.
- Full downloaded vendor demos, third-party libraries, toolchain caches, disassembly and compiled firmware binaries.
- Most full diagnostic source variants, command transcripts and intermediate build logs. Their historical names in the matrix refer to the private archive, not missing public download links.
- Startup shortcuts, runtime status files and authentication/session state.

The initial firmware backup was locally checksum-verified and preserved. Restoration did execute an older application but did not produce visible output in the observed restore test. Conflicting shorthand notes about cold power cycling are explicitly unresolved; see the handoff. Public evidence does not prove the backup can restore a working display.

This repository preserves a curated context package rather than claiming complete forensic reproducibility. When a finding needs the omitted raw artifacts, ask the owner for an appropriately sanitized extract.

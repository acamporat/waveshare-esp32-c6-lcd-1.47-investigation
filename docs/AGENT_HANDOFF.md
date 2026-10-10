# Resume context for a person or agent

## What the owner originally wanted

A USB-powered display of Codex account usage percentages, fed from the connected PC, and a 3D-printed case sitting on top of an LG monitor. Approximate monitor thickness: 18 mm. An 8 GB microSD card was initially inserted. Wi-Fi was not requested. The monitor model and printer were never established.

The owner eventually stopped testing and put the project aside. Publication was requested to preserve learning and make future collaboration possible. **The request to publish does not restart hardware testing.**

## Last known installation

- Board: non-touch Waveshare ESP32-C6-LCD-1.47; identified MCU ESP32-C6FH4 revision 0.1, embedded 4 MB flash.
- Last installed image: `esphome-forum-polling.factory.bin`, 283680 bytes, offset `0x0`, SHA256 `2fcfcafb30c19fd1a4df0b48d97450622f0a67039582e5c9b3ba7cdde992eddc`.
- Actual ESPHome 2024.11.0, PlatformIO espressif32 6.5.0, ESP-IDF 5.1.2. The display implementation matched upstream by hash.
- Explicit backlight GPIO22, mode 3, 4 MHz, 172 × 320, ESPHome `offset_height: 34`, `offset_width: 0`, centered filled circle.
- Startup originally crashed in USB interrupt logger installation before display setup. Logger baud rate zero plus a `puts(message)` callback used the working IDF polling console. Setup then completed and heartbeats continued.
- Six frames through 45 seconds showed backlight only. The planned transition to approximately 12% brightness occurred and was visible. No circle appeared.
- Host serial/camera listeners closed. Usage bridge stopped; startup integration had been removed. No SD operation was part of the final test.

## Board mapping used

| Signal | GPIO |
|---|---:|
| LCD MOSI / SDA | 6 |
| LCD SCK | 7 |
| LCD CS | 14 |
| LCD DC | 15 |
| LCD reset | 21 |
| LCD backlight | 22 |
| RGB LED | 8 |
| SD CS | 4 |
| SD MISO | 5 |

Native full controller memory tests used 240 × 320; nominal visible portrait columns are 34–205. After axis swapping, correct landscape dimensions/window offsets were also tested. Do not assume the ESPHome offset field names mean the same thing as a different library's row/column arguments.

## What remains genuinely unknown

1. Whether correct electrical LCD control/data signals actually arrive at the soldered LCD pads. GPIO readback and internal PCNT measurements do not answer this.
2. The exact fitted controller/panel revision. A flex marking was read approximately as `FP-147BSC01A`; that is not a verified controller identification or datasheet.
3. Whether the panel exposes register readback in its wired mode. Repeated FF values cannot distinguish an unreadable interface, disconnected path or alternate controller.
4. Why the owner-reported previously working project no longer displayed pixels when the preserved initial image was restored. The precise cold-power-cycle sequence/evidence is not sufficiently reconciled to call it conclusively tested under every condition.
5. Whether a revision-specific power/reset/initialization requirement is missing. No verified alternate sequence fixed it.

## Useful next work, if the owner resumes

Choose a test that separates explanations and state that distinction first. These are proposals, not completed results or instructions to execute now:

- Ask Waveshare to identify the flex/board revision and provide a verified minimal binary and flash addresses for the exact non-touch 4 MB unit. An earlier support inquiry was drafted but not sent.
- Reconcile the initial firmware backup's provenance and cold-start history. Preserve it privately; do not publish the dump. If a restore/power-cycle experiment is requested, record actual boot and optical output together rather than relying on a stale serial listener.
- If instrumentation becomes available, compare reset, CS, DC, CLK, SDA and supply at the LCD pads with expected timing. This is the measurement gap left by software-only tests. The original owner had no meter or logic analyzer available.
- If another identical known-good unit becomes available, an agreed A/B experiment with the same minimal firmware could separate unit-specific behavior from assumptions about the model/revision. No such comparison has been performed.

Avoid treating another generic ST7789 example as a fresh idea. Vendor Arduino, several graphics libraries, native ESP-IDF, CircuitPython, actual MicroPython and actual ESPHome already reached the same optical outcome. See the matrix for the distinctions that matter.

## Archive limitations

Only selected evidence and source are public. Full local diagnostics, raw camera frames and original flash dumps exist in the owner's private workspace; this repository does not promise that a future collaborator has them. Published hashes identify historical files, not proof that a fresh build is byte-identical. Relative build-path normalization in the public YAML can change a new binary's hash without changing the display settings.

For a new session, first report current hardware availability, exact board identity, what evidence can be accessed and what the owner wants. Do not assume the board is still plugged in or the host environment still matches the historical one.

# Test matrix

Read [INVESTIGATION.md](INVESTIGATION.md) first. All tests concern one non-touch Waveshare ESP32-C6-LCD-1.47. **No intended image was confirmed during this project. No hardware defect was established.**

“User” means the owner reported the physical screen. “Camera” means captured images were visually reviewed. “Runtime” means serial markers, readback, or acknowledgements established execution; it does not mean LCD reception. Counts below come from the local diagnostic chronology and are states/captures, not distinct boards. Run identifiers name local evidence; the complete raw dataset is not published.

## Firmware and driver families

| Family / local source identifier | What was tried and what worked | Physical outcome | Evidence limits |
| --- | --- | --- | --- |
| Original usage firmware, `usage_display` | Adafruit ST7789-based usage UI; USB usage delivery acknowledged; SD recognized. Firmware built and flash-verified. | User: backlight, no intended UI. | End-to-end usage delivery does not validate physical text, percentages, orientation or colors. |
| Raw Arduino/vendor initialization | Direct SPI RGB/LCD TEST pattern bypassed Adafruit. | User: backlight only. | SPI API completion is not electrical measurement. |
| Preserved pre-project full flash | Original 4 MB image restored and hash-verified; old application emitted serial output. | User and automated reference: blank illuminated display. | Owner reports it worked before the project; it is not currently a known-good visual reference. Cold-boot provenance is qualified in the handoff. |
| Official Waveshare precompiled demo | Exact non-touch `ESP32-C6-LCD-1.47-Test.bin` flashed and hash-verified. | User: backlight only. | Do not conflate later captured Arduino-demo backups with this downloaded binary. |
| Vendor driver with original core, `vendor313_test` | Unchanged Waveshare LCD driver under Arduino ESP32 core 3.1.3; compile, flash verification and frame reporting passed. | User: no moving colored bands, only backlight. | Matching core/pins/init did not identify the cause. |
| TFT_eSPI, `tft_espi_test` | Upstream commit `16e37595040eac69cd628e4bffb56fc30cad6299`; one-line C6 processor-header selection correction; ST7789, 172×320, 34 offset, 10 MHz, inversion on. | User: backlight only after successful build/verified flash. | A locally patched compatibility build, not wholly unchanged upstream. SD remained deselected. |
| Arduino_GFX, `gfx159_test` | Arduino_GFX 1.5.9, Dev Device Pins 0.0.3 exact-board configuration, Arduino core 3.1.3; compile/flash/runtime reporting passed. | User: backlight only. | Confirms another software stack executed, not reception. |
| Early native IDF, `idf_lcd_diagnostic` | ESP-IDF 6.1 hardware SPI at 1 MHz and GPIO software SPI; GPIO low/high sampling; register reads. | User: backlight only. | MCU pin sampling passed; reads FF were inconclusive. |
| Arduino SD-first, `sd_first_lcd_test` | Card initialization at 400 kHz while LCD inactive, then display initialization. Build/flash passed; SD mount failed/card type 0. | User: backlight only with card inserted. | SD init itself did not succeed in this stack; later independent successful SD reads matter. |
| Exact-board CircuitPython 10.3.1 | Official prebuilt runtime, board-specific initialization, terminal and RGB/text tests; runtime verified. SD successfully read, then deselected. 80 MHz and 1 MHz; later no-card startup verified. | User: backlight only both with and without SD; software refresh returned success. | Successful refresh/object creation does not establish visible output. |
| Exploratory GC9307 sequence | CircuitPython with full 32-command LovyanGFX `Panel_GC9307` table from `e2cc321544fd4e2b6d02f613f3b8555210d2c690`; file readback, restart and refresh verified. | User: backlight only. | Not a verified GC9307N-specific driver; CircuitPython performed initial ST7789 setup before recreation. Silicon identity remains unknown. |
| Clean native IDF, `native_isolation_test` | No Arduino/CircuitPython, Wi-Fi/BLE or SD library; manual CS, 1 MHz SPI/DMA, 12% backlight. | Camera: no intended colors or shapes in completed first run. | Later startup-failed repeats are separate, not additional LCD failures. |
| Native interactive/staged, `boot_stages` | Explicit USB Serial/JTAG heartbeat, command ACKs and progressively controlled initialization/writes; successful execution through all phases. | Camera: backlight only. | Resolves execution ambiguity for these runs, not the signal path at the connector. |
| Actual MicroPython reference | Official ESP32_GENERIC_C6 1.29.0; unmodified `st7789py.py` from `7265925bd0c092e8105200d18b2dba9dfbc12c27`, device hash checked. Runtime/import/fills and persistent script verified. | Camera: backlight controls work; rotations/full-memory/visible-window/80 MHz colors do not. | Independent runtime and driver, rather than only a ported init table. |
| Actual ESPHome forum test | ESPHome 2024.11.0/IDF 5.1.2; CUSTOM, GPIO22, mode 3, 4 MHz, 172×320, offset_height 34, centered circle. Final polling-logger build runs without watchdog restart. | Six final camera captures: no circle; timed dimming works. | Initial logger-crash runs never reached display setup. Final run is the relevant display result. |

## Controlled observations and targeted experiments

| Local run ID | Completed observations | Controlled question | Result and boundary |
| --- | ---: | --- | --- |
| `control-01` | 15 states | Backlight 0/12/40%; display off/on, inversion off/on, sleep in/out. | Illumination follows backlight duty; no pixel response to panel commands. RGB reflection distinguished. |
| `direct-01` | 18 states | Direct `busio.SPI` with explicit CS/DC/reset, vendor init, 240×320 white/black/RGB, software reset, RGB666, modes 0/3, 100 kHz, longer reset. | No intended image. Bypasses displayio/FourWire. Full-memory white/black avoids hue/offset ambiguity. |
| `nine-bit-01` | 6 color states | Alternative three-wire nine-bit framing, D/C held high. | No intended colors. Does not establish fitted interface straps. |
| `original-reference-01` | 4 original + 2 restored CircuitPython timed images | Full original image at 2/8/16/30 s; restored CircuitPython at 3/10 s. | Both blank; flash hashes verified. Timed observations, not six independent configurations. |
| `cooldown-01` | 15 observations | Five minutes RGB/backlight off and LCD reset low; initialize before lighting; 1/5/12% brightness. | No colors; 12% white/black channel differences ≤0.13/255. Board stayed powered; CPU readings did not measure panel temperature. |
| `new-usb-port-04` | 9 states | Direct PC USB port; backlight control, white/black/RGB and repeats. | Backlight works, pixels remain blank. Camera moved; absolute ROI comparisons with prior runs invalid. |
| `new-usb-cable-01` | 9 captures | Replacement USB cable; repeat color states. | No correct full-screen colors; faint lines motivated next comparison. Automatic flashing succeeded. |
| `cable-lines-01` | 13 states | White/black alternation and no-op holds. | Thin line in six black states, absent in seven white states. Not proven intended pixel control; later not reproduced. |
| `positioned-01` | 20 states | 40×40 rectangles, individual rows at three positions, explicit readdressed row fills, deselected traffic control. | No intended pattern; line not clearly reproduced even in selected black states. CS-high control therefore inconclusive about line cause. |
| `native-isolation-01` | 15 phases | Clean native hardware SPI, colors, rectangles, rows, deselected controls. | All NEXT/DONE phases matched manifest; no intended image. Some frames blurred; sharp repeat white/black remained negative. |
| `alive-probe-01` | 6 consecutive heartbeat records, not six image tests | Can a no-LCD native application boot and acknowledge STATUS? | Yes: continuing heartbeat and ACK stage 0. No LCD claim. |
| `staged-probe-01` | 13 captures; 10 FRAME markers | ACK RESET/INIT/DRAW with continuing independent heartbeat; RGB/white/black twice. | All execution stages completed without stall; inspected colors and final white/black remain blank. No extra test-side reset after flash. |
| `logical-modes-01` | 19 states | Normal mode 13, idle off 38, MCU interface B1, RAM defaults B0, single-lane E7; minimal init; colors/off/on. | Full-frame review: no intended colors or defined pixel response. |
| `minimal-clock-01` | 7 states | Minimal setup at 100 kHz mode 0, 10 MHz mode 0, 1 MHz mode 3, return mode 0. | Inspected slow white/black and final mode-0 white remain blank. Slow/mode-3 vendor-init checks existed earlier too. |
| `native-readback-01` | Register probe, no image-state count claimed | D/C held low, SDA released, read ID/status/pixel format/orientation with changing writes. | All FF, not a confirmed panel response. Wiring/readback support unverified. |
| `native-buscheck-01` | 3 clock-count repetitions per transfer size; 3 color images | PCNT while LCD/SD deselected, then white/black/red. | Exactly 8 and 3,840 rising edges; all three images backlight-only. Confirms MCU clock path, not connector signal quality or MOSI contents. |
| `repeat-restart-01` | 18 captures, all reviewed | Single/repeated init without reset; double init after one LCD reset; repeat after MCU software restart. | No white/black/red fills. Reset reason changed to 3 and stage reset, confirming MCU restart. No reproduced line. |
| `window-01` | 33 captures; 13 sampled full-frame reviews | Eight MY/MX/MV combinations with correct full memory dimensions; four visible-offset/BGR rotations; 480-byte CS chunks; russhughes reset/double table at modes 0/3. | Reviewed frames showed no intended colors. Not all 33 frames independently optically reviewed. Native table port distinct from next actual-runtime test. |
| `micropython-reference-01` | 17 captures; 13 independently reviewed | Actual unmodified driver/runtime; four full-memory rotations, off/on control, visible offsets, 80 MHz comparison. | Backlight positive control works, reviewed pixel states do not. Persistent script soft-reboot later emitted three REFERENCE_FRAME markers. |
| `esphome-forum-03` | 6 timed captures, all reviewed | Exact forum display settings after logger workaround; captures through 45 s, dim after ~30 s. | Setup and ALIVE/DIMMED12 logged; no watchdog reset; no circle in any frame; dimming visibly works. Last installed state. |

## Incomplete attempts excluded from negative LCD totals

| Attempt / condition | Failed layer | Why it is not a completed display test |
| --- | --- | --- |
| Oversized Arduino sketch | Compile/partition capacity | No new running firmware established from that failed compilation. |
| Early new-port runs before `new-usb-port-04` | Host/runtime mismatch or startup ownership race | Expected REPL absent, or stale display object interrupted setup. |
| `cable-lines-comparison-01` | Host path resolution | Relative-path failure occurred before flashing. |
| `native-isolation-02` through `-06` | Boot/protocol/serial readiness | No completed display phases; one ROM DOWNLOAD boot captured; unsupported reset methods and timeouts observed. |
| `demo-coldboot-01` / `-02` | Observation window | Passive listeners saw no relevant serial event; long listener expired before reported power cycle. |
| `esphome-forum-01` / `-02` | USB interrupt logger startup | Watchdog reset before display setup; first observer also had stdout encoding failure. Final corrected run is `-03`. |

## Interpretation rules

A command state is counted only when its execution was acknowledged. A brightness change is a positive control for seeing the board, not proof of LCD data reception. Camera autoexposure was not verifiably locked; inspect the full screen and compare large intended changes within the same run. Avoid summing the table into an impressive-looking “number of tests”: it mixes probes, repetitions, timed images, runtime checks, and different levels of optical review.

The strongest remaining gap is direct evidence at the panel interface. Controller power, reset level, continuity and SPI arrival at the connector were not measured. The current data supports “many software configurations executed but the intended display output was not observed,” not “the hardware is definitely broken” or “the software has been proven universally correct.”

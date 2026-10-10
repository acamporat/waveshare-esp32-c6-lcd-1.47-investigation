# Investigation handoff: backlight works, LCD pixels unresolved

Status recorded 2026-10-09. The owner paused the project and planned to put the board in storage. This is an investigation archive for humans and future coding agents, **not a working display tutorial or a confirmed hardware diagnosis**.

## Outcome and intended project

The intended device is a USB-powered Codex usage percentage display, with live updates from a Windows host and a printed case perched on an approximately 18 mm thick monitor. Firmware, a host bridge, and an enclosure design were produced. USB delivery of usage data was acknowledged by the MCU. No firmware tested during this investigation produced a confirmed working image on the physical LCD. The enclosure has not been physically fit-tested.

The owner reports that this same board displayed another project before this work began. Preserve that report as relevant history. The old firmware has been preserved privately, but it has not produced a visible image during this investigation. Neither this history nor the negative tests establishes which component or layer is responsible.

**Last installed firmware:** actual ESPHome 2024.11.0, ESP-IDF 5.1.2, using the supplied forum ST7789V CUSTOM circle configuration. Its USB logging startup problem was corrected. Successful setup, continuing heartbeat messages and backlight dimming were observed; six webcam captures still showed no circle. No original/demo restoration followed that final test. The usage bridge is stopped, automatic startup was disabled, and host camera/serial test processes were closed.

## Board identity and wiring

The photographed board is the **Waveshare ESP32-C6-LCD-1.47, non-touch**, with an ESP32-C6FH4 and 4 MB embedded flash. Do not substitute the touch board's pinout.

| Signal | GPIO / specification |
| --- | --- |
| LCD MOSI / SDA | 6 |
| LCD clock | 7 |
| LCD chip select | 14 |
| LCD data/command | 15 |
| LCD reset | 21 |
| LCD backlight | 22 |
| Addressable RGB LED | 8 |
| SD chip select | 4 |
| SD MISO | 5 |
| SD shared clock / MOSI | 7 / 6 |
| Visible LCD | 172 × 320 pixels; documented 34-column offset within 240 × 320 memory |

Waveshare documentation identifies ST7789V3. A vendor-hosted panel drawing also names a GC9307N alternative. A ribbon marking appeared to read `FP-147BSC01A`, but no verified datasheet for that exact marking was found. **The actual controller silicon was not identified.** Failed register reads do not resolve that question.

The schematic places LCD-controller power on 3.3 V with a separate backlight circuit. Illumination therefore verifies a different function from receiving commands or displaying pixels. LCD connector schematic pins are VDD 4, GND 1/5/6/12, DC 7, CS 8, CLK 9, SDA 10, reset 11. These are schematic numbering, not instructions to infer physical pad orientation from a photo.

## What worked

- The USB device was identified, firmware uploads completed, and full-image flash hashes were verified repeatedly. A different host USB port and replacement cable were tested.
- Later minimal native firmware booted automatically, maintained independent heartbeats, acknowledged commands, and continued running through LCD reset, initialization and frame writes. This separated an earlier startup problem from the still-blank LCD.
- GPIO22 backlight PWM visibly responded to off/on and several brightness levels. The addressable LED also operated, but its reflected light was distinguished from LCD output.
- The original full 4 MB flash backup was retained. Other historical snapshots were retained privately. Tests eventually stopped making/restoring redundant backups at the owner's request.
- SD maintenance succeeded when explicitly authorized: an approximately 8 GB card was formatted FAT32 and passed mount and file write/read/delete checks. Later CircuitPython independently read its block count and boot-sector signature. Generated LCD patterns did not require SD files.
- Native PCNT counted exactly 8 clock edges for one transmitted byte and 3,840 for 480 bytes, each repeated three times. This is evidence at the MCU input path, not a measurement at the LCD solder joints.
- Actual independent CircuitPython, MicroPython and ESPHome runtimes executed, beyond merely copying their initialization tables into our own driver.
- Camera runs paired serial completion markers with fresh full-frame images. Backlight changes served as an optical positive control. The final ESPHome logger workaround eliminated a real startup watchdog failure without changing its display driver.

## What did not work

The major families are catalogued in [TEST_MATRIX.md](TEST_MATRIX.md). They include official demo firmware, restoration of the pre-project image, unchanged vendor driver on the original Arduino core version, Adafruit, TFT_eSPI, Arduino_GFX, native hardware/software SPI, CircuitPython, MicroPython and actual ESPHome.

Across these families, full-screen white/black/RGB, text, circles, positioned rectangles, individual rows, orientations, address windows, alternative initialization sequences, reset timing, repeated initialization, MCU restart, data formats, transfer framing, clock speeds and SPI modes did not yield a confirmed intended image. These are repeated negative observations on one board, not proof that all such libraries fail generally or that the hardware is defective.

A thin line briefly correlated with black states in a 13-state cable follow-up: present in six black states and absent in seven white states. It did not reliably recur in the following 35 positioned/native states or the later repeat-initialization review. It was never successful rendering; reflections, focus or camera effects were not fully excluded.

## Failures of the test setup that must not be counted as LCD failures

1. An Arduino demo exceeded the selected application's partition size: 1,633,540 bytes versus a 1,310,720-byte limit. That was a build/partition configuration failure, not proof of LCD behavior. Later builds and flashes succeeded.
2. Early new-port runners expected a CircuitPython REPL while an Arduino application was installed. Another runner interrupted startup and touched a stale display object. Ownership and timeout handling were corrected before counting completed states.
3. Several native-isolation repeats never reached READY/STATUS, including a captured ROM download-mode boot. Watchdog reset and stub soft-reset routes were unsupported on this C6. Those runs did not execute their LCD phases. Manual-reset timing and serial-listener windows complicated observation.
4. One long listener expired before the owner confirmed unplug/replug. The requested cold-start log was not captured. Later explicit USB Serial/JTAG heartbeat firmware did boot and run; host protocol and power-cycle conditions changed together, so the original startup cause was not isolated.
5. One host wrapper failed on a relative restore path before flashing. Paths were corrected. A camera cleanup path was also strengthened; neither failure establishes an LCD result.
6. The first actual ESPHome build needed a compatible setuptools version and a console-baud compile definition for ESP-IDF 5.1.2. These were build compatibility fixes, not display fixes.
7. Initial ESPHome boots watchdog-reset about 5.4 seconds into startup. The decoded stack was inside USB interrupt logger installation, before display setup. One observer also hit Windows stdout encoding trouble; retained logs still showed the watchdog. The final run used `logger.baud_rate: 0` plus a polling USB log callback. Only that final run counts as a completed ESPHome display experiment.

## Final ESPHome experiment, precisely

Actual ESPHome **2024.11.0**, PlatformIO `espressif32` **6.5.0**, ESP-IDF **5.1.2** and an isolated Python **3.12.15** environment were used. The generated ST7789V source matched upstream SHA256 `7ebfd99e94c76e3fc38deefc90a090e1edd665ac77854075255dd91e8422a502`.

The tested display settings were CUSTOM, GPIO7 clock, GPIO6 MOSI, GPIO15 DC, GPIO14 CS, GPIO21 reset, GPIO22 backlight, height 320, width 172, `offset_height: 34`, `offset_width: 0`, SPI mode 3, 4 MHz, and a filled radius-20 circle at the center. No Wi-Fi, API or SD component was configured. In this ESPHome version, the confusingly named `offset_height` is applied to the column/X address; do not swap it merely because its name sounds wrong.

The driver retained its initial backlight-high behavior for approximately 30 seconds after the boot automation began, then an application helper dimmed GPIO22 to about 12% with LEDC. The upstream display driver and circle lambda were not altered. This was a short controlled test; continuous-use brightness should follow the manufacturer's guidance.

The logger correction skipped the problematic interrupt logger installation and forwarded messages through the existing IDF polling USB console. The final factory image, flashed at offset zero, was 283,680 bytes with SHA256 `2fcfcafb30c19fd1a4df0b48d97450622f0a67039582e5c9b3ba7cdde992eddc`.

The final run recorded successful setup, requested pins and SPI settings, repeated `ALIVE circle test`, and `DIMMED12`, without a watchdog reset through the observation interval. All six images at 2/8/16/25/35/45 seconds were reviewed: no circle or convincing drawn pixels; dimming was visibly effective. Display-operation warnings around 362 ms persisted while the program continued running. They are not equivalent to the earlier startup crash.

## Original firmware and cold-start provenance

The owner's original full 4 MB image was saved before project firmware changes. Its checksum was checked against the saved manifest. Inspection found the same LCD pins, a vendor-style initialization sequence and Arduino core 3.1.3; no SD mount or startup-button prerequisite was identified in the inspected startup code. This reduces the plausibility of a missing SD asset requirement, but reverse engineering is not a complete behavioral specification.

The image was restored and flash-verified, and an automated reference run observed it at 2/8/16/30 seconds: all images remained blank. Serial output established execution of that old application. **It is a preserved original, not a currently verified working reference.**

There is a provenance conflict in historical notes: the older root README says the original remained blank after a full USB power cycle, whereas the detailed automated reference run documents an additional USB reset, and a later requested cold-boot listener missed the physical event. A future investigator should not treat a precisely controlled, camera-and-log-observed cold boot of that exact original image as conclusively established by the public archive. Recheck source records before making that claim.

Full flash dumps can contain private data and are not published here. Their absence is deliberate; a future agent must not expect to find the owner's original image in this repository or replace it with a guessed binary.

## False leads and claims to avoid

- **Touch versus non-touch:** the linked Tasmota discussion concerns an 8 MB touch variant with different pins. Its uDisplay option is not a fix for Arduino or CircuitPython.
- **Wrong chip pin examples:** GPIO45/47 snippets do not match this ESP32-C6 board. Pin assignments were verified against the non-touch documentation and original firmware.
- **SD requirement:** solid colors and a programmatically drawn circle need no SD assets. SD-first initialization was a reasonable shared-bus hypothesis, tested both with a successfully readable card and without a card; neither restored pixels.
- **Missing backlight configuration:** explicit GPIO22 handling was tested repeatedly, including the actual forum configuration. The backlight responds but pixels remain unresolved.
- **All-white addressing:** a full 240 × 320 memory fill includes the documented visible columns 34–205. A claim that it necessarily misses the visible window is incorrect. Correct rotated dimensions and explicit visible windows were also tested.
- **All-ones register reads:** `FF` is not positive controller identification and does not prove disconnection or damage. The display's usable readback interface is unverified; shared-bus pull-ups matter.
- **Nine-bit mode:** this was an alternate framing experiment, not evidence of the fitted interface straps.
- **GC9307:** a vendor drawing's alternative part name motivated an exploratory sequence; it did not identify the silicon. The test also inherited an initial ST7789 setup from CircuitPython before releasing/recreating the display.
- **Reset success:** flash verification, a reset command, or a silent serial port does not establish application execution. Demand an ongoing heartbeat/ACK before calling a display phase completed.
- **Camera differences:** fingerprints, glare, RGB LED reflections and automatic exposure are not drawn pixels. Do not compare absolute image statistics across changed camera positions.
- **Cooling:** the five-minute lights-off/reset-low interval left the board powered. CPU temperature readings are not panel temperatures or evidence of a full cold start.
- **Internet research output:** a supplied research report contained incorrect addressing/MADCTL reasoning and an unsubstantiated “known working” reference. Treat generated research as leads requiring source verification.

## Resume guidance for a future agent

Start by reading this document and the matrix. The project is paused; publishing this archive did not authorize a new hardware test. When work resumes, identify the currently connected device and installed firmware afresh. Never assume an old serial-port number still belongs to this board. Keep the usage bridge stopped while diagnostics own the port.

Preserve any original backup before changing firmware. Do not repeatedly restore demos or make redundant backups merely to repeat tests. Several historical wrappers contain automatic restoration in `finally`; inspect those behaviors before reusing them. Flash only a binary whose target, size, offset and provenance are understood. A merged factory image at offset zero is not interchangeable with an application-only image.

A useful next experiment must distinguish remaining hypotheses. Unmeasured items include LCD-controller supply/reset state and the arrival/quality of CS/DC/clock/data at the actual connector. No meter or logic-analyzer measurements at that connector were available. These gaps do not establish a hardware defect. A known-good identical board, a vendor-reviewed exact panel revision, or a fully observed cold boot of the preserved original could provide comparisons if authorized and available. Do not promise any of them will fix this unit.

For each future run record: hypothesis; one controlled change; firmware/runtime versions and hashes; build and flash outcome; explicit runtime acknowledgement; camera/user observation; and interpretation limits. Stop counting at the failed layer. A successful build is not a successful flash; a successful flash is not a boot; boot and SPI API completion are not visible acceptance.

## Source trail and archive limits

This narrative was consolidated from local `firmware/LCD_DIAGNOSTICS.md`, root README, camera-test README, TFT_eSPI and MicroPython reference READMEs, ESPHome README and final ESPHome serial log. Those historical documents contain chronological installed-state statements that were later superseded. This handoff's final state takes precedence over older “currently installed” paragraphs.

Run names in the matrix identify local evidence directories under `firmware/camera_test/`. Full raw camera frames, serial logs, downloaded tools, caches and private flash snapshots are **not published as a complete evidence dataset**. The matrix records the evidence basis rather than pretending the public repo contains every artifact. Counts are captured command states or timed observations, not independent devices or statistically independent trials.

Selected sanitized serial logs are included; see the [public evidence index](../evidence/README.md) for their exact scope and limitations.

Primary references used during the investigation:

- [Waveshare non-touch board documentation](https://docs.waveshare.com/ESP32-C6-LCD-1.47)
- [Waveshare schematic](https://files.waveshare.com/wiki/ESP32-C6-LCD-1.47/ESP32-C6-LCD-1.47_schemetics.pdf)
- [Waveshare LCD manual](https://files.waveshare.com/wiki/ESP32-C6-LCD-1.47/1.47_LCD_Manual.pdf)
- [Espressif shared SD/SPI bus requirements](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c6/api-reference/peripherals/sdspi_share.html)
- [Espressif C6 download-mode reset caveat](https://docs.espressif.com/projects/esptool/en/latest/esp32c6/troubleshooting.html#leaving-download-mode-in-usb-serial-jtag-mode)
- [CircuitPython exact board](https://circuitpython.org/board/waveshare_esp32_c6_lcd_1_47/) and [10.3.1 board initialization](https://raw.githubusercontent.com/adafruit/circuitpython/10.3.1/ports/espressif/boards/waveshare_esp32_c6_lcd_1_47/board.c)
- [Pinned MicroPython ST7789 driver](https://github.com/russhughes/st7789py_mpy/tree/7265925bd0c092e8105200d18b2dba9dfbc12c27)
- [ESPHome 2024.11.0 ST7789V implementation](https://github.com/esphome/esphome/blob/2024.11.0/esphome/components/st7789v/st7789v.cpp)
- [Forum configuration tested](https://community.home-assistant.io/t/help-needed-to-get-this-tiny-screen-working-esp32-c6-1-47in-display/800102)
- [TFT_eSPI pinned revision](https://github.com/Bodmer/TFT_eSPI/tree/16e37595040eac69cd628e4bffb56fc30cad6299)
- [LovyanGFX exploratory GC9307 sequence](https://github.com/lovyan03/LovyanGFX/blob/e2cc321544fd4e2b6d02f613f3b8555210d2c690/src/lgfx/v1/panel/Panel_GC9A01.hpp)
- [Tasmota touch-board discussion](https://github.com/arendst/Tasmota/discussions/24876) and [COM-port troubleshooting video](https://www.youtube.com/watch?v=Q0QM_0RbxCU), reviewed but not matching the unresolved pixel symptom.

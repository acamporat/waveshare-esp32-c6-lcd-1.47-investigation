# Final ESPHome reference: runs, but LCD remains blank

This is the final tested display configuration from the investigation. **It did not fix the LCD.** Read the root handoff before using it on hardware.

The actual ESPHome ST7789V component was used, not a reimplementation. Tested versions: ESPHome 2024.11.0, Python 3.12.15, PlatformIO 6.1.16, espressif32 platform 6.5.0, ESP-IDF 5.1.2 (`framework-espidf@3.50102.240122`). The generated `st7789v.cpp` matched upstream SHA256 `7ebfd99e94c76e3fc38deefc90a090e1edd665ac77854075255dd91e8422a502`.

`forum.yaml` preserves the forum's CUSTOM model, GPIO7 clock, GPIO6 MOSI, GPIO15 DC, GPIO14 CS, GPIO21 reset, GPIO22 backlight, 172 × 320 resolution, offset_height 34 / offset_width 0, SPI mode 3 at 4 MHz, and radius 20 filled circle at the center. No Wi-Fi, API or SD component is configured. The public copy changes only the build output directory to a relative path compared with the final tested YAML.

## Compatibility changes that mattered

1. The historical PlatformIO build required `pkg_resources`. Pinning isolated host setuptools to 75.6.0 fixed the failure caused by a newer setuptools release removing it.
2. IDF 5.1.2 referenced `CONFIG_ESP_CONSOLE_UART_BAUDRATE` in a sleep calculation even with the USB console selected. The build flag in the YAML supplies 115200; no SDK or LCD driver source was patched.
3. The first running image hit a watchdog during `usb_serial_jtag_driver_install`, inside logger pre-setup, before display setup. The decoded stack included `esp_intr_alloc_intrstatus` and `Logger::pre_setup`. Setting logger `baud_rate: 0` skips its interrupt-driver installation; the `on_message` callback uses `puts(message)` over the already working IDF polling USB console. This allowed setup to complete. The underlying interrupt-allocation defect was not fully diagnosed; the workaround solved that observed startup path.

The watchdog run is not a valid LCD result. The corrected run completed setup, repeatedly logged `ALIVE circle test`, reported all requested display settings, and logged `DIMMED12`. Six frames through 45 seconds showed only backlight. Display operation warnings around 362 ms were nonfatal in this run; suppressing them would not demonstrate a fix.

## Brightness instrumentation

The unmodified driver's GPIO22 full-on behavior is retained for the first 30 seconds after boot automation. `dim_backlight.h` then switches GPIO22 to 1 kHz LEDC PWM at 123/1023 (~12%). Both phases were observed, and no circle appeared in either. The transition is instrumentation rather than an LCD fix. Manufacturer guidance limits sustained brightness; this is not a production brightness policy.

## Build reference — does not flash

Use an isolated Python 3.12 environment and install:

```text
esphome==2024.11.0
platformio==6.1.16
setuptools==75.6.0
```

From the repository root:

```sh
python -m esphome compile firmware/esphome_forum/forum.yaml
```

A first build downloads toolchains. The archived successful build produced a merged `firmware.factory.bin` for offset 0x0. No binary is distributed here, and a rebuild may not be byte-identical. See [historical manifests](../../evidence/esphome-build-manifests.json). Flashing requires a separate, explicitly requested hardware operation and correct identification of the connected device.

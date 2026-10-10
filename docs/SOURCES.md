# Historical source map

These links identify material consulted during the investigation. They are not endorsements of a fix; external pages and default branches may change. Version-pinned source and local observations take precedence over an unrelated board example.

- [Waveshare ESP32-C6-LCD-1.47 documentation](https://www.waveshare.com/wiki/ESP32-C6-LCD-1.47): non-touch board, official demo/driver, drawings and pin mapping. Also [manufacturer documentation site](https://docs.waveshare.com/ESP32-C6-LCD-1.47).
- [Home Assistant community: help getting this tiny screen working](https://community.home-assistant.io/t/help-needed-to-get-this-tiny-screen-working-esp32-c6-1-47in-display/800102): source of the GPIO22 / SPI mode 3 / 4 MHz circle configuration. Another user's reported success did not reproduce on this unit.
- [ESPHome ST7789V source at 2024.11.0](https://github.com/esphome/esphome/blob/2024.11.0/esphome/components/st7789v/st7789v.cpp) and [configuration schema](https://github.com/esphome/esphome/blob/2024.11.0/esphome/components/st7789v/display.py): final test used the actual implementation, not a native rewrite of its initialization table.
- [russhughes st7789py driver, pinned commit](https://github.com/russhughes/st7789py_mpy/blob/7265925bd0c092e8105200d18b2dba9dfbc12c27/lib/st7789py.py): both a native sequence comparison and a later independent actual MicroPython run were tested; they are separate experiments.
- [MicroPython ESP32_GENERIC_C6 downloads](https://micropython.org/download/ESP32_GENERIC_C6/): independent runtime used version 1.29.0 dated 2026-08-24.
- [TFT_eSPI](https://github.com/Bodmer/TFT_eSPI): tested after C6 processor compatibility work; did not restore pixels.
- [Arduino_GFX](https://github.com/moononournation/Arduino_GFX): tested version 1.5.9 with exact-board pin configuration.
- [Adafruit ST7735/ST7789 library](https://github.com/adafruit/Adafruit-ST7735-Library): another earlier graphics-library test family.
- [Tasmota discussion 24876](https://github.com/arendst/Tasmota/discussions/24876): examined, but involves the similarly named touch board. Do not import its pin map into the non-touch target.
- [User-provided video](https://www.youtube.com/watch?v=Q0QM_0RbxCU): examined during troubleshooting; not evidence of a successful LCD fix on this unit.

A user-supplied deep research report was also reviewed locally. It is not redistributed. Some of its claims were rejected: full 240 × 320 writes do include the nominal visible 34–205 column range; all-FF reads do not identify GC9307; and a suggested example was not verified working merely because it appeared in a search result.

# Independent MicroPython reference

This example ran using actual MicroPython and the original driver, independently of the native C diagnostic. **No intended pixel colors appeared.**

- Runtime: official ESP32_GENERIC_C6 MicroPython 1.29.0, dated 2026-08-24.
- Historical firmware SHA256: `3688ba4e2c3949e639f5772e99fdb0efa1258b162a496133f78c108434195c89` (1,967,664 bytes).
- Driver: [st7789py.py at commit 7265925bd0c092e8105200d18b2dba9dfbc12c27](https://github.com/russhughes/st7789py_mpy/blob/7265925bd0c092e8105200d18b2dba9dfbc12c27/lib/st7789py.py).
- Driver SHA256 verified on device: `a071cfc56a32006b3ddefcc1b68e158fbd7674df6a363cac59ea7ce9510ed958`.

The driver is not bundled. Obtain it from the pinned source and retain its MIT notice when using it. `main.py` requires that driver and a compatible MicroPython runtime; it does not run under desktop Python.

The preserved example cycles full 240 × 320 memory through white, black, red, green and blue at 1 MHz mode 0, with 12% backlight and SD CS held high. Full memory includes the nominal visible 172 × 320 region. Frame markers confirm Python execution and write completion, not pixels on the LCD.

The larger private host-driven experiment completed 17 captured states covering rotations, explicit visible offsets, backlight off/on and a high-clock comparison. Sampled review of 13 frames found no intended fills; backlight off/on did visibly respond. The persistent example then emitted three successive frame markers after installation. It was later replaced by the ESPHome test, which is the last known installation.

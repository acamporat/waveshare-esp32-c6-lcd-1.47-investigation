# Attribution and scope

The repository's MIT license covers original investigation documentation, authored examples, bridge prototype and enclosure CAD. It does not relicense externally linked projects, vendor binaries, libraries, firmware distributions or forum content.

The final display configuration was tested following a user-supplied report in the [Home Assistant community thread](https://community.home-assistant.io/t/help-needed-to-get-this-tiny-screen-working-esp32-c6-1-47in-display/800102). It retains that report's pin assignments, geometry, clock/mode and simple centered-circle drawing operation, with local logging and brightness instrumentation described in its README.

The MicroPython example depends on the external MIT-licensed russhughes st7789py driver; that driver is not copied into this repository. Preserve its upstream license if obtaining or redistributing it. ESPHome, ESP-IDF, MicroPython, graphics libraries and other dependencies retain their respective licenses. Manufacturer drawings and downloaded demo bundles are linked rather than redistributed.

Waveshare, Espressif, ESPHome, MicroPython, OpenAI/Codex and LG are referenced for identification. This is an independent investigation and is not an official support publication from any of them.

# Codex monitor-top case — prototype v1

Designed for the non-touch **Waveshare ESP32-C6-LCD-1.47**, in landscape orientation, and the user's approximately **18 mm thick LG monitor**. These are generated printable parts, not a physically fitted or printer-tested product. No print has been started.

## Files

- `codex_monitor.scad`: editable parametric master; select `part` for individual pieces.
- `stl/case.stl`: open-back protective cradle, USB/buttons exposed, removable with two M3 screws.
- `stl/saddle.stl`: gravity-supported padded monitor bridge, two slots for adjustment.
- `stl/rear_stop.stl`: movable rear locating foot; **not a tightening clamp**.
- `assembly.png`: assembled CAD view. Translucent monitor and turquoise LCD are reference geometry, not printed pieces.
- Manufacturer drawings are linked through the Waveshare documentation; they are not redistributed here.
- `mesh-check.json`: generated geometric checks; does not establish real-world fit.

## Dimensions and assumptions

Official [Waveshare documentation](https://docs.waveshare.com/ESP32-C6-LCD-1.47) gives PCB 36.37 × 20.32 mm, assembled thickness 7.60 mm, LCD module 36.28 ±0.2 × 19.39 ±0.2 mm and active area 32.35 × 17.39 mm. Four factory M2 mounts have 32 mm long-axis spacing; short-axis spacing is 13.28 mm away from USB and 16.32 mm at USB. Their asymmetry is included in the model. There is 0.55 mm clearance per PCB edge. The cradle's rear is open for cooling and microSD service; its front is open so printed plastic does not press on the LCD. Service access may require removing the cradle from its stand.

The design assumes **no soldered GPIO headers**. If this is the `-M` header version or headers are fitted, inspect pin projection before assembly; increase depth or revise the rear openings as needed. Do not trim pins to fit this prototype.

The saddle adjusts for roughly **14–32 mm** monitor thickness with 1 mm soft pads on both faces. The initial position is 18 mm + 2 mm pads. The 3 mm front lip must touch only the structural bezel, never the active screen or thin display glass. The model is a starting point for the approximate thickness; LG model, local top contour, structural bezel depth and nearby vents still need verification. For an edge-to-edge glass panel set `front_lip=0` and use a suitable removable top-support adhesive instead, after checking the surface; that change needs fresh STL export.

## Hardware and printing

- 4 × M2 × 5 mm pan-head screws for the factory mounts: through 3 mm printed pads gives approximately 2 mm engagement. **Verify mount thread/depth on your actual unit before tightening.** Use a shorter screw or washer if needed; never bottom out into the display.
- 4 × M3 × 10 mm pan-head screws, 4 nuts, 8 small washers: two join cradle to mast, two lock the sliding rear foot. Standard nuts remain accessible, no inserts required.
- 1 mm silicone/EPDM or felt strips on the top bridge, front lip and rear foot; use nonconductive material. Keep pad adhesive away from circuit components.
- PETG is preferred for a monitor's warm top. Start with a 0.4 mm nozzle, 0.20 mm layers, 3–4 walls and 25–35% infill. Printer/material dependent; these settings have not been sliced or tested.
- Cradle: rear mounting pads down, front rim up. The exported saddle is edge-on with its front lip on the bed; add a brim and supports beneath the elevated mast. The rear foot is on its broad outside wall. Inspect first-layer contact and overhangs in your slicer. Remove all support debris before fitting electronics.
- Print one of each. Smallest screw holes may need gentle hand reaming to 2.35/3.4 mm. Do not drill with electronics installed.

## Assembly and fit check

1. Measure monitor thickness at the exact mounting location, minimum structural top-bezel depth, and USB plug overmold width/height. Ensure the location does not cover ventilation slots, camera, sensors or buttons.
2. With board unplugged, dry-fit it in the cradle, screen outward. USB points right when viewed from the front. Factory posts sit on the four rear pads; no printed feature should load the glass, push a button or touch a component. Check SD insertion/ejection travel. Do not force the fit.
3. Fasten the four M2 screws gently from the rear into the factory mounts. Confirm safe engagement before tightening. Secure cradle to the saddle mast with two M3 bolts and washers.
4. Add soft pads, set rear-foot spacing to measured monitor thickness plus both face pads, and fasten the slot bolts. Rest the saddle on the monitor by gravity. It must locate lightly, with no squeezing force on the panel. Check stability by hand before releasing it.
5. Route USB cable toward the rear with slack and a separate cable tie/adhesive strain relief on a suitable rear surface. The USB connector and case must not carry cable tension. Remove the assembly if it rocks or bears on screen glass.
6. Confirm LCD visibility, buttons, USB and SD operation after mounting. Inspect temperature after an hour; firmware brightness should stay at or below Waveshare's recommended 50%.

## Regeneration

The original exports used OpenSCAD 2021.01. Install OpenSCAD separately; no runtime is bundled. With openscad.com on PATH, from the repository root in PowerShell:

```powershell
& openscad.com -o enclosure/stl/case.stl -D 'part="case"' enclosure/codex_monitor.scad
& openscad.com -o enclosure/stl/saddle.stl -D 'part="saddle"' enclosure/codex_monitor.scad
& openscad.com -o enclosure/stl/rear_stop.stl -D 'part="rear_stop"' enclosure/codex_monitor.scad
python -m pip install trimesh numpy
python enclosure/check_mesh.py
```

Check all changed exports in a slicer and repeat the physical fit check. Mesh validity and CAD rendering do not establish load capacity, monitor compatibility, or safe screw engagement.

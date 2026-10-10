# Codex usage bridge prototype

This is useful retained work from the original goal, separate from the unresolved LCD. Historical local Codex account-rate-limit retrieval worked; the physical usage display never worked end to end. No credentials, real usage samples, runtime state or startup integration are included.

The Python bridge uses an installed, authenticated Codex CLI's `app-server` stdio interface: `initialize`, `initialized`, then `account/rateLimits/read`. It does not create a model turn or read an authentication file. This is a historical implementation against the locally available experimental protocol, not a guarantee of compatibility with future Codex versions.

It prefers the account `codex` limit bucket, identifies windows by duration, treats missing values as unavailable and clamps valid consumed percentages to 0–100. It transmits only an allowlisted JSON packet to USB serial; it does not forward arbitrary account/API data.

## Offline verification

From the repository root:

```sh
python -m unittest discover -s bridge -v
```

Tests use synthetic values for bucket selection, missing/invalid data, duration labeling, clamping and acknowledgment filtering. They do not verify an LCD or current authentication.

## Optional execution when resuming

```sh
python -m pip install -r bridge/requirements.txt
python bridge/usage_bridge.py --once
```

`--once` reads and prints the allowlisted usage packet without opening serial. It uses your local account; do not paste its output publicly without reviewing it.

Normal mode (`python bridge/usage_bridge.py --port YOUR_PORT`) opens the explicitly chosen serial port at 115200 baud. The code also has USB VID303A/PID1001 discovery; if multiple devices match, use an explicit verified port. Stop it before flashing or opening another monitor. No bridge process or startup task should be started just to inspect this archive.

The bridge polls every 60 seconds and resends the latest packet every 5 seconds. Repeats preserve the original sample timestamp. It writes a bounded local `runtime/status.json` and uses a process lock. Runtime files are ignored by Git.

## Protocol

Newline-delimited JSON; this example is synthetic:

```json
{"type":"usage","windows":[{"label":"WEEK","used":25,"reset":null,"minutes":10080}],"updated":1700000000}
{"type":"status","message":"Codex unavailable - check PC"}
```

`used` means consumed, not remaining. Labels derive from 300-minute or 10080-minute windows; other durations become OTHER. Missing windows are unavailable, never zero. A receiving UI must clear missing windows and determine staleness from the sample timestamp, not repeated serial receipt. A status/error packet must not make old data look current.

The original Arduino usage-display sketch and startup scripts remain private/local and are not part of this curated snapshot. The final installed ESPHome diagnostic does not implement this usage protocol, so starting the bridge will not turn that diagnostic into a usage display.

# bb-coord 🌍

So you've got coordinates in 6 different formats and none of them match. Same. That's literally why this exists.

bb-coord is a command line tool for Linux that converts messy, inconsistent coordinate formats into clean standard **Decimal Degrees (DD)** — straight from your terminal. No copy-pasting into online converters, no browser, no nonsense. Just paste your coords and get a clean result.

---

## What it can do 🔥

- Auto-detects the coordinate format — no flags, no config
- Converts **6 formats** to Decimal Degrees in one command
- Shows you the detected format label in every result (`[DMS]`, `[MGRS]`, `[UTM]`, etc.)
- Handles a **single coordinate** or scans an **entire .txt file** of mixed formats
- Auto-installs missing Python dependencies on first run
- South and West coordinates are automatically negated — no manual sign flipping

---

## Supported Formats

| Format | Example Input |
|--------|--------------|
| DMS (Degrees Minutes Seconds) | `40 26 46 S, 79 58 56 W` |
| DDM (Degrees Decimal Minutes) | `40 26.767 S, 79 58.933 W` |
| DD with Direction | `40.446 S, 79.982 W` |
| Signed DD | `-40.446111, -79.982222` |
| MGRS | `17TPE8056816806` |
| UTM | `17N 580568 4477606` |

---

## Requirements

- Linux
- Python 3.9+
- `mgrs` and `pyproj` — **auto-installed on first run**

---

## How to install

### Option 1 — Run from source (recommended)

```bash
git clone https://github.com/amtechguy/bb-coord.git
cd bb-coord
```

Then create a wrapper so you can call it from anywhere:

```bash
sudo nano /usr/local/bin/bb-coord
```

Paste this in:

```bash
#!/bin/bash
python3 /home/grant/coord_converter.py "$@"
```

Make it executable:

```bash
sudo chmod +x /usr/local/bin/bb-coord
```

Then just type `bb-coord` from anywhere 😄

---

## How to use

### Single coordinate
```bash
bb-coord -t '40 26 46 S, 79 58 56 W'
```
### Batch file
```bash
bb-coord -f /path/to/coords.txt
```
### Help
```bash
bb-coord -h
```

---

## Tips 💡

- Always wrap your input in **single quotes** to avoid shell issues with degree symbols and special characters
- The `.txt` file for batch mode should have one coordinate per line, blank lines are skipped
- S and W are automatically converted to negative — you don't need to do anything

---

## Legal stuff 👀

This tool does math on coordinates. Very dangerous stuff. If anyone asks — especially anyone with a GPS unit and a suspicious look — you found this on the internet and you have no idea who made it. The developer is a ghost. Doesn't exist. Never heard of him.

Stay safe out there 🫡

---

## Credits

Built with love, broken code, and a lot of patience by **amtechguy** 😄

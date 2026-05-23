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

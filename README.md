# bb-coord

A command-line coordinate conversion utility for Linux that normalizes inconsistent geographic coordinate formats into standardized **Decimal Degrees (DD)** directly from your terminal.

---

## Features

- **Automated Format Detection:** Automatically identifies input format without requiring manual configuration or flags.
- **6 Supported Formats:** Converts DMS, DDM, DD with direction, signed DD, MGRS, and UTM into standard Decimal Degrees.
- **Batch Processing:** Processes single coordinates via inline arguments or batch processes entire `.txt` files containing mixed formats.
- **Direction Handling:** Automatically normalizes South and West coordinates to signed negative values.
- **Clean Format Tagging:** Outputs clear format tags (`[DMS]`, `[MGRS]`, `[UTM]`, etc.) alongside normalized coordinates.

---

## Supported Coordinate Formats

| Format | Description | Example Input |
| :--- | :--- | :--- |
| **DMS** | Degrees Minutes Seconds | `40 26 46 S, 79 58 56 W` |
| **DDM** | Degrees Decimal Minutes | `40 26.767 S, 79 58.933 W` |
| **DD (Direction)** | Decimal Degrees with Cardinal | `40.446 S, 79.982 W` |
| **Signed DD** | Standard Signed Decimal Degrees | `-40.446111, -79.982222` |
| **MGRS** | Military Grid Reference System | `17TPE8056816806` |
| **UTM** | Universal Transverse Mercator | `17N 580568 4477606` |

---

## Requirements

- **Operating System:** Linux / macOS / WSL 2
- **Python:** 3.9 or higher
- **Dependencies:** `mgrs`, `pyproj`

---

## Installation

```bash
git clone https://github.com/amtechguy/bb-coord.git
cd bb-coord
pip install -r requirements.txt
chmod +x coord_converter.py
```

To run it globally as `bb-coord`:

```bash
sudo ln -s "$(pwd)/coord_converter.py" /usr/local/bin/bb-coord
```

---

## Usage

### Single Coordinate Conversion
```bash
bb-coord -t '40 26 46 S, 79 58 56 W'
```

### Batch File Conversion
```bash
bb-coord -f path/to/coordinates.txt
```

### View Help & Options
```bash
bb-coord -h
```

---

## License

This project is licensed under the MIT License. Developed by **James Ofori** ([@amtechguy](https://github.com/amtechguy)).

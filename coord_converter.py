#!/usr/bin/env python3
import re
import sys
import argparse

def ensure_dependencies():
    missing = []
    try:
        import mgrs
    except ImportError:
        missing.append("mgrs")
    try:
        import pyproj
    except ImportError:
        missing.append("pyproj")

    if missing:
        print(f"⚙️  Missing dependencies: {', '.join(missing)}. Installing...")
        import subprocess
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "--break-system-packages", *missing
        ])
        print("✅ Dependencies installed. Restarting...\n")
        import os
        os.execv(sys.executable, [sys.executable] + sys.argv)

ensure_dependencies()

import mgrs as mgrs_module
from pyproj import Proj, Transformer

def is_mgrs(s):
    return bool(re.match(r'^\d{1,2}[C-X][A-Z]{2}\d{4,10}$', s.strip(), re.IGNORECASE))

def is_utm(s):
    return bool(re.match(r'^\d{1,2}[A-Z]\s+\d+\s+\d+$', s.strip(), re.IGNORECASE))

def is_signed_dd(s):
    parts = s.split(',')
    if len(parts) == 2:
        try:
            float(parts[0].strip())
            float(parts[1].strip())
            return True
        except ValueError:
            return False
    return False

def is_dd_with_direction(s):
    parts = s.split(',')
    if len(parts) == 2:
        n0 = re.findall(r"[\d\.]+", parts[0])
        n1 = re.findall(r"[\d\.]+", parts[1])
        has_direction = bool(re.search(r'[NSEW]', s, re.IGNORECASE))
        if len(n0) == 1 and len(n1) == 1 and has_direction:
            return True
    return False

def is_ddm(s):
    has_direction = bool(re.search(r'[NSEW]', s, re.IGNORECASE))
    parts = s.split(',')
    if len(parts) == 2:
        n0 = re.findall(r"[\d\.]+", parts[0])
        n1 = re.findall(r"[\d\.]+", parts[1])
        if len(n0) == 2 and len(n1) == 2 and has_direction:
            return True
    return False

def is_dms(s):
    parts = s.split(',')
    if len(parts) == 2:
        n0 = re.findall(r"[\d\.]+", parts[0])
        n1 = re.findall(r"[\d\.]+", parts[1])
        has_direction = bool(re.search(r'[NSEW]', s, re.IGNORECASE))
        if len(n0) == 3 and len(n1) == 3 and has_direction:
            return True
    return False

def convert_mgrs(s):
    import warnings
    try:
        m = mgrs_module.MGRS()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            lat, lon = m.toLatLon(s.strip().encode())
        return round(lat, 6), round(lon, 6), "MGRS"
    except Exception:
        return None, None, "MGRS"

def convert_utm(s):
    try:
        match = re.match(r'(\d{1,2})([A-Z])\s+(\d+)\s+(\d+)', s.strip(), re.IGNORECASE)
        if not match:
            return None, None, "UTM"
        zone_num = int(match.group(1))
        easting = float(match.group(3))
        northing = float(match.group(4))
        zone_letter = match.group(2).upper()
        southern = zone_letter < 'N'
        proj = Proj(proj='utm', zone=zone_num, south=southern, ellps='WGS84')
        transformer = Transformer.from_proj(proj, Proj(proj='latlong', ellps='WGS84'))
        lon, lat = transformer.transform(easting, northing)
        return round(lat, 6), round(lon, 6), "UTM"
    except Exception:
        return None, None, "UTM"

def convert_signed_dd(s):
    parts = s.split(',')
    lat = round(float(parts[0].strip()), 6)
    lon = round(float(parts[1].strip()), 6)
    return lat, lon, "Signed DD"

def convert_dd_with_direction(s):
    parts = s.split(',')
    results = []
    for part in parts:
        num = re.findall(r"[\d\.]+", part)
        direction = re.search(r'[NSEW]', part, re.IGNORECASE)
        if num and direction:
            val = float(num[0])
            if direction.group().upper() in ['S', 'W']:
                val = -val
            results.append(round(val, 6))
    if len(results) == 2:
        return results[0], results[1], "DD"
    return None, None, "DD"

def convert_ddm(s):
    parts = s.split(',')
    results = []
    for part in parts:
        nums = re.findall(r"[\d\.]+", part)
        direction = re.search(r'[NSEW]', part, re.IGNORECASE)
        if len(nums) >= 2 and direction:
            val = float(nums[0]) + float(nums[1]) / 60
            if direction.group().upper() in ['S', 'W']:
                val = -val
            results.append(round(val, 6))
    if len(results) == 2:
        return results[0], results[1], "DDM"
    return None, None, "DDM"

def convert_dms(s):
    parts = s.split(',')
    results = []
    for part in parts:
        nums = re.findall(r"[\d\.]+", part)
        direction = re.search(r'[NSEW]', part, re.IGNORECASE)
        if len(nums) >= 3 and direction:
            val = float(nums[0]) + float(nums[1]) / 60 + float(nums[2]) / 3600
            if direction.group().upper() in ['S', 'W']:
                val = -val
            results.append(round(val, 6))
    if len(results) == 2:
        return results[0], results[1], "DMS"
    return None, None, "DMS"

def convert(line):
    s = line.strip()
    if is_mgrs(s):
        return convert_mgrs(s)
    if is_utm(s):
        return convert_utm(s)
    if is_signed_dd(s):
        return convert_signed_dd(s)
    if is_dd_with_direction(s):
        return convert_dd_with_direction(s)
    if is_ddm(s):
        return convert_ddm(s)
    if is_dms(s):
        return convert_dms(s)
    return None, None, "Unknown"

def main():
    parser = argparse.ArgumentParser(description="Convert any coordinate format to Decimal Degrees (DD)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-t", "--text", type=str, help='Single coordinate in quotes')
    group.add_argument("-f", "--file", type=str, help="Path to a .txt file of coordinates")
    args = parser.parse_args()

    if args.text:
        lat, lon, fmt = convert(args.text)
        if lat is not None:
            print(f"\n✅ [{fmt}] {lat}, {lon}\n")
        else:
            print("⚠️  Could not parse the coordinate. Check the format and try again.")

    elif args.file:
        try:
            with open(args.file, 'r') as f:
                lines = f.readlines()
            print(f"\n📂 Scanning {args.file}...\n")
            print("-" * 45)
            for line_num, line in enumerate(lines, 1):
                clean = line.strip()
                if not clean:
                    continue
                lat, lon, fmt = convert(clean)
                if lat is not None:
                    print(f"Line {line_num}: [{fmt}] {lat}, {lon}")
                else:
                    print(f"Line {line_num}: ⚠️  Could not parse '{clean}'")
            print("-" * 45)
            print("✅ Done.\n")
        except FileNotFoundError:
            print(f"⚠️  File not found: '{args.file}'")

if __name__ == "__main__":
    main()

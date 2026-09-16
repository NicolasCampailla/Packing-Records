#!/usr/bin/env python3
"""
Erich Friedman Record Checker for Polygon Packings
===================================================
Scrapes Erich Friedman's Packing Center website (https://erich-friedman.github.io/packing/)
and compares local polygon packing solutions against the currently published records.

Usage:
    python check_records.py                 # Check all packing folders in current directory
    python check_records.py "To Be Sent"     # Check specific folder or file
    python check_records.py solution.txt    # Check a single solution file
    python check_records.py --markdown      # Output a GitHub-flavored Markdown table
"""

import os
import sys
import re
import argparse
import urllib.request
from typing import Dict, Optional, Tuple, Any

# ==============================================================================
# CONFIGURATION PARAMETERS
# ==============================================================================
AUTHOR_NAME = "Nicolas Campailla"
# ==============================================================================

# Map polygon names / aliases to Friedman 3-letter code and side count
SHAPE_ALIASES = {
    'tri': ('tri', 3, 'triangle'),
    'triangle': ('tri', 3, 'triangle'),
    'triangles': ('tri', 3, 'triangle'),
    'squ': ('squ', 4, 'square'),
    'square': ('squ', 4, 'square'),
    'squares': ('squ', 4, 'square'),
    'a square': ('squ', 4, 'square'),
    'a squares': ('squ', 4, 'square'),
    'pen': ('pen', 5, 'pentagon'),
    'pentagon': ('pen', 5, 'pentagon'),
    'pentagons': ('pen', 5, 'pentagon'),
    'a pentagon': ('pen', 5, 'pentagon'),
    'a pentagons': ('pen', 5, 'pentagon'),
    'hex': ('hex', 6, 'hexagon'),
    'hexagon': ('hex', 6, 'hexagon'),
    'hexagons': ('hex', 6, 'hexagon'),
    'oct': ('oct', 8, 'octagon'),
    'octagon': ('oct', 8, 'octagon'),
    'octagons': ('oct', 8, 'octagon'),
    'an octagon': ('oct', 8, 'octagon'),
    'an octagons': ('oct', 8, 'octagon'),
}

SIDES_TO_CODE = {
    3: 'tri',
    4: 'squ',
    5: 'pen',
    6: 'hex',
    8: 'oct',
}

SIDES_TO_NAME = {
    3: 'triangle',
    4: 'square',
    5: 'pentagon',
    6: 'hexagon',
    8: 'octagon',
}

_page_cache: Dict[str, Dict[int, Dict[str, Any]]] = {}

def parse_cell_data(n: int, cell_content: str, records: Dict[int, Dict[str, Any]]):
    s_matches = re.findall(r's\s*=\s*([^<\n\r]+)', cell_content, re.I)
    decimal_val: Optional[float] = None
    formula: Optional[str] = None

    for sm in s_matches:
        sm_clean = sm.replace('&nbsp;', ' ').strip().rstrip('+')
        try:
            decimal_val = float(sm_clean)
        except ValueError:
            if '/' in sm_clean:
                parts = sm_clean.split('/')
                try:
                    decimal_val = float(parts[0].strip()) / float(parts[1].strip())
                except Exception:
                    formula = sm.strip()
            else:
                formula = sm.strip()

    author = "Unknown"
    m_author = re.search(r'Found by\s+([^<\n\r]+)', cell_content, re.I)
    date = ""
    if m_author:
        author = m_author.group(1).strip()
        m_date = re.search(r'in\s+([A-Za-z]+\s+\d{4})', cell_content, re.I)
        if m_date:
            date = m_date.group(1).strip()
    elif 'Trivial' in cell_content:
        author = 'Trivial'

    if formula:
        formula = formula.replace('&radic;', '√').replace('&ndash;', '–').replace('&nbsp;', ' ').strip()

    records[n] = {
        's': decimal_val,
        'formula': formula,
        'author': author,
        'date': date,
        'raw_cell': cell_content.strip()
    }


def fetch_friedman_records(inner_code: str, outer_code: str) -> Dict[int, Dict[str, Any]]:
    """Fetches and parses a packing page from Friedman's website."""
    key = f"{inner_code}in{outer_code}"
    if key in _page_cache:
        return _page_cache[key]

    url = f"https://erich-friedman.github.io/packing/{key}/"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
    except Exception:
        _page_cache[key] = {}
        return {}

    records: Dict[int, Dict[str, Any]] = {}
    tables = re.findall(r'<TABLE.*?</TABLE>', html, re.I | re.S)

    for table in tables:
        # Check if table has cells that contain both <font size=+3>N. and s =
        cells = re.split(r'<(?:td|TD)[^>]*>', table)[1:]
        has_combined_cells = any(
            re.search(r'<font\s+size=[+]3>(\d+)\.', c, re.I) and ('s =' in c or 's&nbsp;=' in c or 's=' in c)
            for c in cells
        )

        if has_combined_cells:
            for cell in cells:
                m_num = re.search(r'<font\s+size=[+]3>(\d+)\.', cell, re.I)
                if not m_num:
                    continue
                n = int(m_num.group(1))
                parse_cell_data(n, cell, records)
        else:
            rows = re.findall(r'<TR.*?</TR>', table, re.I | re.S)
            if len(rows) >= 2:
                nums = [int(m) for m in re.findall(r'<font\s+size=[+]3>(\d+)\.', rows[0], re.I)]
                desc_cells = re.split(r'<td\s+align=center>', rows[1], flags=re.I)[1:]
                for idx, n in enumerate(nums):
                    if idx < len(desc_cells):
                        parse_cell_data(n, desc_cells[idx], records)

    _page_cache[key] = records
    return records


def parse_solution_file(file_path: str) -> Optional[Dict[str, Any]]:
    """Parses standard [HEADER] from a polygon packing .txt file."""
    if not os.path.isfile(file_path):
        return None

    info = {}
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if '=' in line:
                    k, v = line.split('=', 1)
                    k = k.strip()
                    v = v.strip()
                    if k == 'inner_count':
                        info['n'] = int(v)
                    elif k == 'inner_sides':
                        info['inner_sides'] = int(v)
                    elif k == 'container_sides':
                        info['container_sides'] = int(v)
                    elif k == 'container_side_len':
                        info['s'] = float(v)
    except Exception:
        return None

    if 'n' in info and 'inner_sides' in info and 'container_sides' in info:
        info['file_path'] = file_path
        return info
    return None


def parse_name_from_string(name: str) -> Optional[Tuple[int, int, int]]:
    """Infers (n, inner_sides, container_sides) from folder or file name."""
    m = re.match(r'^(\d+)\s+([a-zA-Z\s]+?)\s+in\s+(?:an?|the)?\s*([a-zA-Z\s]+?)(?:\s+.*|$)', name, re.I)
    if not m:
        return None

    n = int(m.group(1))
    inner_str = m.group(2).strip().lower()
    outer_str = m.group(3).strip().lower()

    inner_info = SHAPE_ALIASES.get(inner_str)
    outer_info = SHAPE_ALIASES.get(outer_str)

    if inner_info and outer_info:
        return n, inner_info[1], outer_info[1]
    return None


def inspect_directory(root_dir: str):
    """Recursively finds all packing folders and solution files."""
    findings = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip internal system or hidden folders (ignore '.' and '..')
        if any(part.startswith('.') and part not in ['.', '..'] or part == '__pycache__' for part in dirpath.split(os.sep)):
            continue

        solution_txts = [
            f for f in filenames
            if f.endswith('.txt') and not any(k in f.lower() for k in ['readme', 'expression', 'latex'])
        ]

        item: Dict[str, Any] = {
            'dirpath': dirpath,
            'relpath': os.path.relpath(dirpath, root_dir),
            'filenames': filenames,
        }

        # Priority 1: Check solution .txt
        parsed = None
        for tf in solution_txts:
            candidate = parse_solution_file(os.path.join(dirpath, tf))
            if candidate and 's' in candidate:
                parsed = candidate
                break

        if parsed:
            item.update(parsed)
            findings.append(item)
            continue

        # Priority 2: Infer from folder name
        inferred = parse_name_from_string(os.path.basename(dirpath))
        if inferred:
            item['n'], item['inner_sides'], item['container_sides'] = inferred
            item['s'] = None
            findings.append(item)

    return findings


def matches_target_author(live_author: str, target_author: str) -> bool:
    """Checks if the live author string matches the specified target author."""
    if not live_author or not target_author:
        return False
    if target_author.lower() in live_author.lower():
        return True
    # Match any distinctive token of the target author (first/last name)
    parts = [p.lower() for p in re.split(r'[\s,]+', target_author) if len(p) > 2]
    return any(p in live_author.lower() for p in parts)


def compare_item(item: Dict[str, Any], target_author: str = AUTHOR_NAME) -> Dict[str, Any]:
    """Compares a local packing item against Friedman's live website."""
    n = item.get('n')
    i_sides = item.get('inner_sides')
    c_sides = item.get('container_sides')
    local_s = item.get('s')

    i_code = SIDES_TO_CODE.get(i_sides)
    c_code = SIDES_TO_CODE.get(c_sides)

    result = {
        'item': item,
        'inner_name': SIDES_TO_NAME.get(i_sides, '?'),
        'outer_name': SIDES_TO_NAME.get(c_sides, '?'),
        'n': n,
        'local_s': local_s,
        'live_s': None,
        'live_author': "Unknown",
        'live_date': "",
        'live_formula': None,
        'status': "Unknown",
        'status_code': "UNKNOWN",
    }

    if not (i_code and c_code and n):
        result['status'] = "Cannot determine polygon geometry"
        return result

    records = fetch_friedman_records(i_code, c_code)
    live = records.get(n)

    if not live:
        result['status'] = "NOT ON SITE (Unpublished size)"
        result['status_code'] = "NOT_ON_SITE"
        return result

    live_s = live['s']
    live_author = live['author']
    result['live_s'] = live_s
    result['live_author'] = live_author
    result['live_date'] = live['date']
    result['live_formula'] = live['formula']

    is_user = matches_target_author(live_author, target_author)

    if local_s is not None and live_s is not None:
        diff = local_s - live_s
        if abs(diff) < 1e-4:
            if is_user:
                result['status'] = f"ACTIVE RECORD ({target_author} on site: {live_s})"
                result['status_code'] = "RECORD"
            else:
                result['status'] = f"TIED RECORD ({live_author}: {live_s})"
                result['status_code'] = "TIED"
        elif local_s < live_s - 1e-4:
            improvement = live_s - local_s
            result['status'] = f"NEW RECORD! Beats site by {improvement:.5f} (Site: {live_s} by {live_author})"
            result['status_code'] = "NEW_RECORD"
        else:
            if is_user:
                result['status'] = f"RECORD HELD (Local {local_s:.5f} vs Site {live_s:.5f})"
                result['status_code'] = "RECORD"
            else:
                diff_worse = local_s - live_s
                result['status'] = f"BEATEN / SUBOPTIMAL (Site is better by {diff_worse:.5f} by {live_author})"
                result['status_code'] = "BEATEN"
    else:
        if is_user:
            result['status'] = f"ACTIVE RECORD ({target_author} on site: {live_s})"
            result['status_code'] = "RECORD"
        else:
            result['status'] = f"Site: {live_s} by {live_author}"
            result['status_code'] = "SITE_OTHER"

    return result


def main():
    parser = argparse.ArgumentParser(description="Check polygon packing records against Erich Friedman's website")
    parser.add_argument("target", nargs="?", default=".", help="Directory or file to check (default: current directory)")
    parser.add_argument("--author", default=AUTHOR_NAME, help=f"Author name to verify records for (default: '{AUTHOR_NAME}')")
    parser.add_argument("--markdown", action="store_true", help="Print summary as Markdown table")
    args = parser.parse_args()

    target = args.target
    author = args.author

    if os.path.isfile(target):
        parsed = parse_solution_file(target)
        if not parsed:
            # try inferring from filename
            inferred = parse_name_from_string(os.path.basename(target))
            if inferred:
                n, isides, csides = inferred
                parsed = {'n': n, 'inner_sides': isides, 'container_sides': csides, 's': None, 'file_path': target}

        if not parsed:
            print(f"Error: Could not parse solution metadata from {target}")
            sys.exit(1)

        res = compare_item(parsed, target_author=author)
        print(f"\n--- Checking: {target} (Target Author: {author}) ---")
        print(f"Packing: {res['n']} {res['inner_name']} in {res['outer_name']}")
        print(f"Local side: {res['local_s']}")
        print(f"Live side:  {res['live_s']} (Author: {res['live_author']} {res['live_date']})")
        if res['live_formula']:
            print(f"Formula:    {res['live_formula']}")
        print(f"Status:     {res['status']}\n")
        return

    # Target is a directory
    findings = inspect_directory(target)
    if not findings:
        print(f"No packing solutions found in {target}.")
        return

    results = [compare_item(item, target_author=author) for item in findings]
    results.sort(key=lambda x: x['item']['relpath'])

    if args.markdown:
        print("# Erich Friedman Packing Center Record Check\n")
        print("| Category / Folder | Packing | Local Side | Live Side | Live Record Holder | Status |")
        print("| :--- | :--- | :---: | :---: | :--- | :--- |")
        for r in results:
            rel = r['item']['relpath']
            packing = f"{r['n']} {r['inner_name']} in {r['outer_name']}"
            loc = f"{r['local_s']:.5f}" if r['local_s'] is not None else "—"
            liv = f"{r['live_s']:.5f}" if r['live_s'] is not None else "—"
            holder = f"{r['live_author']} ({r['live_date']})" if r['live_date'] else r['live_author']
            print(f"| `{rel}` | {packing} | {loc} | {liv} | {holder} | **{r['status_code']}** |")
        return

    # Console table output
    print(f"\nChecked {len(results)} packing solutions against Erich Friedman's live website:\n")
    print(f"{'Folder / Path':<42} | {'Packing':<22} | {'Local s':<9} | {'Live s':<9} | {'Author':<20} | Status")
    print("-" * 135)

    for r in results:
        rel = r['item']['relpath']
        if len(rel) > 42:
            rel = "..." + rel[-39:]
        packing = f"{r['n']} {r['inner_name']} in {r['outer_name']}"
        loc = f"{r['local_s']:.5f}" if r['local_s'] is not None else "—"
        liv = f"{r['live_s']:.5f}" if r['live_s'] is not None else "—"
        auth = r['live_author'][:19]
        status = r['status']

        print(f"{rel:<42} | {packing:<22} | {loc:<9} | {liv:<9} | {auth:<20} | {status}")

    print("\nCheck complete.\n")


if __name__ == '__main__':
    main()

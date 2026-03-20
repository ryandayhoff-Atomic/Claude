#!/usr/bin/env python3
"""Track which files still need to be downloaded."""
import csv
import os

BUDGET_DIR = '/home/user/Claude/2026_Budgets'

# Read the master file list
files = []
with open(os.path.join(BUDGET_DIR, 'all_2026_budget_files.csv'), 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        files.append(row)

# Check which xlsx files already exist
existing = set()
for fname in os.listdir(BUDGET_DIR):
    if fname.endswith('.xlsx'):
        existing.add(fname)

# Find files that still need to be downloaded
remaining = []
for f in files:
    name = f['File Name']
    xlsx_name = f"{name}.xlsx"
    if xlsx_name not in existing:
        remaining.append(f)
    else:
        print(f"  EXISTS: {xlsx_name}")

print(f"\n--- {len(existing)} files already downloaded, {len(remaining)} remaining ---\n")
for r in remaining:
    print(f"  NEED: {r['File Name']} | ID: {r['Google Drive ID']}")

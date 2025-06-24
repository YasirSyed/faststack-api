import sys
import os
import re
import pandas as pd

MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'app', 'models')
TIMESTAMP_PATTERNS = [
    r'(\s*created_at\s*=\s*Column\(.*)server_default=func.now\(\)(.*)\)',
    r'(\s*updated_at\s*=\s*Column\(.*)onupdate=func.now\(\)(.*)\)'
]

COMMENT_PREFIX = '# AUTOTOGGLE# '


def toggle_autopopulation(mode: str):
    assert mode in {'off', 'on'}, "Mode must be 'off' or 'on'"
    for fname in os.listdir(MODELS_DIR):
        if not fname.endswith('.py'):
            continue
        fpath = os.path.join(MODELS_DIR, fname)
        with open(fpath, 'r') as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            if mode == 'off':
                # Comment out autopopulation lines
                for pat in TIMESTAMP_PATTERNS:
                    if re.search(pat, line):
                        if not line.lstrip().startswith(COMMENT_PREFIX):
                            line = COMMENT_PREFIX + line
                new_lines.append(line)
            else:
                # Uncomment lines
                if line.lstrip().startswith(COMMENT_PREFIX):
                    line = line.replace(COMMENT_PREFIX, '', 1)
                new_lines.append(line)
        with open(fpath, 'w') as f:
            f.writelines(new_lines)
    print(f"Timestamp autopopulation toggled: {mode}")

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in {'off', 'on'}:
        print("Usage: python scripts/toggle_timestamp_autopop.py [off|on]")
        sys.exit(1)
    toggle_autopopulation(sys.argv[1]) 
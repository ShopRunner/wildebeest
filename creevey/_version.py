from pathlib import Path
import re

CHANGELOG_PATH = Path(__file__).parents[1].resolve() / 'CHANGELOG.md'

with open(CHANGELOG_PATH, 'r') as f:
    changelog = f.read()

__version__ = re.search(r'\[(\d+\.\d+\.\d+)\]', changelog).group(1)

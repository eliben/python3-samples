# Demonstrates common path manipulation tasks
from pathlib import Path
import sys

if len(sys.argv) < 2:
    print('Usage: {} <file name>'.format(sys.argv[0]))
    sys.exit(1)

inputpath = Path(sys.argv[1])

# Just the filename without the suffix and parent path
stem = inputpath.stem

# Replace <...>/foo.<suffix> with <...>/foo/foo.x
newpath = Path(inputpath.parent, stem, stem + '.x')

print(newpath)

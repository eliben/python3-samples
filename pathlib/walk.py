# Shows how to recursively glob for files and access various parts of a Path
from pathlib import Path
import os

# Recursively 'glob' all .py files under the current directory
for pyfile in Path('.').rglob('*.py'):
    print('--', pyfile)
    print('Name [final path component]:', pyfile.name)
    print('Stem and suffix:', pyfile.stem, ':', pyfile.suffix)
    print('Parent:', pyfile.parent)
    print('Absolute path [resolved]:', pyfile.resolve())


#!/bin/sh

cd "$(dirname "$0")"

rm -rf dist/

python3 setup.py check
python3 setup.py register
python3 setup.py sdist upload
python3 setup.py sdist --formats=zip upload

exit 0

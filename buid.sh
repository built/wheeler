#!/bin/bash
# Create a clean version for distribution.
mkdir -p snapshot
cp -R category snapshot
cp -R interpreter snapshot
cp common.py snapshot
cp wheeler.py snapshot
cp wheeler snapshot
cp bigwheel.py snapshot
cp bigwheel snapshot

tar czf `date "+snapshot_%H%M%S_%m_%d_%y"`.tgz snapshot

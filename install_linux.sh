#!/usr/bin/env bash

set -e  # makes the script fail as soon as one command fails

tlmgr install truncate
tlmgr install tocloft
tlmgr install wallpaper
tlmgr install morefloats
tlmgr install sectsty
tlmgr install siunitx
tlmgr install threeparttable
tlmgr update l3packages
tlmgr update l3kernel
tlmgr update l3experimental
tlmgr update l3backend
# Would it be simpler to just update all packages? (takes ~10m)
# sudo tlmgr update --all
pip install pandoc-fignos pandoc-eqnos pandoc-tablenos pandoc-secnos pandoc-shortcaption

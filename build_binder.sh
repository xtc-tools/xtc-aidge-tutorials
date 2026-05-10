#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0$")"

tmpdir=tmp.docker_build
rm -rf $tmpdir
mkdir -p $tmpdir
mkdir -p $tmpdir/.binder $tmpdir/tutorials
cp -a .binder/requirements.txt $tmpdir/.binder
cp -a .binder/entrypoint.sh $tmpdir/.binder/
cp -a tutorials/*.py  tutorials/*.ipynb tutorials/*.md $tmpdir/tutorials

docker build -f .binder/Dockerfile -t xtc-aidge-tutorial-cpsiot $tmpdir

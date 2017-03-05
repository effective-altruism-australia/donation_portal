#!/usr/bin/env bash
if [[ $# == 1 ]]
then
   pip install $1
   rootdir=$(git rev-parse --show-toplevel)
   echo $1 >> "$rootdir/deps/pip.base"
   pip freeze | grep $1 >> "$rootdir/deps/pip"
fi

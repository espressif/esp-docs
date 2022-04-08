#!/usr/bin/env bash
set -e

for dir in ./*/
do
    echo "Running build.sh from ${dir}"
    cd ${dir}
    ./build.sh
    cd ..
done
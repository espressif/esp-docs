#!/usr/bin/env bash

# sets up the repo incl submodules with specified version as $1
set -o errexit # Exit if command failed.

if [ -z $2 ] || [ -z $ESP_DOCS_PATH ] || [ -z $1 ] ; then
    echo "Mandatory variables undefined"
    exit 1;
fi;

echo "Checking out repo version $1"
cd $2
# Cleans out the untracked files in the repo, so the next "git checkout" doesn't fail
git clean -f
git checkout $1
# Removes the esp-docs submodule, so the next submodule update doesn't fail
rm -rf $2/docs/esp-docs
git submodule update --init --recursive


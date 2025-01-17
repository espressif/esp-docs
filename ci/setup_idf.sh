#!/usr/bin/env bash

# $1: repo url
# $2: commit id
# $3: IDF_PATH
# $4: toolchain target

# sets up the repo incl submodules
set -o errexit # Exit if command failed.

if [ -z $2 ] || [ -z $1 ]  || [ -z $3 ] || [ -z $4 ] ; then
    echo "Mandatory variables undefined"
    exit 1;
fi;

# sets up the repo incl submodules with specified version as $2
echo "Checking out repo $1 with commit $2"
mkdir $3 && cd $3
git init
git remote add origin $1
git fetch --depth 1 origin $2
git checkout FETCH_HEAD

git submodule init
git submodule update --depth 1

#!/bin/sh

if [ ! -d resources ]; then
    echo 'Create resources directory'
    mkdir resources
fi

if [ ! -d resources/wordnet-1.6 ]; then
    echo "Download WordNet-1.6"
    wget http://wordnetcode.princeton.edu/1.6/wn16.unix.tar.gz -O wn16.unix.tar.gz
    tar -xzf wn16.unix.tar.gz
    mv wordnet-1.6 resources/
    rm wn16.unix.tar.gz
fi

if [ ! -d resources/WordNet-3.0 ]; then
    echo "Download WordNet-3.0"
    wget http://wordnetcode.princeton.edu/3.0/WordNet-3.0.tar.gz -O WordNet-3.0.tar.gz
    tar -xzf WordNet-3.0.tar.gz
    mv WordNet-3.0 resources/
    rm WordNet-3.0.tar.gz
fi

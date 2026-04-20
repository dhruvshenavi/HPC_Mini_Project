#!/usr/bin/env bash

apt-get update
apt-get install -y g++

g++ -fopenmp -shared -fPIC parallel.cpp -o libparallel.so

pip install -r requirements.txt
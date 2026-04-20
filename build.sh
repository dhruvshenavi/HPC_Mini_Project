#!/usr/bin/env bash

# compile C++ (g++ is already available on Render)
g++ -fopenmp -shared -fPIC parallel.cpp -o libparallel.so

# install python dependencies
pip install -r requirements.txt
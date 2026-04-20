#!/usr/bin/env bash

# compile C++ (g++ is already available on Render)
echo "Compiling C++..."
g++ -fopenmp -shared -fPIC parallel.cpp -o libparallel.so
echo "Done compiling"

# install python dependencies
pip install -r requirements.txt
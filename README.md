# triangles-segga
This repository contains python code to extract triangle-based cell shape anisotropy (see [this publication](https://doi.org/10.1103/PhysRevE.95.032401) for details) from biological image data segmented using [SEGGA](http://dx.doi.org/10.1242/dev.146837).

This code was developed for the research published in:
**[Anisotropy links cell shapes to a solid-to-fluid transition during convergent extension.](http://dx.doi.org/10.1101/781492)** Xun Wang, Matthias Merkel, Leo B. Sutter, Gonca Erdemci-Tandogan, M. Lisa Manning, Karen E. Kasza. *bioRxiv*, doi: 10.1101/781492 (2019).

## Requirements
- a working installation of python
- the following python packages:
    - numpy
    - scipy
    - PyQt4 - used for drawing only and not absolutely necessary (to get rid of this dependency, just remove any imports of `Drawing.py` and `NetworkDrawing.py` from `extractAverageQ.py`)
    
## Structure and usage
- This package contains a collection of data structures and routines to extract and display the cellular structure from SEGGA-segmented data, as well as compute a triangle-based cell shape tensor.
- One way to use this code is to start from `extractAverageQ.py` and adapt it to your needs.
- It contains the following python files:
    - `Geometry/` folder containing routines to carry out geometric computations:
        - `Point.py`  definition of a point
        - `Nematic.py`  definition of a "nematic" (i.e. a symmetric, traceless tensor in 2D)
        - `Triangle.py`  definition of a triangle and computation of triangle properties
    - `Network.py`  definition of the cell network structure `Network` and conversion into a list of triangles
    - `Segga.py`  loading of a SEGGA `.mat` file and translation into a `Network` structure
    - `Drawing.py`  general routines to draw into a pdf file based on PyQt4
    - `NetworkDrawing.py`  drawing routines for `Network` cells and triangles using the routines in `Drawing.py`
    - `extractAverageQ.py`  example file reading a number of SEGGA `.mat` files, translating them into `Network`s, extracting the triangles, computing the average Q tensor, and drawing cell networks, triangles, and Q tensors on the original images

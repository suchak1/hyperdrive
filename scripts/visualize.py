import sys
sys.path.append('hyperdrive')
from FileOps import FileReader  # noqa
from Precognition import Oracle  # noqa

# calc = Calculator()
oracle = Oracle()
# reader = FileReader()


X = oracle.load_model_pickle('X')
y = oracle.load_model_pickle('y')

# on line 43 of preds_v2.py
# finish translating
# and then get 2d and 3d correct from visualize_plotly.ipynb
# make 2d square?
# use contour for 2d?
# have options for rect prism, cube, sphere, icosphere, or octahedron as param for 3d
# have option for go.Volume / Isosurface vs small points (from notebook) - may be js
# have param for refinement / num of points in linspace

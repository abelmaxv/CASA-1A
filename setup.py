from setuptools import setup,Extension
from Cython.Build import cythonize
import numpy as np

numpy_path = np.get_include()

extensions = [
    Extension("_graph",["src/_graph.pyx"], 
              include_dirs=[numpy_path]),

    Extension("_union_find", ["src/_union_find.pyx"],
              include_dirs=[numpy_path]),

    Extension("_tree", ["src/_tree.pyx"],
              include_dirs=[numpy_path]),

    Extension("_percolation", ["percolation/_percolation.pyx"],
              include_dirs=[numpy_path],
              depends= ["src/_union_find.pyx", "src/_tree.pyx", "src/_graph.pyx"])
]

setup(
    ext_modules = cythonize(extensions)
)
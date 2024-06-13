from setuptools import setup,Extension
from Cython.Build import cythonize
import numpy as np

numpy_path = np.get_include()

extensions = [
    Extension("_graph",["_graph.pyx"], 
              include_dirs=[numpy_path]),
    Extension("_union_find", ["_union_find.pyx"],
              include_dirs=[numpy_path])
]

setup(
    ext_modules = cythonize(extensions)
)
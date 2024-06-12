from setuptools import setup,Extension
from Cython.Build import cythonize
import numpy as np

extensions = [Extension("_graph",["_graph.pyx"], include_dirs=[np.get_include()])]

setup(
    ext_modules = cythonize(extensions)
)
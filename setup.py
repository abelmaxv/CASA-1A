from setuptools import find_packages, setup,Extension
from Cython.Build import cythonize
import numpy as np

numpy_path = np.get_include()

with open("README.md", "r") as f:
    long_description = f.read()


extensions = [
    Extension("NetHDBSCAN.structures._graph",["NetHDBSCAN/structures/_graph.pyx"], 
              include_dirs=[numpy_path]),

    Extension("NetHDBSCAN.structures._union_find", ["NetHDBSCAN/structures/_union_find.pyx"],
              include_dirs=[numpy_path]),

    Extension("NetHDBSCAN.structures._tree", ["NetHDBSCAN/structures/_tree.pyx"],
              include_dirs=[numpy_path], 
              depends=["NetHDBSCAN/structures/_union_find.pyx"]),

    Extension("NetHDBSCAN.percolation._percolation", ["NetHDBSCAN/percolation/_percolation.pyx"],
              include_dirs=[numpy_path],
              depends= ["NetHDBSCAN/structures/_union_find.pyx", "NetHDBSCAN/structures/_tree.pyx", "NetHDBSCAN/structures/_graph.pyx"])

]

setup(
    ext_modules = cythonize(extensions)
) 
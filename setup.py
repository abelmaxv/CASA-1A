from setuptools import find_packages, setup,Extension
from Cython.Build import cythonize
import numpy as np

numpy_path = np.get_include()

with open("README.md", "r") as f:
    long_description = f.read()


extensions = [
    Extension("NetHDBSCAN.structures._graph",["NetHDBSCAN/structures/_graph"], 
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
    name = "NetHDBSCAN",
    version = "0.0.1",
    description="A graph clustering algorithm inspired by HDBSCAN",
    #package_dir={"":},
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/abelmaxv/CASA-1A",
    author = "Abel Verley",
    author_email = "abel.verley@ens-paris-saclay.fr",
    #install_requires = [],
    ext_modules = cythonize(extensions)
) 
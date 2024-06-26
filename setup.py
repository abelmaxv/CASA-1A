from setuptools import find_packages, setup,Extension
from Cython.Build import cythonize
import numpy as np

numpy_path = np.get_include()

with open("README.md", "r") as f:
    long_description = f.read()


extensions = [
    Extension("src._graph",["src/_graph.pyx"], 
              include_dirs=[numpy_path]),

    Extension("src._union_find", ["src/_union_find.pyx"],
              include_dirs=[numpy_path]),

    Extension("src._tree", ["src/_tree.pyx"],
              include_dirs=[numpy_path], 
              depends=["src/_union_find.pyx"]),

    Extension("percolation._percolation", ["percolation/_percolation.pyx"],
              include_dirs=[numpy_path],
              depends= ["src/_union_find.pyx", "src/_tree.pyx", "src/_graph.pyx"])

]

setup(
    name = "intership_clusterer_project",
    #version = "O.O.10",
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
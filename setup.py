from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(
		"cuckoovec.pyx",
		sources=["libcuckoo/src/cuckoohash_map.hh"],
		language="c++")
)
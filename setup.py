from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    ext_modules = [Extension('cuckoovec',
		sources=["libcuckoo.pyx"],
		language="c++",
		extra_compile_args=["-std=c++11"]
	)],
	cmdclass = {'build_ext': build_ext}
)
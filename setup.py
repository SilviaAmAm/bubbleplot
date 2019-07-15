from numpy.distutils.core import Extension, setup

__author__ = "Silvia Amabilino"
__copyright__ = "Copyright 2019"
__credits__ = ["University of Bristol"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Silvia Amabilino"
__email__ = "walfits@gmail.com"
__status__ = "Beta"
__description__ = "Bubble Charts"
__url__ = "https://github.com/SilviaAmAm/bubbleplot"

FORTRAN = "f90"

ext_foptimise_module = Extension(name = 'foptimise',
                          sources = ['bubbleplot/foptimise.f90'],
                          language = FORTRAN,
                          f2py_options=['--quiet'])

setup(name='bubbleplot',
        version=__version__,
        description=__description__,
        author=__author__,
        author_email=__email__,
        url=__url__,
        packages=['bubbleplot'],
        ext_package = 'bubbleplot',
        ext_modules=[ext_foptimise_module]
     )
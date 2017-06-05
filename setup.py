import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyand",
    version = "0.9.1.2",
    author = "ardevd",
    author_email = "no-reply@unknown.com",
    description = ("Python wrapper for ADB and Fastboot"),
    license = "MIT",
    keywords = "python android adb fastboot",
    url = "https://github.com/ardevd/pyand",
    packages=['pyand'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Programming Language :: Python",
    ],
)

import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyand",
    version = "0.9.1.2",
    author = "Edvard Holst",
    author_email = "edvard.holst@gmail.com",
    description = ("Python wrapper for ADB and Fastboot"),
    license = "MIT",
    keywords = "python android adb fastboot",
    url = "https://github.com/Zyg0te/pyand",
    packages=['pyand'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Programming Language :: Python",
    ],
)

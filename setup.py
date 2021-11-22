"Parametrize and run PWM on an Arduino using a serial connection."
import os
from setuptools import setup


def read(fname):
    "Read a file in the current directory."
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pypwm",
    version="0.2",
    author="Romain Fayat",
    author_email="r.fayat@gmail.com",
    description=__doc__,
    install_requires=["pyserial", "toml"],
    packages=["pypwm"],
    long_description=read('README.md'),
)

#!/usr/bin/env python

import sys
import os
import subprocess
import shutil

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup
from distutils.cmd import Command
from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError
from distutils.core import Extension

requirements = []
try:
    import xml.etree.ElementTree
except ImportError:
    requirements.append("elementtree")

version = "0.9.3"

f = open("README.rst")
try:
    try:
        readme_content = f.read()
    except:
        readme_content = ""
finally:
    f.close()

class GenerateDoc(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        path = "doc/%s" % version

        shutil.rmtree(path, ignore_errors=True)
        os.makedirs(path)

        subprocess.call(["epydoc", "--config", "epydoc-config", "-o", path])

class custom_build_ext(build_ext):
    """Allow C extension building to fail.

    The C extension speeds up BSON encoding, but is not essential.
    """
    def build_extension(self, ext):
        if sys.version_info[:3] >= (2, 4, 0):
            try:
                build_ext.build_extension(self, ext)
            except CCompilerError:
                print ""
                print ("*" * 62)
                print """WARNING: The %s extension module could not
be compiled. No C extensions are essential for PyMongo to run,
although they do result in significant speed improvements.

Above is the ouput showing how the compilation failed.""" % ext.name
                print ("*" * 62 + "\n")
        else:
            print ""
            print ("*" * 62)
            print """WARNING: The %s extension module is not supported
for this version of Python. No C extensions are essential
for PyMongo to run, although they do result in significant
speed improvements.

Please use Python >= 2.4 to take advantage of the extension.""" % ext.name
            print ("*" * 62 + "\n")

setup(
    name="pymongo",
    version=version,
    description="Driver for the Mongo database <http://www.mongodb.org>",
    long_description=readme_content,
    author="10gen",
    author_email="mongodb-user@googlegroups.com",
    url="http://github.com/mongodb/mongo-python-driver",
    packages=["pymongo", "gridfs"],
    ext_modules=[Extension('pymongo._cbson', ['pymongo/_cbsonmodule.c'])],
    install_requires=requirements,
    license="Apache License, Version 2.0",
    test_suite="nose.collector",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Database"],
    cmdclass={"build_ext": custom_build_ext,
              "doc": GenerateDoc})

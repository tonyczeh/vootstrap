import sys

from setuptools import setup

from vootstrap import __version__


long_description = """
vootstrap
=========

A tool for creating virtualenv bootstrap scripts.

0.9
---

* Initial release
"""

setup(
    author="Tony Czeh",
    author_email="tony.czeh@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
    ],
    description="A tool for creating virtualenv bootstrap scripts.",
    entry_points={
        "console_scripts": [
            "vootstrap=vootstrap:main",
            "vootstrap-%s=vootstrap:main" % sys.version[:3],
        ]
    },
    keywords="virtualenv bootstrap",
    license="MIT",
    long_description=long_description,
    name="vootstrap",
    packages=["vootstrap", "vootstrap.lib", ],
    url="http://github.com/tonyczeh/vootstrap",
    version=__version__,
    zip_safe=False,
)


from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='py-ip-command',
    version='0.0.4',
    url='https://github.com/Corvan/py-ip-command',
    license='LGPL v. 3.0',
    author='Lars Liedtke',
    author_email='LarsLiedtke@gmx.de',
    description='A wrapper around the linux `ip` command',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
            "Operating System :: POSIX :: Linux",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Utilities"
        ]
)

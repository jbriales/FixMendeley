# coding=utf-8
from distutils.core import setup

import fixmendeley

setup(
    name='FixMendeley',
    version=fixmendeley.__version__,
    description=fixmendeley.__doc__.strip(),
    long_description=open('README.txt').read(),
    url='https://github.com/jbriales/fixmendeley',
    license=fixmendeley.__license__,
    author=fixmendeley.__author__,
    author_email='jesusbriales@gmail.com',
    packages=['fixmendeley',],
)

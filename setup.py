#!/usr/bin/env python2.7
from __future__ import absolute_import, division, print_function
from setuptools import setup
from utool import util_setup

INSTALL_REQUIRES = [
    'matplotlib >= 1.3.1',
]


if __name__ == '__main__':
    kwargs = util_setup.setuptools_setup(
        name='plottool',
        version=util_setup.parse_package_for_version('plottool'),
        licence=util_setup.read_license('LICENSE'),
        long_description=util_setup.parse_readme('README.md'),
        description=('Plottool - tools matplotlib computer vision plots'),
        url='https://github.com/Erotemic/plottool',
        keywords='',
        package_data={},
        classifiers=[],
        author='Jon Crall',
        author_email='erotemic@gmail.com',
        setup_fpath=__file__,
    )
    setup(**kwargs)

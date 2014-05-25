#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

INSTALL_REQUIRES = [
    'matplotlib >= 1.3.1',
]

if __name__ == '__main__':
    from utool.util_setup import setuptools_setup
    setuptools_setup(
        name='plottool',
        description=('Plottool - tools matplotlib computer vision plots'),
        url='https://github.com/Erotemic/plottool',
        keywords='',
        package_data={},
        classifiers=[],
        author='Jon Crall',
        author_email='erotemic@gmail.com',
        setup_fpath=__file__,
    )

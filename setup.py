# -*- coding: utf-8 -*-
"""
This module contains the tool of hostout.plone
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1'

long_description = (
    read('README.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('hostout', 'plone', 'plone', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
   'Download\n'
    '********\n')


tests_require = ['zope.testing', 'zc.buildout']

setup(name='hostout.plone',
      version=version,
      description="Fabric scripts for specific plone tasks",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Zope Public License',
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['hostout',],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout'
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='hostout.plone.tests.test_docs.test_suite',
    entry_points = {'zc.buildout':['default = hostout.plone:Recipe'],
                    'fabric': ['fabfile = hostout.plone.fabfile']
                    },
      )

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from setuptools import setup


install_requires = [
    'construct==0.0.4',
    'construct_cli==0.0.2',
    'construct_launcher==0.0.1',
    'construct_maya==0.0.1',
    'construct_nuke==0.0.1',
    'construct_templates==0.0.1',
    'fsfs==0.1.4',
]

dependency_links = [
    'git+ssh://git@github.com/construct-org/construct.git@master#egg=construct-0.0.4',
    'git+ssh://git@github.com/construct-org/construct_cli.git@master#egg=construct_cli-0.0.2',
    'git+ssh://git@github.com/construct-org/construct_cpenv.git@master#egg=construct_cpenv-0.0.1',
    'git+ssh://git@github.com/construct-org/construct_launcher.git@master#egg=construct_launcher-0.0.1',
    'git+ssh://git@github.com/construct-org/construct_maya.git@master#egg=construct_maya-0.0.1',
    'git+ssh://git@github.com/construct-org/construct_nuke.git@master#egg=construct_nuke-0.0.1',
    'git+ssh://git@github.com/construct-org/construct_templates.git@master#egg=construct_templates-0.0.1',
    'git+ssh://git@github.com/danbradham/fsfs.git@master#egg=fsfs-0.1.4'
]

with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name='construct_setup',
    version='0.0.1',
    author='Dan Bradham',
    author_email='danielbradham@gmail.com',
    description='Install construct core packages',
    url='https://github.com/construct-org/construct_setup',
    long_description=readme,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=install_requires,
    dependency_links=dependency_links
)

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from setuptools import setup


dependencies = dict(
    construct='0.0.4',
    construct_cli='0.0.2',
    construct_launcher='0.0.1',
    construct_maya='0.0.1',
    construct_templates='0.0.1'
)

req = '{0}=={1}'
lnk = 'git+ssh://git@github.com/construct-org/{0}.git@master#egg={0}-{1}'
install_requires = [req.format(*dep) for dep in dependencies.items()]
dependency_links = [lnk.format(*dep) for dep in dependencies.items()]


setup(
    name='construct',
    version='0.0.1',
    author='Dan Bradham',
    author_email='danielbradham@gmail.com',
    description='Install Construct',
    url='https://github.com/construct-org/construct_setup',
    long_description='Install construct core packages',
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

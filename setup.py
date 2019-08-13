
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from setuptools import setup


class Dependencies(object):

    def __init__(self):
        self.install_requires = []
        self.dependency_links = []

    def __call__(self, requirement):
        self.install_requires.append(requirement)

    def git(self, org, package, version, branch='master'):
        repo = (
            'git+git://github.com/'
            '{org}/{package}.git@{version}#egg={package}-{version}'
        ).format(**locals())
        require = '{package} @ {repo}'.format(**locals())
        self.install_requires.append(require)


requires = Dependencies()
requires.git('construct-org', 'construct', '0.1.24')
requires.git('construct-org', 'construct_cpenv', '0.1.1')
requires.git('construct-org', 'construct_launcher', '0.1.5')
requires.git('construct-org', 'construct_maya', '0.1.11')
requires.git('construct-org', 'construct_hou', '0.1.1')
requires.git('construct-org', 'construct_nuke', '0.1.9')
requires.git('construct-org', 'construct_ui', '0.1.9')
requires('fsfs==0.2.6')


setup(
    name='construct_setup',
    version='0.1.24',
    author='Dan Bradham',
    author_email='danielbradham@gmail.com',
    description='Install construct core packages',
    url='https://github.com/construct-org/construct_setup',
    long_description=open('README.rst', 'r').read(),
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
    install_requires=requires.install_requires,
)

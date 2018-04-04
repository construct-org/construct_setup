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
        link = (
            'git+ssh://git@github.com/'
            '{org}/{package}.git@{branch}#egg={package}-{version}'
        ).format(**locals())
        require = '{package}=={version}'.format(**locals())
        self.dependency_links.append(link)
        self.install_requires.append(require)


requires = Dependencies()
requires.git('construct-org', 'construct', '0.1.5')
requires.git('construct-org', 'construct_cpenv', '0.1.1')
requires.git('construct-org', 'construct_launcher', '0.1.1')
requires.git('construct-org', 'construct_maya', '0.1.1')
requires.git('construct-org', 'construct_nuke', '0.1.1')
requires.git('danbradham', 'fsfs', '0.1.9')


setup(
    name='construct_setup',
    version='0.1.5',
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
    dependency_links=requires.dependency_links
)

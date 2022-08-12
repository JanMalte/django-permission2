# coding=utf-8
from setuptools import setup, find_packages

NAME = 'django-permission2'
VERSION = '2.0.0b0'


def read(filename):
    import os
    BASE_DIR = os.path.dirname(__file__)
    filename = os.path.join(BASE_DIR, filename)
    with open(filename, 'r') as fi:
        return fi.read()


def readlist(filename):
    rows = read(filename).split("\n")
    rows = [x.strip() for x in rows if x.strip()]
    return rows


setup(
    name=NAME,
    version=VERSION,
    description=('A simple permission system which enable logical permission'
                 'systems to complex permissions'),
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='django object logical permission auth authentication',
    author='Malte Gerth',
    author_email='mail@malte-gerth.de',
    url='https://github.com/janmalte/%s' % NAME,
    download_url='https://github.com/janmalte/%s/tarball/master' % NAME,
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        '': ['README.rst',
             'requirements.txt',
             'requirements-test.txt',
             'requirements-docs.txt'],
    },
    zip_safe=True,
    install_requires=readlist('requirements.txt'),
)

# coding=utf-8
from pathlib import Path

from setuptools import setup, find_packages

NAME = 'django-permission2'

BASE_DIR = Path(__file__).parent
README = (BASE_DIR / "README.rst").read_text()


setup(
    name=NAME,
    description=('A simple permission system which enable logical permission'
                 'systems to complex permissions'),
    long_description=README,
    long_description_content_type='text/x-rst',
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
    install_requires=[r for r in (BASE_DIR / "requirements.txt").read_text().split("\n") if r.strip()],
)

# Contributing Guide

👍🎉 First off, thanks for taking the time to contribute! 🎉👍

## Setup Development Environment

First, make sure you are using pyenv (https://github.com/pyenv/pyenv) and poetry (https://python-poetry.org/).
Once that's installed, create your virtualenv:

```shell
pyenv install --skip-existing
poetry env use $(pyenv which python)
poetry install --extras=docs
```

## Install development tools

```shell
poetry install
```

## Run tests

You can run the tests using the current installed python and django version using

```shell
poetry run python manage.py test tests/
```

Running a complete test suite against all supported python and django versions is possible using `tox`

```shell
poetry run tox
# or use the `--parallel` flag to speed up execution
poetry run tox --parallel
# you can run tox against a single env combination using the `-e` option
poetry run tox -e py310-django42
```

To get the coverage report use the following commands

```shell
poetry run coverage run --append --source=permission manage.py test tests
poetry run coverage report
```

## Generate the docs

```shell
poetry install --extras docs
cd docs/
make clean
make html
```

## Build package

```shell
poetry build --clean
```

## Bump version

```shell
poetry version prerelease
poetry version patch
poetry version minor
poetry version major
```

## Poetry Publish

Publish to PyPI test instance

```shell
poetry publish -r test-pypi
```

Publish to official PyPI index

```shell
poetry publish
```

You can add the `--build` flag to build the package before publishing

```shell
poetry publish --build
```

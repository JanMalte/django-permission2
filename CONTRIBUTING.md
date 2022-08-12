## Install development tools

    poetry install

## Run tests

You can run the tests using the current installed python and django version using

    poetry run python manage.py test src/

Running a complete test suite against all supported python and django versions is possible using `tox`

    tox
    # or use the `--parallel` flag to speed up execution
    tox --parallel
    # you can run tox against a single env combination using the `-e` option
    tox -e py38-django40

To get the coverage report use the following commands

    poetry run coverage run --append --source=src/permission manage.py test permission
    poetry run coverage report

## Generate the docs

    poetry install --extras docs
    cd docs/
    make clean
    make html

## Build package

    poetry build

## Bump version

    poetry version prerelease
    poetry version patch

## Poetry Publish

Publish to PyPI test instance

    poetry publish -r test-pypi

Publish to official PyPI index

    poetry publish

You can add the `--build` flag to build the package before publishing

    poetry publish --build

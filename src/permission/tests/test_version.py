# coding=utf-8
from django.test import TestCase


class VersionTestCase(TestCase):
    def test_version_is_available(self):
        from permission import __version__

        self.assertIsNotNone(__version__)

    def test_version_is_a_string(self):
        from permission import __version__

        self.assertIsInstance(__version__, str)

    def test_version_is_a_semver_string(self):
        from permission import __version__

        self.assertRegex(__version__, r"\d+\.\d+\.\d+")

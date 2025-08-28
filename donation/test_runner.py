"""
Custom Django test runner that runs system checks before tests.
"""

from django.test.runner import DiscoverRunner
from django.core.checks import run_checks, Error


class SystemCheckTestRunner(DiscoverRunner):
    """
    Runs Django's system checks before executing the test suite.
    """

    def run_tests(self, test_labels, **kwargs):
        # Run system checks and abort on any errors
        errors = run_checks()
        failures = [e for e in errors if isinstance(e, Error)]
        if failures:
            failure_msgs = "\n".join(str(e) for e in failures)
            raise RuntimeError(
                f"System check failures before running tests:\n{failure_msgs}"
            )
        return super().run_tests(test_labels, **kwargs)

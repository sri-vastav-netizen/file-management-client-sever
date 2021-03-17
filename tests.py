"""
This program deals with the testing of
the server-client application
"""
import unittest
import sys
import pandas
import os
import shutil


class TestClient(unittest.TestCase):
    pass


def step_completed(test):
    """
    This function deals with execution of all the
    tests in sequence and returns the result
    """

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(test))
    runtest = unittest.TextTestRunner(verbosity=2)
    result = runtest.run(suite)

    if result.skipped:
        return False

    return result.wasSuccessful()


def testing():
    """
    This function executes the function of step_completed
    """
    print('*'*60 + "\nTesting:\n")
    return step_completed(TestClient)

if __name__ == "__main__":
    if testing() is not True:
        print("\n\tThe tests did not pass,")
        sys.exit(1)

    sys.exit(0)
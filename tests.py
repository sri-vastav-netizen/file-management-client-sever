"""
This program deals with the testing of
the server-client application
"""
import unittest
import sys
import os
import shutil
import pandas
from commandhandler import CommandHandler


class TestClient(unittest.TestCase):
    
    def test_commands_output(self):
        """This test deals with testing whether correct description of 
        commands is returned by the server to client.
        """
        commands = ["register : To register as a new user ,command:register <username> <password> \n",
                 "login : To login (only works if you already registered), command:login <username> <password>,Note:password should be in integer\n",
                 "quit : To logout, command:quit\n",
                 "change_folder : To change the current path, command:change_folder <name>\n",
                 "list : Lists all files in the current path, command:list\n",
                 "read_file : To read content from the file, command:read_file <name>\n",
                 "write_file : To write content into the file, command:write_file <name> <content>\n",
                 "create_folder : To create new folder, command:create_folder <name>\n"
                ]
        expected = "".join(commands)

        test_user = CommandHandler()
        actual = test_user.commands()
        self.assertEqual(expected, actual)



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
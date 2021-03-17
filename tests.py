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
        commands = ["""register : To register as a new user ,
                    command:register <username> <password> \n""",
                    """login : To login , 
                    command:login <username> <password>""",
                    """quit : To logout, 
                    command:quit\n""",
                    """change_folder : To change the current path, 
                    command:change_folder <name>\n""",
                    """list : Lists all files in the current path, 
                    command:list\n""",
                    """read_file : To read content from the file, 
                    command:read_file <name>\n""",
                    """write_file : To write content into the file, 
                    command:write_file <name> <content>\n""",
                    """create_folder : To create new folder, 
                    command:create_folder <name>\n"""
                ]
        expected = "".join(commands)

        test_user = CommandHandler()
        actual = test_user.commands()
        self.assertEqual(expected, actual)

    def test_registration(self):

        """This test deals with testing whether register command is working or not!
        """

        test_user = CommandHandler()
        expected = "\nSuccess! Registered test1"
        actual = test_user.register("test1", "17bfdsbgl")
        self.assertEqual(expected, actual)

    def test_registration_with_weak_password(self):
        
        """This test checks the registretion method sends information 
        if the user attempts to register with a weak password
        """

        test_user = CommandHandler()
        expected = "\n Password length should be more than 8 characters."
        actual = test_user.register("test2", "hdfgh")
        self.assertEqual(expected, actual)

    def test_login(self):

        """This test deals with testing whether a user after a proper registeration is 
        able to login into the system or not!
        """

        test_user = CommandHandler()
        test_user.register("test3", "125354nnn3883")
        expected = "Success test3 Logged into the system"
        actual = test_user.login("test3", "125354nnn3883")
        self.assertEqual(expected, actual)

    def test_login_with_wrong_password(self):

        """This test deals with testing when a user attempts to login with wrong 
        password the system throws an error 'Wrong Password'
        """

        test_user = CommandHandler()
        test_user.register("test4", "jsdlghosd")
        expected = "\nSorry, The password you entered is wrong. Please Try Again"
        actual = test_user.login("test4", "jsdlgholgegl")
        self.assertEqual(expected, actual)

    def test_quit(self):

        """Tests if the user able to safely quit from the system.
        """

        test_user = CommandHandler()
        test_user.register("test5", "bdghkga")
        test_user.login("test5", "bdghkga")
        expected = test_user.quit()
        actual = "\nLogged Out"
        self.assertEqual(expected, actual)

    def test_create_folder(self):

        """Tests if the user able to create a folder
        """

        test_user = CommandHandler()
        test_user.register("test6", "jgldaoghgealg8014")
        test_user.login("test6", "jgldaoghgealg8014")
        expected = test_user.create_folder("movies")
        actual = "\nSuccessfully created folder movies"
        self.assertEqual(expected, actual)
        
    def test_create_already_existing_folder(self):

        """Tests if the user is attempting to create 
        a folder which is already existing.
        """

        test_user = CommandHandler()
        test_user.register("test7", "lognslb402193570")
        test_user.login("test7", "lognslb402193570")
        test_user.create_folder("movies")
        expected = "\nThe folder already exists!"
        actual = test_user.create_folder("movies")
        self.assertEqual(expected, actual)

    def test_change_folder(self):

        """Tests if the user is attempting to move the location 
        of the directory tree.
        """

        test_user = CommandHandler()
        test_user.register("test8", "rgglherglse9421-4")
        test_user.login("test8", "rgglherglse9421-4")
        test_user.create_folder("movies")
        expected = "\nSuccessfully Moved to folder Root/test8\movies"
        actual = test_user.change_folder("movies")
        self.assertEqual(expected, actual)

    def test_write_file(self):

        """Tests if the user is attempting to create and 
        write content into a file
        """

        test_user = CommandHandler()
        test_user.register("test9", "nlndgsvns")
        test_user.login("test9", "nlndgsvns")
        
        expected = "\nCreated and written data to file k.txt successfully"
        actual = test_user.write_file("k.txt", "Hello World")
        self.assertEqual(expected, actual)
        # Check also if the user able to append new data to the 
        # existing file
        expected = "\nSuccess Written data to file k.txt successfully"
        actual = test_user.write_file("k.txt", "Hello Second World")
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
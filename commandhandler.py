"""
This program handles the commands
passed by the client to server.
"""

import pathlib
import os
import pandas
import time
from shutil import rmtree
import csv

class CommandHandler():

    ROOT_DIR = "Root/"
    def __init__(self):

        self.user_id = ""
        self.is_login = None
        self.registered_users = None
        self.logged_in_users = None
        self.current_dir = CommandHandler.ROOT_DIR
        self.read_index = {}
        self.char_count = 100

    def commands(self):
        """Returns commands description that can be used by the user to interact with file server.
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

        desc = ""
        for command in commands:
            desc += command
        return desc

    
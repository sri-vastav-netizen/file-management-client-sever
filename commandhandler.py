"""
This program handles the commands
passed by the client to server.
"""


import os
import time
import pandas


class CommandHandler:
    """
    Handles all the commands received from the client.
    Acts as helper program to the server.

    Returns
    -------
    Object
        CommandHandler Object
    """

    ROOT_DIR = "Root/"
    REGISTERED_USERS_CSV_FILE = "AccessSession/registered_users.csv"
    LOGGED_IN_USERS_CSV_FILE = "AccessSession/logged_in_users.csv"
    CSV_HEADING = "username,password\n"

    def __init__(self):
        """
        TODO
        """
        self.user_id = ""
        self.is_login = None
        self.registered_users = None
        self.logged_in_users = None
        self.current_dir = CommandHandler.ROOT_DIR
        self.read_index = {}
        self.char_count = 100

    def commands(self):    
        commands = ["""register : To register as a new user,
                    command:register <username> <password> \n""",
                    """login : To login,
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

        return "".join(commands)

    def access_user_info(self):
        """
        TODO
        """
        if not os.path.exists("AccessSession"):
            os.mkdir("AccessSession")

        if not os.path.isfile(CommandHandler.REGISTERED_USERS_CSV_FILE):
            with open(CommandHandler.REGISTERED_USERS_CSV_FILE, "w") as writer:
                writer.write(CommandHandler.CSV_HEADING)
        if not os.path.isfile(CommandHandler.LOGGED_IN_USERS_CSV_FILE):
            with open(CommandHandler.LOGGED_IN_USERS_CSV_FILE, "w") as writer:
                writer.write(CommandHandler.CSV_HEADING)
        self.logged_in_users = pandas.read_csv(CommandHandler.LOGGED_IN_USERS_CSV_FILE)
        self.registered_users = pandas.read_csv(CommandHandler.REGISTERED_USERS_CSV_FILE)


    def register(self, user_id, password):
        """
        TODO

        Parameters
        ----------
        user_id : str
            Username of the client
        password : str
            Password set by the client

        Returns
        -------
        str
            On Success:
                Success! Registered <username>
            On Failure:
                Password length should be more than 8 characters 
                Username not available
        """
        self.access_user_info()
        if user_id in self.registered_users['username'].tolist():
            return "\nUsername not available"
        if len(password) < 8:
            return "\n Password length should be more than 8 characters."
        with open(CommandHandler.REGISTERED_USERS_CSV_FILE, "a") as writer:
            writer.write(user_id+","+password+"\n")
        if not os.path.exists(self.current_dir):
            os.mkdir(self.current_dir)
        os.mkdir(os.path.join(self.current_dir, user_id))
        self.user_id = user_id
        return "\nSuccess! Registered " + self.user_id

    def login(self, user_id, password):
        """
        TODO

        Parameters
        ----------
        user_id : str
            Username of the logged in user
        password : str
            Password of the logged in user

        Returns
        -------
        str
            On Success:
                Case 1: First Login
                -------------------
                Success <username> Logged into the system
                Case 2: Logged from another system
                ----------------------------------
                You logged through another system
                Case 3: Re-logged
                -----------------
                Already logged in 
            On Failure:
                Case 1: If not registered
                --------------------------
                You haven't registered! Please register--> 
                command: register <username> <password>
                Case 2: If Password is wrong
                ----------------------------
                Sorry, The password you entered is wrong. Please Try Again
        """

        self.access_user_info()
        if self.is_login:
            return "\nAlready logged in"
        if user_id not in self.registered_users['username'].tolist():
           # print (self.registered_users)
            return "\nYou haven't registered! command: register <username> <password>"
        if password not in self.registered_users['password'].tolist() and user_id in self.registered_users['username'].tolist():
            return "\nSorry, The password you entered is wrong. Please Try Again"
        if user_id in self.logged_in_users['username'].tolist():
            self.is_login = True
            self.user_id = user_id
            self.current_dir = self.current_dir + self.user_id
            return "\nYou logged through another system"
        
        self.is_login = True
        self.user_id = user_id
        self.current_dir = self.current_dir + self.user_id
        with open(CommandHandler.LOGGED_IN_USERS_CSV_FILE, "a") as writer:
            writer.write(user_id + "," + password + "\n")
        return "Success " + self.user_id + " Logged into the system"

    def quit(self):
        """
        TODO

        Returns
        -------
        str
            On Success:
                Case 1: Safe Logout
                -------------------
                Logged Out
                Case 2: Forced Logout
                ---------------------
                Forced Logged Out through Keyboard Interruption (CTRL-C)   
        """
        
        try:
            self.access_user_info()
            with open(CommandHandler.LOGGED_IN_USERS_CSV_FILE, "w") as file:
                file.write(CommandHandler.CSV_HEADING)
                user_ids = self.logged_in_users['username'].tolist()
                passwords = self.logged_in_users['password'].tolist()
                for index, user_id in enumerate(user_ids):
                    if self.user_id != str(user_id):
                        file.write(user_id +","+passwords[index])
            self.is_login = False
            self.user_id = ""
            return "\nLogged Out"
        except KeyError:
            return "\nForced Logged Out through Keyboard Interruption (CTRL-C)"

    def create_folder(self, folder):
        """
        TODO

        Parameters
        ----------
        folder : str
            Folder Name

        Returns
        -------
        str
            On Success:
                Successfully created folder <folder-name>
            On Failure:
                The folder already exists
        """

        if not self.is_login:
            return "\nLogin to continue"
        self.access_user_info()
        path = os.path.join(self.current_dir)
        try:
            os.mkdir(os.path.join(path, folder))
        except FileExistsError:
            return "\nThe folder already exists!"
        return "\nSuccessfully created folder " + folder

    def change_folder(self, folder):
        """
        TODO

        Parameters
        ----------
        folder : str
            Folder name

        Returns
        -------
        str
            On Success:
                Successfully moved to folder <current-folder>
            On Failure:
                Case 1: If the user attempts to move parent 
                folder of "Root/<username>" folder
                -------------------------------------------
                Cannot Move Back from Root/<username> folder
                Case 2: If the user attempts to move to 
                non-existing folder
                -------------------------------------------
                No such folder exists
        """

        if not self.is_login:
            return "\nLogin to continue"

        self.access_user_info()
        if folder == ".." and self.current_dir != CommandHandler.ROOT_DIR + self.user_id:
            self.current_dir = os.path.dirname(os.path.join(self.current_dir))
            return "\nSuccessfully moved to folder " + self.current_dir
        
        elif folder == ".." and self.current_dir == CommandHandler.ROOT_DIR + self.user_id:
            return "\nCannot Move Back from Root/" + self.user_id + " folder"

        if folder in os.listdir(self.current_dir):
            self.current_dir = os.path.join(self.current_dir, folder)
            return "\nSuccessfully Moved to folder " + self.current_dir
        return "\n No such folder exists"

    
    def write_file(self, filename, data):
        """
        TODO

        Parameters
        ----------
        filename : str
            Name of the name to which content to be written
        data : str
            Content to be written to a file

        Returns
        -------
        str
            On Success:
              Case 1: On Creating new file and writing content
              ------------------------------------------------
              Created and Written data to file <filename> successfully
              Case 2: Writing content to already existing file
              ------------------------------------------------
              Success Written data to file <filename> successfully
        """

        self.access_user_info()
        if not self.is_login:
            return "\nLogin to Continue"
        t_file = []
        for file in os.listdir(os.path.join(self.current_dir)):
            if os.path.isfile(os.path.join(self.current_dir, file)):
                t_file.append(file)
            
        writeable_data = ""
        path = os.path.join(self.current_dir, filename)
        for i in data:
            writeable_data += i
        if filename in t_file:
            with open(path, "a+") as file:
                file.write(writeable_data)
            return "\nSuccess Written data to file " + filename + " successfully"
        with open(path, "w+") as file:
            file.write(writeable_data)
        return "\nCreated and written data to file " + filename + " successfully"

    def read_file(self, filename):
        """
        TODO

        Parameters
        ----------
        filename : str
            Name of the file to be read

        Returns
        -------
        str
            On Success:
                Read file from <old_index> to <current_index> are <content>
            On Failure:
                If file does not exists:
                ------------------------
                Return No Such file <filename> exists!
        """
        self.access_user_info()
        if not self.is_login:
            return "\nLogin to Continue"
        try:
            t_path = os.path.join(self.current_dir, filename)
        except FileExistsError:
            "\nReturn No Such file " + filename + "exists!"
        if t_path not in list(self.read_index.keys()):
            self.read_index[t_path] = 0
        with open(t_path, "r") as file:
            content = file.read()
        old_index = str(self.read_index[t_path]*self.char_count)
        index = self.read_index[t_path]
        data = content[index*self.char_count:(index+1)*self.char_count]
        self.read_index[t_path] += 1
        self.read_index[t_path] %= len(content) // self.char_count + 1
        return "\n" + "Read file from " + old_index + " to " + str(int(old_index)+self.char_count) + "are\n" + data

    def list(self):
        """
        TODO

        Returns
        -------
        str
            File   | Size           | Modified Date
            <file> | <size_of_file> | <time_file_modified>
        """

        self.access_user_info()
        if not self.is_login:
            return "\nLogin to Continue!"
        path = os.path.join(self.current_dir)
        folders = []
        try:
            for file_name in os.listdir(path):
               file_stats = os.stat(os.path.join(path, file_name))
               folders.append([file_name, str(file_stats.st_size), str(time.ctime(file_stats.st_ctime))])
        except NotADirectoryError:
            return "\nNot A Directory"
        details = "\nFile | Size | Modified Date"
        for folder in folders:
            line = " | ".join([folder[0], folder[1], folder[2]]) + "\n"
            details += "-----------------------\n" + line
        return details

    

    




    




    
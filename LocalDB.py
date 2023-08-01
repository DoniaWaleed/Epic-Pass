import hashlib
import random
import sqlite3

import onetimepad
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from cryptography.fernet import Fernet


class Shuffler:

    @classmethod
    def shuffle_under_seed(cls, ls, seed):
        # Shuffle the list ls using the seed `seed`
        random.seed(seed)
        random.shuffle(ls)
        return ls

    @classmethod
    def unshuffle_list(cls, shuffled_ls, seed):
        n = len(shuffled_ls)
        # Perm is [1, 2, ..., n]
        perm = [i for i in range(1, n + 1)]
        # Apply sigma to perm
        shuffled_perm = cls.shuffle_under_seed(perm, seed)
        # Zip and unshuffle
        zipped_ls = list(zip(shuffled_ls, shuffled_perm))
        zipped_ls.sort(key=lambda x: x[1])
        return [a for (a, b) in zipped_ls]


class SecureDB:
    # constructor for the object
    def __init__(self, path_to_db_exists, start_page, pass_exists, password=None, dataBasePath="Password_Manager.db"):

        self.path_to_db_exists = path_to_db_exists
        self.startPage = start_page
        self.dataBasePath = dataBasePath
        # main sqlite3 connection object
        self.connection = sqlite3.connect(dataBasePath)

        if path_to_db_exists:
            if pass_exists:
                if password == None:
                    raise RuntimeError("Password is not Passed")

                # storing into object
                self.password = str(password)

                self.table_exists = False
                try:
                    self.connection.execute("SELECT * FROM Password_Manager")
                    print('Table Exists')

                except sqlite3.OperationalError:
                    print("Creating Tables Now!!")
                    # create database table and populate it with release_list
                    self.connection.execute(
                        "CREATE TABLE Password_Manager (Username TEXT, Password TEXT, URL TEXT, Notes TEXT, Category TEXT)")
                    self.connection.commit()
                print("Opened DataBase successfully")
                self.table_exists = True

                self.wrong_pass = self.validate_password()
            else:
                self.password = None
        else:
            self.path_to_db_exists = True
            if pass_exists:
                if password == None:
                    raise RuntimeError("Password is not Passed")

                # storing into object
                self.password = str(password)

                self.table_exists = False
                try:
                    self.connection.execute("SELECT * FROM Password_Manager")
                    print('Table Exists')

                except sqlite3.OperationalError:
                    print("Creating Tables Now!!")
                    # create database table and populate it with release_list
                    self.connection.execute(
                        "CREATE TABLE Password_Manager (Username TEXT, Password TEXT, URL TEXT, Notes TEXT, Category TEXT)")
                    self.connection.commit()
                print("Opened DataBase successfully")
                self.table_exists = True

                # # print all the rows from the Password_Manager table
                # print("At Opening------------------------------------------------------------")
                # for row in self.connection.execute("select * from Password_Manager"):
                #     print(row)

                self.create_Auth_table()
            else:
                raise RuntimeError("Can't Create Authentication Table without Password")

    def create_Auth_table(self):
        self.connection.execute("CREATE TABLE authenticationTable (SHA512_pass TEXT , encryptedKey TEXT)")
        self.connection.commit()

        # converting password to SHA512
        sha512Pass = hashlib.sha512(self.password.encode()).hexdigest()
        # converting password to SHA256
        sha256Pass = hashlib.sha256(self.password.encode()).hexdigest()
        # getting a random key from fernet
        stringKey = Fernet.generate_key().decode("utf-8")
        # encrypting this key
        encryptedKey = onetimepad.encrypt(stringKey, sha256Pass)
        # adding sha512 password and encrypted key to database
        self.connection.execute("INSERT INTO authenticationTable (SHA512_pass , encryptedKey) VALUES ({} , {})".format(
            "'" + sha512Pass + "'", "'" + encryptedKey + "'"))
        self.connection.commit()

        # generating key to decrypt key
        sha256Pass = hashlib.sha256(self.password.encode()).hexdigest()
        self.sha256Pass = sha256Pass

        # decrypting key
        decryptedKey = onetimepad.decrypt(encryptedKey, sha256Pass)

        # initialising fernet module
        self.stringKey = decryptedKey
        self.key = bytes(self.stringKey, "utf-8")
        self.cipherSuite = Fernet(self.key)

        self.md5Pass = hashlib.md5(self.password.encode()).hexdigest()

    def checkDefaultPass(self, startPage):
        # print all the rows from the authenticationTable table
        # print("At authenticationTable------------------------------------------------------------")
        for row in self.connection.execute("select SHA512_pass from authenticationTable"):
            # print(row)
            SHA512_pass_inTable = row[0]

        # converting default password to SHA512
        defPassword = '12345678'
        sha512Pass = hashlib.sha512(defPassword.encode()).hexdigest()

        if sha512Pass == SHA512_pass_inTable:
            startPage.label_warning.setVisible(True)
        else:
            # startPage.label_warning.clear()
            startPage.label_warning.setVisible(False)

    def validate_password(self):
        # validate the password passed to password stored in database

        # converting password to SHA512
        sha512Pass = hashlib.sha512(self.password.encode()).hexdigest()

        # getting the password and encrypted key from db
        for i in self.connection.execute("SELECT * FROM authenticationTable;"):
            sha512PassFromDB = i[0]
            encryptedKey = i[1]

        # validating and raising error if not match
        if (sha512PassFromDB != sha512Pass):
            self.wrong_pass = True
        else:
            self.wrong_pass = False
            # generating key to decrypt key
            sha256Pass = hashlib.sha256(self.password.encode()).hexdigest()
            self.sha256Pass = sha256Pass

            # decrypting key
            decryptedKey = onetimepad.decrypt(encryptedKey, sha256Pass)

            # initialising fernet module
            self.stringKey = decryptedKey
            self.key = bytes(self.stringKey, "utf-8")
            self.cipherSuite = Fernet(self.key)

            self.md5Pass = hashlib.md5(self.password.encode()).hexdigest()
        return self.wrong_pass

    # getter method
    def get_password(self):
        return self.password

    # def set_and_create_password(self, x):
    #     self.password = x
    #     if self.password == None:
    #         raise RuntimeError("Password is not Passed")
    #
    #     # storing into object
    #     self.password = str(self.password)
    #
    #     self.table_exists = False  # ///// db_exists
    #     try:
    #         self.connection.execute("SELECT * FROM Password_Manager")
    #         print('Table Exists')
    #
    #     except sqlite3.OperationalError:
    #         print("Creating Tables Now!!")
    #         # create database table and populate it with release_list
    #         self.connection.execute(
    #             "CREATE TABLE Password_Manager (Username TEXT, Password TEXT, URL TEXT, Notes TEXT)")
    #         self.connection.commit()
    #     print("Opened DataBase successfully")
    #     self.table_exists = True
    #
    #     # print all the rows from the Password_Manager table
    #     print("At Opening------------------------------------------------------------")
    #     for row in self.connection.execute("select * from Password_Manager"):
    #         print(row)
    #
    #     self.create_Auth_table()


    def set_and_validate_password(self, x):
        self.password = x
        if self.password == None:
            raise RuntimeError("Password is not Passed")

        # storing into object
        self.password = str(self.password)

        self.table_exists = False  # ///// db_exists
        try:
            self.connection.execute("SELECT * FROM Password_Manager")
            print('Table Exists')

        except sqlite3.OperationalError:
            print("Creating Tables Now!!")
            # create database table and populate it with release_list
            self.connection.execute(
                "CREATE TABLE Password_Manager (Username TEXT, Password TEXT, URL TEXT, Notes TEXT, Category TEXT)")
            self.connection.commit()
        print("Opened DataBase successfully")
        self.table_exists = True

        # # print all the rows from the Password_Manager table
        # print("At Opening------------------------------------------------------------")
        # for row in self.connection.execute("select * from Password_Manager"):
        #     print(row)

        self.new_Pass_Validate = self.validate_password()

        return self.new_Pass_Validate


    def checkTableExist(self, tableName):

        table_exists = False
        query = "SELECT * FROM " + tableName
        try:
            self.connection.execute(query)
            table_exists = True

        except sqlite3.OperationalError:
            print('Table does not Exist')

        return table_exists

    # function to encrypt the passed string
    def encryptor(self, string):
        # encrypting
        stringToPass = bytes(string, "utf-8")
        encodedText = self.cipherSuite.encrypt(stringToPass)
        encodedText = encodedText.decode("utf-8")

        # shuffling
        list_encodedText = list(encodedText)
        shuffled_encodedTextList = Shuffler.shuffle_under_seed(list_encodedText, self.md5Pass)
        encodedText = ''.join(shuffled_encodedTextList)

        return encodedText

    # function to decrypt the passed string
    def decryptor(self, string):
        # deshuffling
        list_string = list(string)
        deshuffledString = Shuffler.unshuffle_list(list_string, self.md5Pass)
        string = ''.join(deshuffledString)

        # decrypting
        stringToPass = bytes(string, "utf-8")
        decodedText = self.cipherSuite.decrypt(stringToPass)
        return decodedText.decode("utf-8")

    # function to change the password in database
    # we need to encrypt the key using new password and change it in database
    # we need to change the SHA512 value in database
    def changePassword(self, newPass):
        newPass_str = str(newPass)
        oldPass = self.password

        Table_decrypted_old_pass = self.getFromTable_decrypted('Password_Manager')
        self.connection.execute('DELETE FROM Password_Manager')
        self.connection.commit()

        # converting password to SHA512
        oldSha512Pass = hashlib.sha512(self.password.encode()).hexdigest()
        new_sha512Pass = hashlib.sha512(newPass_str.encode()).hexdigest()

        # converting password to SHA256
        new_sha256Pass = hashlib.sha256(newPass_str.encode()).hexdigest()

        key = self.stringKey

        # key encrypted using new password
        encryptedKey = onetimepad.encrypt(key, new_sha256Pass)

        # change the key
        stringToExe = """UPDATE authenticationTable set encryptedKey = '{}' where SHA512_pass = '{}'""".format(encryptedKey, oldSha512Pass)
        self.connection.execute(stringToExe)
        self.connection.commit()

        # change the sha512 value
        stringToExe = """UPDATE authenticationTable set SHA512_pass = '{}' where SHA512_pass = '{}'""".format(new_sha512Pass, oldSha512Pass)
        self.connection.execute(stringToExe)
        self.connection.commit()

        self.password = newPass_str
        self.md5Pass = hashlib.md5(self.password.encode()).hexdigest()

        for row in Table_decrypted_old_pass:
            self.insertIntoTable_encrypted('Password_Manager', row)

    def insertIntoTable_encrypted(self, tableName, insertList, commit=True):
        list_to_insert = list(insertList)

        list_encrypted = []
        for element in list_to_insert:
            list_encrypted.append(self.encryptor(str(element)))

        self.connection.execute("INSERT INTO {}".format(tableName) + "(Username, Password, URL, Notes, Category) VALUES ({},{},{},{},{});".format("'" + list_encrypted[0] + "'", "'" + list_encrypted[1] + "'", "'" + list_encrypted[2] + "'", "'" + list_encrypted[3] + "'" , "'" + list_encrypted[4] + "'"))

        # # print all the rows from the Password_Manager table
        # print("At Insert------------------------------------------------------------")
        # for row in self.connection.execute("select * from Password_Manager"):
        #     print(row)

        if commit:
            self.connection.commit()

    def getFromTable_decrypted(self, tableName):# , condition='All'
        self.tableName = tableName
        # self.condition = condition

        table_encrypted = None

        query = "SELECT * FROM " + self.tableName
        table_encrypted = self.connection.execute(query)

        list_of_rows_encrypted = []
        for row in table_encrypted:
            list_of_rows_encrypted.append(row)

        list_of_rows_decrypted = []
        element_list_decrypted = []
        for row in list_of_rows_encrypted:
            for element in row:
                element_list_decrypted.append(self.decryptor(str(element)))
            list_of_rows_decrypted += [element_list_decrypted]
            element_list_decrypted = []

        return list_of_rows_decrypted

    def edit_entry(self, row_num, selection, new_entry):

        self.row_num = row_num
        self.selection = selection
        self.new_entry = new_entry

        Table_decrypted_old = self.getFromTable_decrypted('Password_Manager')
        self.connection.execute('DELETE FROM Password_Manager')
        self.connection.commit()

        duplicate_found = False
        if self.selection == 'Password':
            for row in Table_decrypted_old:
                if self.new_entry.strip() in row:
                    error = QMessageBox()
                    error.setWindowTitle("Error!!")
                    error.setIcon(QMessageBox.Critical)
                    error.setWindowIcon(QIcon('images/icon.png'))
                    error.setText("Password already in Database                       ")
                    error.exec()
                    duplicate_found = True
                    break
        counter = 0
        for row in Table_decrypted_old:
            if str(counter) == self.row_num:
                if self.selection == 'Username':
                    row[0] = self.new_entry
                elif self.selection == 'Password' and not duplicate_found:
                    row[1] = self.new_entry
                elif self.selection == 'URL':
                    row[2] = self.new_entry
                elif self.selection == 'Notes':
                    row[3] = self.new_entry
                elif self.selection == 'Category':
                    row[4] = self.new_entry

            self.insertIntoTable_encrypted('Password_Manager', row)
            counter += 1
        return duplicate_found
    def row_count(self):
        table_list = self.getFromTable_decrypted("Password_Manager")
        count = len(table_list)

        return count


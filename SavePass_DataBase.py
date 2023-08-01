import os.path
import time
import webbrowser
from pathlib import Path
import pandas as pd
import validators as validators
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from LocalDB import *


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


# class DB_Pass(QWidget):
#
#     def __init__(self):
#         super().__init__()
#
#         DB_Pass_mainLayout = QVBoxLayout()
#         Flayout = QFormLayout()
#
#         self.password_editText = QLineEdit()
#         Flayout.addRow("Password: ", self.password_editText)
#         DB_Pass_mainLayout.addLayout(Flayout)
#         DB_Pass_mainLayout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)
#
#         self.setLayout(DB_Pass_mainLayout)
#
#     # getter method
#     def get_password_editText(self):
#         return self.password_editText.text()


class SavePass_DB(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        self.table = QtWidgets.QTableView()
        data = pd.DataFrame(columns=['Username', 'Password', 'URL', 'Notes', 'Category'])

        self.model = TableModel(data)
        self.table.setModel(self.model)

        header_horizontal = self.table.horizontalHeader()
        header_vertical = self.table.verticalHeader()

        header_horizontal.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header_horizontal.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header_horizontal.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header_horizontal.setStretchLastSection(False)

        header_vertical.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size.setHorizontalStretch(1)
        self.table.setSizePolicy(size)
        self.table.adjustSize()
        self.main_layout.addWidget(self.table)

        self.table.setMouseTracking(True)
        self.table.setCursor(Qt.PointingHandCursor)

        self.table.doubleClicked.connect(lambda: self.OpenLink(self.table.currentIndex()))

        self.setLayout(self.main_layout)
    #     self.setMouseTracking(True)
    #
    # def mouseMoveEvent(self, event):
    #     super().mouseMoveEvent(event)
    #     time.sleep(60)
    #     self.setMouseTracking(True)
    #     if not event.buttons():
    #         index = self.table.indexAt(event.pos())
    #         if index.column() == 2:
    #             self.setToolTip("Double-Click to Open URL")
    #             self.setToolTipDuration(1300)
    #         else:
    #             self.setToolTip("Testtt")
    #             # self.setToolTipDuration(0)

    def OpenLink(self, link):
        # Error Box
        error = QMessageBox()
        error.setWindowTitle("Error!!")
        error.setText("Invalid URL                                     ")
        error.setIcon(QMessageBox.Critical)
        WindowIcon = QIcon('images/icon.png')
        error.setWindowIcon(WindowIcon)
        if link.column() == 2:
            url = self.model.data(link, 0)
            print("link: ", url)
            if validators.url(url):
                webbrowser.open(url)
            elif 'http://' and '/' not in url:
                newURL = 'http://' + url + '/'
                if validators.url(newURL):
                    webbrowser.open(newURL)
                else:
                    error.exec_()
            else:
                error.exec_()

class edit_window(QWidget):
    def __init__(self, db_object, save_pass_db):
        QWidget.__init__(self)
        self.setWindowTitle("Edit Item")
        self.setWindowIcon(QIcon('images/icon.png'))
        self.db_object = db_object
        self.save_pass_db = save_pass_db

        mainLayout = QVBoxLayout()
        self.HLayout = QHBoxLayout()

        self.row_number_editText = QLineEdit()
        self.row_number_editText.adjustSize()

        self.editText = QLineEdit()
        self.editText.adjustSize()

        self.category_combobox = QComboBox()
        self.category_combobox.setVisible(False)
        self.category_combobox.adjustSize()
        self.category_combobox.addItems(['Others', 'Email addresses', 'Passwords', 'Secure Notes'])

        self.selection_combobox = QComboBox()
        self.selection_combobox.adjustSize()
        self.selection_combobox.addItems(['Username', 'Password', 'URL', 'Notes', 'Category'])
        self.selection_combobox.currentTextChanged.connect(self.show_box)

        self.button_edit = QPushButton('Edit', self)
        # self.button_edit.setMinimumSize(300, 50)
        self.button_edit.adjustSize()
        self.button_edit.clicked.connect(self.edit)

        Flayout_data = QFormLayout()
        Flayout_data.addRow("Row Number: ", self.row_number_editText)
        Flayout_data.addRow("Choose what to update: ", self.selection_combobox)

        self.HLayout.addWidget(QLabel("New Entry: "))
        self.HLayout.addWidget(self.editText, alignment=QtCore.Qt.AlignCenter)
        self.HLayout.addWidget(self.selection_combobox, alignment=QtCore.Qt.AlignCenter)

        mainLayout.addLayout(Flayout_data)
        mainLayout.addLayout(self.HLayout)
        mainLayout.addWidget(self.button_edit, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(mainLayout)

    def show_box(self):
        if self.selection_combobox.currentText() == 'Category':
            self.category_combobox.setVisible(True)
            self.category_combobox.adjustSize()
            self.editText.setVisible(False)
            self.HLayout.addWidget(self.category_combobox, alignment=QtCore.Qt.AlignCenter)
        else:
            self.editText.setVisible(True)
            self.editText.adjustSize()
            self.category_combobox.setVisible(False)

    # getter method
    def get_row_num(self):
        return self.row_number_editText.text()

    # getter method
    def get_Selection(self):
        return self.selection_combobox.currentText()

    # getter method
    def get_new_entry(self):
        if self.selection_combobox.currentText() == 'Category':
            return self.category_combobox.currentText()
        else:
            return self.editText.text()

    def update_after_edit(self):
        if self.db_object.table_exists:
            data = pd.DataFrame(columns=['Username', 'Password', 'URL', 'Notes', 'Category'])

            for row in self.db_object.getFromTable_decrypted('Password_Manager'):
                pass_list = []
                for cell in row:
                    pass_list.append(cell)
                data.loc[len(data)] = pass_list
        else:
            data = pd.DataFrame(columns=['Username', 'Password', 'URL', 'Notes', 'Category'])
        self.save_pass_db.model = TableModel(data)
        self.save_pass_db.table.setModel(self.save_pass_db.model)

    def edit(self):
        row_num = self.get_row_num()

        selection = self.get_Selection()

        new_entry = self.get_new_entry()
        if int(row_num) < self.db_object.row_count():
            edit_done = not (self.db_object.edit_entry(row_num, selection, new_entry))
            if edit_done:
                print("Selection Updated Successfully")

                done = QMessageBox()
                done.setWindowTitle("Changed Successfully")
                done.setText(selection + " Changed Successfully                           ")
                done.setIcon(QMessageBox.Information)
                done.setWindowIcon(QIcon('images/icon.png'))

                self.close()

                done.exec_()
                self.update_after_edit()
        else:
            error = QMessageBox()
            error.setWindowTitle("Error!!")
            error.setIcon(QMessageBox.Critical)
            error.setWindowIcon(QIcon('images/icon.png'))
            error.setText("Row Not Found                                      ")
            error.exec()


class DB_layout(QtWidgets.QMainWindow):
    def __init__(self, save_pass_db, start_page):
        super().__init__()

        path_to_db_exists = os.path.exists('./Password_Manager.db')

        self.database = SecureDB(path_to_db_exists, start_page, True, '12345678')
        self.save_pass_db = save_pass_db
        self.startPage = start_page
        self.setCentralWidget(self.save_pass_db)
        mainLayout = QVBoxLayout()

        # Change Password item
        changePassAction = QAction('&Change Password', self) #QIcon('./assets/exit.png'),
        changePassAction.setStatusTip('Changing Password now..')
        # exit_action.setShortcut('Alt+F4')
        changePassAction.triggered.connect(lambda: self.change_password(self.database))

        # Copy item
        copyAction = QAction('&Copy', self) #QIcon('./assets/exit.png'),
        copyAction.setStatusTip('Copying..')
        copyAction.setShortcut('CTRL+C')
        copyAction.triggered.connect(lambda: self.copy())

        # Edit item
        editAction = QAction('&Edit', self) #QIcon('./assets/exit.png'),
        editAction.setStatusTip('Editing..')
        editAction.setShortcut('F2')
        editAction.triggered.connect(lambda: self.edit(self.database, self.save_pass_db))

        # Delete item
        deleteAction = QAction('&Delete', self)  # QIcon('./assets/exit.png'),
        deleteAction.setStatusTip('Deleting..')
        deleteAction.setShortcut('Ctrl+-')
        deleteAction.triggered.connect(lambda: self.delete(self.database))

        # Select Category item
        selectAction = QAction('&Select Category', self)  # QIcon('./assets/exit.png'),
        selectAction.setStatusTip('Selecting Category..')
        # selectAction.setShortcut('Ctrl+-')
        selectAction.triggered.connect(lambda: self.select(self.database))

        # Help item
        HelpAction = QAction('&Help', self)  # QIcon('./images/help.png'),
        HelpAction.setIcon(QIcon('./images/help.png'))
        HelpAction.setStatusTip("Double-Click Any URL to Open")
        HelpAction.setToolTip("Double-Click Any URL to Open")

        # toolbar
        toolbar = QToolBar('Main ToolBar')
        self.addToolBar(toolbar)
        toolbar.adjustSize()

        toolbar.setIconSize(QSize(16, 16))

        toolbar.addAction(changePassAction)
        toolbar.addSeparator()

        toolbar.addAction(copyAction)
        toolbar.addSeparator()

        toolbar.addAction(editAction)
        toolbar.addSeparator()

        toolbar.addAction(deleteAction)
        toolbar.addSeparator()

        toolbar.addAction(selectAction)
        toolbar.addSeparator()

        toolbar.addAction(HelpAction)

        # status bar
        self.status_bar = self.statusBar()
        self.status_bar.adjustSize()

        self.show()

        self.setLayout(mainLayout)

    def update_on_pressing_next(self):
        if self.database.table_exists:
            data = pd.DataFrame(columns=['Username', 'Password', 'URL', 'Notes', 'Category'])

            for row in self.database.getFromTable_decrypted('Password_Manager'):
                pass_list = []
                for cell in row:
                    pass_list.append(cell)
                data.loc[len(data)] = pass_list
        else:
            data = pd.DataFrame(columns=['Username', 'Password', 'URL', 'Notes', 'Category'])
        self.save_pass_db.model = TableModel(data)
        self.save_pass_db.table.setModel(self.save_pass_db.model)



    # -------------------------Functions-----------------------------------------------START
    # def next(self):
    #
    #     if self.database.path_to_db_exists == False:
    #         self.database.set_and_create_password(self.db_pass.get_password_editText())
    #         self.database.path_to_db_exists = True
    #
    #         self.SavePass_db_manager.objClass = self.database
    #         self.SavePass_db_manager.update_on_pressing_next()
    #     else:
    #         if self.database.set_and_validate_password(self.db_pass.get_password_editText()):  # True at Wrong Password
    #             # Error Box
    #             error = QMessageBox()
    #             error.setWindowTitle("Error!!")
    #             error.setIcon(QMessageBox.Critical)
    #             WindowIcon = QIcon('images/icon.jpg')
    #             error.setWindowIcon(WindowIcon)
    #             error.setText("Incorrect Password..Please enter correct one   ")
    #             error.exec()
    #         else:
    #             self.stackedLayout.setCurrentIndex(1)
    #             self.button_next.setVisible(False)
    #             self.menuBar.setVisible(True)
    #             self.SavePass_db_manager.update_on_pressing_next()

    def update_table_on_adding(self, db_object):
        data = pd.DataFrame(columns=['Username', 'Password', 'URL', 'Notes', 'Category'])

        # print all the rows from the Password_Manager table
        for row in db_object.getFromTable_decrypted('Password_Manager'):
            pass_list = []
            for cell in row:
                pass_list.append(cell)
            data.loc[len(data)] = pass_list
        self.save_pass_db.model = TableModel(data)
        self.save_pass_db.table.setModel(self.save_pass_db.model)

    def change_password(self, db_object):
        self.updatedPass = QInputDialog()
        self.updatedPass.adjustSize()
        self.updatedPass.setInputMode(0)
        new_password, ok = self.updatedPass.getText(self, 'New Password!!', 'Enter New Password:', QLineEdit.Normal, "")
        if ok:
            self.startPage.set_password_editText(new_password)
            db_object.changePassword(new_password)

            done = QMessageBox()
            done.setWindowTitle("Changed Successfully")
            done.setText("Password Changed Successfully                           ")
            done.setIcon(QMessageBox.Information)
            done.setWindowIcon(QIcon('images/icon.png'))
            done.exec()

    def copy(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        selected_list = self.save_pass_db.table.selectedIndexes()
        selected_as_string = ""
        for selection in selected_list:
            selected_as_string += self.save_pass_db.model.data(selection, 0)
            selected_as_string += ' '
        print("Selected as String: ", selected_as_string)
        cb.setText(selected_as_string, mode=cb.Clipboard)
        print("Copied Selection Successfully")

        clipBoardAlert = QMessageBox()
        clipBoardAlert.setWindowIcon(QIcon('images/icon.png'))
        clipBoardAlert.setWindowTitle("Copied!!")
        clipBoardAlert.setIcon(QMessageBox.Information)
        clipBoardAlert.setText("Copied Selection Successfully")
        clipBoardAlert.exec_()

    def edit(self, db_object, save_pass_db):
        self.edit_window = edit_window(db_object, save_pass_db)
        self.edit_window.show()

    def delete(self, db_object):
        self.row_num_dialog = QInputDialog()
        self.row_num_dialog.adjustSize()
        self.row_num_dialog.setInputMode(0)
        row_num, ok = self.row_num_dialog.getText(self, 'Delete Row!!', 'Enter Row Number:', QLineEdit.Normal, "")
        if ok:
            if int(row_num) < db_object.row_count():
                Table_decrypted_old = db_object.getFromTable_decrypted('Password_Manager')
                db_object.connection.execute('DELETE FROM Password_Manager')
                db_object.connection.commit()

                counter = 0
                for row in Table_decrypted_old:
                    if str(counter) != row_num:
                        db_object.insertIntoTable_encrypted('Password_Manager', row)
                    counter += 1

                done = QMessageBox()
                done.setWindowTitle("Deleted Successfully")
                done.setText("Row Deleted Successfully                           ")
                done.setIcon(QMessageBox.Information)
                done.setWindowIcon(QIcon('images/icon.png'))
                done.exec_()
                self.update_on_pressing_next()
            else:
                error = QMessageBox()
                error.setWindowTitle("Error!!")
                error.setIcon(QMessageBox.Critical)
                error.setWindowIcon(QIcon('images/icon.png'))
                error.setText("Row Not Found                                      ")
                error.exec()
    def select(self, db_object):
        self.selection_dialog = QInputDialog()
        self.selection_dialog.adjustSize()
        self.selection_dialog.setInputMode(0)
        # self.selection_dialog.setComboBoxItems(['Others', 'Email addresses', 'Passwords', 'Secure Notes'])
        selection, ok = self.selection_dialog.getItem(self, 'Choose Category', 'Category:', ['Others', 'Email addresses', 'Passwords', 'Secure Notes', 'All'], 0, False)
        if ok:
            data = pd.DataFrame(columns=['Username', 'Password', 'URL', 'Notes', 'Category'])

            # print all the rows from the Password_Manager table
            for row in db_object.getFromTable_decrypted('Password_Manager'):
                pass_list = []
                if row[4] == selection:
                    for cell in row:
                        pass_list.append(cell)
                    data.loc[len(data)] = pass_list
                elif selection == 'All':
                    for cell in row:
                        pass_list.append(cell)
                    data.loc[len(data)] = pass_list
            self.save_pass_db.model = TableModel(data)
            self.save_pass_db.table.setModel(self.save_pass_db.model)


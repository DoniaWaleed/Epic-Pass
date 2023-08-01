from pathlib import Path
import pandas as pd
from openpyxl import *
from PassGenerator import *
from SavePass import *
from SavePass_DataBase import *
from StartPage import StartPage

# -------------------------Dark Theme--------------------------------------------------
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.black)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
# -------------------------Dark Theme--------------------------------------------------

# -------------------------Class MainWindow----------------------------------------START


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.WindowIcon = QIcon('images/icon.png')
        self.setWindowTitle("Epic Pass")
        self.setWindowIcon(self.WindowIcon)
        self.setMinimumWidth(450)
        # self.setMinimumSize(1100, 1100)
        # geometry = qApp.desktop().availableGeometry(self)
        #
        # self.setMinimumSize(int(geometry.width() * 0.27), int(geometry.height() * 0.456))

        mainLayout = QVBoxLayout()

        self.stackedLayout = QStackedLayout()

        self.startPage = StartPage()  # Initializing an object from StartPage Class

        self.passGen = PassGenerator()  # Initializing an object from PassGenerator Class
        self.PASSWORD = str(self.passGen.copyPass)

        self.db_manager = DB_layout(SavePass_DB(), self.startPage)  # Initializing an object from DB_layout Class

        self.db_manager.database.checkDefaultPass(self.startPage)

        self.startPage.label_warning.adjustSize()

        self.savePassword = SavePass(self.PASSWORD, self.db_manager, self.db_manager.database)  # Initializing an object from SavePass Class

        self.stackedLayout.addWidget(self.startPage)   # index 0
        self.stackedLayout.addWidget(self.passGen)  # index 1
        self.stackedLayout.addWidget(self.savePassword)  # index 2
        self.stackedLayout.addWidget(self.db_manager)  # index 3

        self.button_generate = QPushButton('Generate', self)
        # self.button_generate.setMinimumSize(250, 50)
        self.button_generate.adjustSize()
        self.button_generate.clicked.connect(self.generate)

        self.startPage.password_editText.returnPressed.connect(self.button_generate.click)

        self.button_db_Manager = QPushButton('My Passwords', self)
        # self.button_db_Manager.setMinimumSize(250, 50)
        self.button_db_Manager.adjustSize()
        self.button_db_Manager.clicked.connect(self.db_Manager)

        self.button_save_Manager = QPushButton('Add', self)
        # self.button_save_Manager.setMinimumSize(250, 50)
        self.button_save_Manager.adjustSize()
        self.button_save_Manager.clicked.connect(self.save_Manager)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.button_generate)
        buttonLayout.addWidget(self.button_db_Manager)
        buttonLayout.addWidget(self.button_save_Manager)

        mainLayout.addLayout(self.stackedLayout)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)
        self.adjustSize()


    # -------------------------Functions-----------------------------------------------START
    def generate(self):
        error = QMessageBox()
        error.setWindowTitle("Error!!")
        error.setIcon(QMessageBox.Critical)
        error.setWindowIcon(QIcon('images/icon.png'))

        path_to_db_exists = os.path.exists('./Password_Manager.db')
        if self.startPage.get_password_editText() != "":
            if path_to_db_exists:
                wrong_pass = self.db_manager.database.set_and_validate_password(self.startPage.get_password_editText())
                if wrong_pass:
                    error.setText("Incorrect Password..Please enter correct one   ")
                    error.exec()
                else:
                    self.stackedLayout.setCurrentIndex(1)
                    self.button_generate.setVisible(False)
                    self.button_save_Manager.setVisible(True)
                    self.button_db_Manager.setVisible(True)

        else:
            error.setText("Please Enter a Password                    ")
            error.exec()

    def db_Manager(self):
        error = QMessageBox()
        error.setWindowTitle("Error!!")
        error.setIcon(QMessageBox.Critical)
        error.setWindowIcon(QIcon('images/icon.png'))

        path_to_db_exists = os.path.exists('./Password_Manager.db')
        if self.startPage.get_password_editText() != "":
            if path_to_db_exists:
                wrong_pass = self.db_manager.database.set_and_validate_password(self.startPage.get_password_editText())
                if wrong_pass:
                    error.setText("Incorrect Password..Please enter correct one   ")
                    error.exec()
                else:
                    self.stackedLayout.setCurrentIndex(3)
                    self.button_db_Manager.setVisible(False)
                    self.button_generate.setVisible(True)
                    self.button_save_Manager.setVisible(True)

                    self.db_manager.update_on_pressing_next()

        else:
            error.setText("Please Enter a Password                    ")
            error.exec()

    def save_Manager(self):
        error = QMessageBox()
        error.setWindowTitle("Error!!")
        error.setIcon(QMessageBox.Critical)
        error.setWindowIcon(QIcon('images/icon.png'))

        path_to_db_exists = os.path.exists('./Password_Manager.db')
        if self.startPage.get_password_editText() != "":
            if path_to_db_exists:
                wrong_pass = self.db_manager.database.set_and_validate_password(self.startPage.get_password_editText())
                if wrong_pass:
                    error.setText("Incorrect Password..Please enter correct one   ")
                    error.exec()
                else:
                    self.stackedLayout.setCurrentIndex(2)
                    self.button_save_Manager.setVisible(False)
                    self.button_generate.setVisible(True)
                    self.button_db_Manager.setVisible(True)

                    self.PASSWORD = str(self.passGen.copyPass)
                    self.savePassword.generated_pass_editText.setText(self.PASSWORD)

        else:
            error.setText("Please Enter a Password                    ")
            error.exec()


# -------------------------Functions-----------------------------------------------END
# -------------------------Class MainWindow----------------------------------------END

if __name__ == "__main__":
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    os.environ["QT_DEVICE_PIXEL_RATIO"] = "1"

    app = QApplication(sys.argv)
    app.setPalette(palette)
    app.setStyle("Fusion")


    window = MainWindow()
    window.show()
    app.exec_()


    # # terminate the connection to "Password_Manager.db"
    # connection.close()

    sys.exit()


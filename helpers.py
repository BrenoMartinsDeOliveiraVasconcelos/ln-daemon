from PyQt6.QtWidgets import QFileDialog, QDialog, QMessageBox, QGridLayout, QLabel, QLineEdit, QPushButton
import os
import locale
from sys import argv as args

original_cwd = os.getcwd()
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def get_txt_dict(path: str):
    with open(path, 'r') as f:
        return {line.split("=")[0]: line.split("=")[1].strip() for line in f.readlines()}


def get_locale():
    loc =  locale.getlocale()[0].split("_")[0]
    args.append("")

    if args[1] != "":
        return args[1]

    return loc

english_str = "strings.txt"
localised_str = "strings_" + get_locale() + ".txt"

if os.path.exists(localised_str):
    strings = get_txt_dict(localised_str)
else:
    strings = get_txt_dict(english_str)

def get_file_path():
    return QFileDialog.getOpenFileName()[0]

def get_folder_path():
    return QFileDialog.getExistingDirectory()

def get_new_file_path():
    return QFileDialog.getSaveFileName()[0]

def get_new_folder_path():
    dialog = QDialog()
    dialog.path = ""

    dialog.setWindowTitle(strings["getFolder"])

    layout = QGridLayout()

    # Where the folder will be created
    path_label = QLabel(strings["parentFolder"]+":")
    path_input = QLineEdit()
    path_select_button = QPushButton(strings["pathInput"])
    layout.addWidget(path_label, 0, 0)
    layout.addWidget(path_input, 0, 1)
    layout.addWidget(path_select_button, 0, 2)

    # Folder name
    name_label = QLabel(strings["name"]+":")
    name_input = QLineEdit()
    layout.addWidget(name_label, 1, 0)
    layout.addWidget(name_input, 1, 1)

    # Ok button
    ok_button = QPushButton(strings["confirm"])
    layout.addWidget(ok_button, 2, 0, 1, 3)

    # Cancel button
    cancel_button = QPushButton(strings["cancel"])
    layout.addWidget(cancel_button, 3, 0, 1, 3)

    def on_ok_button_click():
        if path_input.text() == "":
            error_message(strings["pathInputEmpty"])
            return

        if name_input.text() == "":
            error_message(strings["folderNameEmpty"])
            return
        
        dialog.path = path_input.text() + os.path.sep + name_input.text()
        dialog.close()

    
    def on_cancel_button_click():
        dialog.close()

    def on_path_select():
        path = get_folder_path()
        path_input.setText(path)

    path_select_button.clicked.connect(on_path_select)
    ok_button.clicked.connect(on_ok_button_click)
    cancel_button.clicked.connect(on_cancel_button_click)

    dialog.setLayout(layout)
    dialog.exec()

    return dialog.path



def info_message(message: str):
    QMessageBox.information(None, strings["info"], message)

def error_message(message: str):
    QMessageBox.critical(None, strings["error"], message)

def warning_message(message: str):
    QMessageBox.warning(None, strings["warning"], message)

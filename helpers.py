from PyQt6.QtWidgets import QFileDialog, QMessageBox

def get_txt_dict(path: str):
    with open(path, 'r') as f:
        return {line.split("=")[0]: line.split("=")[1].strip() for line in f.readlines()}

strings = get_txt_dict("strings.txt")

def get_file_path():
    return QFileDialog.getOpenFileName()[0]

def get_folder_path():
    return QFileDialog.getExistingDirectory()

def info_message(message: str):
    QMessageBox.information(None, strings["info"], message)

def error_message(message: str):
    QMessageBox.critical(None, strings["error"], message)

from PyQt6.QtWidgets import QFileDialog

def get_txt_dict(path: str):
    with open(path, 'r') as f:
        return {line.split("=")[0]: line.split("=")[1].strip() for line in f.readlines()}
    

def get_file_path():
    return QFileDialog.getOpenFileName()[0]

def get_folder_path():
    return QFileDialog.getExistingDirectory()

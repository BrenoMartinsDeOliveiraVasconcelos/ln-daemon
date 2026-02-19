import sys
import helpers
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QCheckBox, QPushButton, QLabel
import os
import shutil

class LnDaemon(QMainWindow):
    def __init__(self):
        super().__init__()
        self.strings = helpers.strings
        self.setWindowTitle(self.strings["mainName"])
        print(self.strings)

        # Central widget to hold the layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Vertical layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Horizontal layout for original path
        o_path_layout = QHBoxLayout()

        self.original_path_label = QLabel(self.strings["from"]+":")
        self.original_path_input = QLineEdit()
        self.original_path_select_button = QPushButton(self.strings["pathInput"])
        o_path_layout.addWidget(self.original_path_label)
        o_path_layout.addWidget(self.original_path_input)
        o_path_layout.addWidget(self.original_path_select_button)

        # Horizontal layout for link mode
        link_mode_layout = QHBoxLayout()

        self.link_mode_checkbox = QCheckBox(self.strings["soft"])
        self.link_mode_checkbox.setChecked(True)
        
        self.is_folder_checkbox = QCheckBox(self.strings["folder"])
        self.is_folder_checkbox.setChecked(False)

        link_mode_layout.addWidget(self.link_mode_checkbox)
        link_mode_layout.addWidget(self.is_folder_checkbox)

        #Horizontal layout for target path
        t_path_layout = QHBoxLayout()

        self.target_path_label = QLabel(self.strings["to"]+":")
        self.target_path_input = QLineEdit()
        self.target_path_select_button = QPushButton(self.strings["pathInput"])
    
        t_path_layout.addWidget(self.target_path_label)
        t_path_layout.addWidget(self.target_path_input)
        t_path_layout.addWidget(self.target_path_select_button)

        # Horizontal layout for action button
        action_layout = QHBoxLayout()

        self.action_button = QPushButton(self.strings["confirm"])
        action_layout.addWidget(self.action_button)

        # Horizontal layout for inverting folders
        invert_layout = QHBoxLayout()

        self.invert_checkbox = QCheckBox(self.strings["invert"])
        invert_layout.addWidget(self.invert_checkbox)

        # Adding
        layout.addLayout(o_path_layout)
        layout.addLayout(link_mode_layout)
        layout.addLayout(t_path_layout)
        layout.addLayout(action_layout)
        layout.addLayout(invert_layout)


        # Connect signals
        self.target_path_select_button.clicked.connect(lambda: self.on_path_select(self.target_path_input, True))
        self.original_path_select_button.clicked.connect(lambda: self.on_path_select(self.original_path_input))
        self.link_mode_checkbox.stateChanged.connect(self.on_link_mode_updated)
        self.is_folder_checkbox.stateChanged.connect(self.on_folder_checked)
        self.action_button.clicked.connect(self.on_action_button_click)
        self.invert_checkbox.stateChanged.connect(self.on_invert_checked)


    def on_path_select(self, label, is_target=False):

        path = "."
        if self.is_folder_checkbox.isChecked():
            if is_target:
                path = helpers.get_new_folder_path()
            else:
                path = helpers.get_folder_path()
        else:
            if is_target:
                path = helpers.get_new_file_path()
            else:
                path = helpers.get_file_path()

        label.setText(path)

    
    def on_link_mode_updated(self):
        if not self.link_mode_checkbox.isChecked():
            self.is_folder_checkbox.setChecked(False)

    
    def on_folder_checked(self):
        # Hard links cannot be created on folders
        if self.is_folder_checkbox.isChecked():
            self.link_mode_checkbox.setChecked(True)
        return
    
    def on_invert_checked(self):
        if self.invert_checkbox.isChecked():
            helpers.warning_message(self.strings["dangerWarning"])
    

    def on_action_button_click(self):
        # Check input emptiness
        if self.original_path_input.text() == "" or self.target_path_input.text() == "":
            helpers.error_message(self.strings["pathInputEmpty"])
            return
        
        # CHeck if both paths are equal
        if self.original_path_input.text() == self.target_path_input.text():
            helpers.error_message(self.strings["pathInputSame"])
            return

        # Check path existence
        if not os.path.exists(self.original_path_input.text()):
            helpers.error_message(self.strings["pathInvalid"].replace("\\0", self.original_path_input.text()))
            return
        
        # Check if target path exists
        if os.path.exists(self.target_path_input.text()):
            helpers.error_message(self.strings["pathExists"].replace("\\0", self.target_path_input.text()))
            return

        # Check path accessibility
        if not os.access(os.path.split(self.target_path_input.text())[0], os.W_OK) and os.name == "posix": 
            helpers.error_message(self.strings["pathDenied"].replace("\\0", self.target_path_input.text()))
            return


        # Create link
        try:
            self.action_button.setEnabled(False)
            self.action_button.setText(self.strings["wait"])

            self.update()
            origin = self.original_path_input.text()
            target = self.target_path_input.text()

            if self.invert_checkbox.isChecked():
                shutil.move(origin, target)

                origin = target
                target = self.original_path_input.text()

            if self.link_mode_checkbox.isChecked():
                os.symlink(origin, target)
            else:
                os.link(origin, target)

            helpers.info_message(self.strings["success"])
        except PermissionError:
            helpers.error_message(self.strings["pathDeniedNT"])
        except Exception as e:
            helpers.error_message(self.strings["failure"] + ": " + str(e))

        self.target_path_input.setText("")
        self.original_path_input.setText("")
        self.action_button.setText(self.strings["confirm"])
        self.action_button.setEnabled(True)
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LnDaemon()
    window.show()
    ext_code = app.exec()

    os.chdir(helpers.original_cwd)
    sys.exit(ext_code)
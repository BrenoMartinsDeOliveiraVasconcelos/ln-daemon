import sys
import helpers
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QCheckBox, QPushButton, QLabel

class LnDaemon(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LnDaemon")
        self.strings = helpers.get_txt_dict("strings.txt")
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

        # Adding
        layout.addLayout(o_path_layout)
        layout.addLayout(link_mode_layout)
        layout.addLayout(t_path_layout)
        layout.addLayout(action_layout)


        # Connect signals
        self.target_path_select_button.clicked.connect(lambda: self.on_path_select(self.target_path_input))
        self.original_path_select_button.clicked.connect(lambda: self.on_path_select(self.original_path_input))
        self.is_folder_checkbox.clicked.connect(self.on_folder_checked)


    def on_path_select(self, label):

        path = "."
        if self.is_folder_checkbox.isChecked():
            path = helpers.get_folder_path()
        else:
            path = helpers.get_file_path()

        label.setText(path)

    
    def on_folder_checked(self):
        # Hard links cannot be created on folders
        print("Set link mode to soft")
        self.link_mode_checkbox.setChecked(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LnDaemon()
    window.show()
    sys.exit(app.exec())
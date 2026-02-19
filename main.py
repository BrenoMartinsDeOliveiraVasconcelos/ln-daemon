import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QCheckBox, QPushButton

class LnDaemon(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LnDaemon")

        # Central widget to hold the layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Vertical layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Horizontal layout for original path
        o_path_layout = QHBoxLayout()

        self.original_path_input = QLineEdit()
        self.original_path_select_button = QPushButton("...")
        o_path_layout.addWidget(self.original_path_input)
        o_path_layout.addWidget(self.original_path_select_button)

        # Horizontal layout for link mode
        link_mode_layout = QHBoxLayout()

        self.link_mode_checkbox = QCheckBox("Symbolic")
        self.link_mode_checkbox.setChecked(True)
        link_mode_layout.addWidget(self.link_mode_checkbox)

        #Horizontal layout for target path
        t_path_layout = QHBoxLayout()

        self.target_path_input = QLineEdit()
        self.target_path_select_button = QPushButton("...")
        t_path_layout.addWidget(self.target_path_input)
        t_path_layout.addWidget(self.target_path_select_button)

        # Horizontal layout for action button
        action_layout = QHBoxLayout()

        self.action_button = QPushButton("Link")
        action_layout.addWidget(self.action_button)

        # Adding
        layout.addLayout(o_path_layout)
        layout.addLayout(link_mode_layout)
        layout.addLayout(t_path_layout)
        layout.addLayout(action_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LnDaemon()
    window.show()
    sys.exit(app.exec())
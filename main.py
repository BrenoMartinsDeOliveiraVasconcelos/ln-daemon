import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

class LnDaemon(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LnDaemon")
        self.setGeometry(100, 100, 400, 300)  # x, y, width, height

        # Central widget to hold the layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Vertical layout (empty)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LnDaemon()
    window.show()
    sys.exit(app.exec())
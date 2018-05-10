import sys
import qdarkstyle
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QFontDatabase
from .MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)

    app.setFont(QFont('WenQuanYi Micro Hei Mono'))

    main_window = MainWindow()

    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    sys.exit(app.exec())

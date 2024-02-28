from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

import sys

from package_qt.handle_qt import HandleQt

if __name__ == '__main__':
    app = QApplication([])
    program = HandleQt()
    program.ui.show()
    sys.exit(app.exec_())

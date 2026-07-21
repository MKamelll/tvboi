from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSplitter,
    QListWidget,
    QStackedWidget,
)
from PySide6.QtCore import Qt
from dashboardwidget import DashboardWidget
from searchwidget import SearchWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("tvboi")
        self.resize(600, 400)

        self.splitter = QSplitter(orientation=Qt.Orientation.Horizontal)
        self.left_list = QListWidget()
        self.views = ["Dashboard", "Search"]
        self.left_list.addItems(self.views)
        self.splitter.addWidget(self.left_list)
        self.stack = QStackedWidget()
        self.splitter.addWidget(self.stack)
        self.splitter.setSizes([150, 450])

        self.dashboard_widget = DashboardWidget()
        self.stack.addWidget(self.dashboard_widget)

        self.search_widget = SearchWidget()
        self.stack.addWidget(self.search_widget)

        self.left_list.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.setCentralWidget(self.splitter)


if __name__ == "__main__":
    import sys

    app = QApplication()
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

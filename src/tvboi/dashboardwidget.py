from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class DashboardWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.main_layout = QVBoxLayout(self)
        self.label = QLabel("dashboard")
        self.main_layout.addWidget(self.label)

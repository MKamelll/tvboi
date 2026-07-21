from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QListWidget,
    QProgressBar,
    QMessageBox,
    QLabel,
    QListWidgetItem,
)
from PySide6.QtCore import QThread, Signal, Qt
from api.tmdb import api
from api.pydantic_models import Success, Failure, SearchResults, ShowBasic


class SearchWorker(QThread):
    result = Signal(int, list)
    error = Signal(int, str)

    def __init__(self, query: str) -> None:
        super().__init__()
        self.query = query

    def run(self) -> None:
        res = api.search_for_show(self.query)
        match res:
            case Success(data=SearchResults(page=page, results=results)):
                self.result.emit(page, results)
            case Failure(status_code=code, status_message=msg):
                self.error.emit(code, msg)


class SearchResultWidget(QWidget):
    def __init__(self, show: ShowBasic, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.main_layout = QVBoxLayout(self)
        self.name_label = QLabel(show.name)
        self.air_year_label = QLabel(show.first_air_date or "N/A")
        self.overview_label = QLabel(show.overview or "N/A")
        self.overview_label.setWordWrap(True)
        self.main_layout.addWidget(self.name_label)
        self.main_layout.addWidget(self.air_year_label)
        self.main_layout.addWidget(self.overview_label)


class SearchWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.main_layout = QVBoxLayout(self)
        self.search_bar = QLineEdit(placeholderText="search...")
        self.search_bar.returnPressed.connect(self.on_return_pressed)
        self.shows_list = QListWidget()
        self.shows_list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.hide()
        self.main_layout.addWidget(self.search_bar)
        self.main_layout.addWidget(self.shows_list)
        self.main_layout.addWidget(self.progress_bar)

    def on_return_pressed(self) -> None:
        query = self.search_bar.text()
        self.worker = SearchWorker(query)
        self.worker.started.connect(self.progress_bar.show)
        self.worker.finished.connect(self.progress_bar.hide)
        self.worker.result.connect(self.on_result)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_result(self, page: int, shows: list[ShowBasic]) -> None:
        for show in shows:
            widget = SearchResultWidget(show)
            item = QListWidgetItem(self.shows_list)
            item.setSizeHint(widget.sizeHint())
            self.shows_list.setItemWidget(item, widget)

    def on_error(self, code: int, msg: str) -> None:
        QMessageBox.warning(self, "Search Failed", f"code: {code}, {msg}")

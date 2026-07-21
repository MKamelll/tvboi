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
from api.pydantic_models import Success, Failure, SearchResults, ShowBasic, Show
from showdetailswidget import ShowDetailsWidget


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


class ShowDetailsWorker(QThread):
    result = Signal(Show)
    error = Signal(int, str)

    def __init__(self, show: ShowBasic) -> None:
        super().__init__()
        self.tv_show = show

    def run(self) -> None:
        res = api.get_show_details(self.tv_show.id)
        match res:
            case Success(data=show):
                self.result.emit(show)
            case Failure(status_code=code, status_message=msg):
                self.error.emit(code, msg)


class SearchResultWidget(QWidget):
    def __init__(self, show: ShowBasic, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.tv_show = show
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
        self.shows_list.itemDoubleClicked.connect(self.on_item_double_click)
        self.shows_list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.hide()
        self.main_layout.addWidget(self.search_bar)
        self.main_layout.addWidget(self.shows_list)
        self.main_layout.addWidget(self.progress_bar)

    def on_item_double_click(self, item: QListWidgetItem) -> None:
        widget = self.shows_list.itemWidget(item)
        if widget is None:
            return
        if isinstance(widget, SearchResultWidget):
            self.details_worker = ShowDetailsWorker(widget.tv_show)
            self.details_worker.started.connect(self.progress_bar.show)
            self.details_worker.finished.connect(self.progress_bar.hide)
            self.details_worker.result.connect(self.on_details_result)
            self.details_worker.error.connect(self.on_details_error)
            self.details_worker.start()

    def on_details_result(self, show: Show) -> None:
        show_details_window = ShowDetailsWidget(show, self)
        show_details_window.setWindowFlag(Qt.WindowType.Window)
        show_details_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        show_details_window.show()

    def on_details_error(self, code: int, msg: str) -> None:
        QMessageBox.warning(self, "Details Request Failed", f"code: {code}, {msg}")

    def on_return_pressed(self) -> None:
        query = self.search_bar.text()
        self.search_worker = SearchWorker(query)
        self.search_worker.started.connect(self.progress_bar.show)
        self.search_worker.finished.connect(self.progress_bar.hide)
        self.search_worker.result.connect(self.on_search_result)
        self.search_worker.error.connect(self.on_search_error)
        self.search_worker.start()

    def on_search_result(self, page: int, shows: list[ShowBasic]) -> None:
        for show in shows:
            widget = SearchResultWidget(show)
            item = QListWidgetItem(self.shows_list)
            item.setSizeHint(widget.sizeHint())
            self.shows_list.setItemWidget(item, widget)

    def on_search_error(self, code: int, msg: str) -> None:
        QMessageBox.warning(self, "Search Failed", f"code: {code}, {msg}")

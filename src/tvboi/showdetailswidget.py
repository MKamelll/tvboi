from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QListWidget,
    QProgressBar,
    QMessageBox,
    QLabel,
    QListWidgetItem,
    QGroupBox,
    QScrollArea,
)

from PySide6.QtCore import QThread, Signal, Qt
from api.pydantic_models import ShowBasic, Show, Success, Failure
from api.tmdb import api


class InfoGroupWidget(QGroupBox):
    def __init__(
        self, title: str, body: str, wrap: bool = False, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent=parent, title=title)
        layout = QVBoxLayout(self)
        label = QLabel(body)
        label.setWordWrap(wrap)
        layout.addWidget(label)


class ShowInfoWidget(QWidget):
    def __init__(self, show: Show, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.tv_show = show
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.title_gp = InfoGroupWidget("Title", self.tv_show.name)
        self.year_gp = InfoGroupWidget("Year", self.tv_show.first_air_date)
        self.origin_country_gp = InfoGroupWidget(
            "Origin Country", ",".join(self.tv_show.origin_country)
        )
        self.original_language_gp = InfoGroupWidget(
            "Original Language", self.tv_show.original_language
        )
        self.overview_gp = InfoGroupWidget("Overview", self.tv_show.overview, wrap=True)
        self.vote_averge_gp = InfoGroupWidget(
            "Vote Average", f"{self.tv_show.vote_average:.1f}/10"
        )
        self.number_of_seasons_gp = InfoGroupWidget(
            "Number Of Seasons", str(self.tv_show.number_of_seasons)
        )
        self.number_of_episodes_gp = InfoGroupWidget(
            "Number Of Episodes", str(self.tv_show.number_of_episodes)
        )
        self.main_layout.addWidget(self.title_gp)
        self.main_layout.addWidget(self.year_gp)
        self.main_layout.addWidget(self.origin_country_gp)
        self.main_layout.addWidget(self.original_language_gp)
        self.main_layout.addWidget(self.overview_gp)
        self.main_layout.addWidget(self.vote_averge_gp)
        self.main_layout.addWidget(self.number_of_seasons_gp)
        self.main_layout.addWidget(self.number_of_episodes_gp)


class ShowDetailsWidget(QWidget):
    def __init__(self, show: Show, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.tv_show = show
        self.setWindowTitle(self.tv_show.name)
        self.resize(600, 400)
        self.main_layout = QVBoxLayout(self)
        self.info_widget = ShowInfoWidget(self.tv_show)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.info_widget)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

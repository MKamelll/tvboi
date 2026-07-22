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
    QSplitter,
    QTabWidget,
)

from PySide6.QtCore import QThread, Signal, Qt
from api.pydantic_models import ShowBasic, Show, Success, Failure, SeasonBasic
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
        self.splitter = QSplitter(orientation=Qt.Orientation.Horizontal)

        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)
        self.title_gp = InfoGroupWidget("Title", self.tv_show.name)
        self.year_gp = InfoGroupWidget("Year", self.tv_show.first_air_date)
        self.origin_country_gp = InfoGroupWidget(
            "Origin Country", ",".join(self.tv_show.origin_country)
        )
        self.original_language_gp = InfoGroupWidget(
            "Original Language", self.tv_show.original_language
        )
        self.vote_averge_gp = InfoGroupWidget(
            "Vote Average", f"{self.tv_show.vote_average:.1f}/10"
        )
        self.number_of_seasons_gp = InfoGroupWidget(
            "Number Of Seasons", str(self.tv_show.number_of_seasons)
        )
        self.number_of_episodes_gp = InfoGroupWidget(
            "Number Of Episodes", str(self.tv_show.number_of_episodes)
        )
        self.left_layout.addWidget(self.title_gp)
        self.left_layout.addWidget(self.year_gp)
        self.left_layout.addWidget(self.origin_country_gp)
        self.left_layout.addWidget(self.original_language_gp)
        self.left_layout.addWidget(self.vote_averge_gp)
        self.left_layout.addWidget(self.number_of_seasons_gp)
        self.left_layout.addWidget(self.number_of_episodes_gp)
        self.left_scroll_area = QScrollArea(self)
        self.left_scroll_area.setWidget(self.left_widget)
        self.left_scroll_area.setWidgetResizable(True)
        self.splitter.addWidget(self.left_scroll_area)

        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)
        self.overview_gp = InfoGroupWidget("Overview", self.tv_show.overview, wrap=True)
        self.right_layout.addWidget(self.overview_gp)
        self.tab_widget = QTabWidget()
        self.specials_season: SeasonBasic | None = None
        for season in self.tv_show.seasons:
            if "specials" in season.name.lower():
                self.specials_season = season
                continue
            self.tab_widget.addTab(QLabel(season.name), season.name)
        if self.specials_season:
            self.tab_widget.addTab(
                QLabel(self.specials_season.name), self.specials_season.name
            )
        self.right_layout.addWidget(self.tab_widget)

        self.splitter.addWidget(self.right_widget)
        self.main_layout.addWidget(self.splitter)


class ShowDetailsWidget(QWidget):
    def __init__(self, show: Show, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.tv_show = show
        self.setWindowTitle(self.tv_show.name)
        self.resize(600, 400)
        self.main_layout = QVBoxLayout(self)
        self.info_widget = ShowInfoWidget(self.tv_show)
        self.main_layout.addWidget(self.info_widget)

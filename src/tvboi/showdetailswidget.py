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
    QGridLayout,
    QPushButton,
)

from PySide6.QtCore import QThread, Signal, Qt
from api.pydantic_models import SeasonBasic, Episode, Show, Season  # type: ignore
from api.tmdb import api, TmdbException  # type: ignore


class InfoGroupWidget(QGroupBox):
    def __init__(
        self, title: str, body: str, wrap: bool = False, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent=parent, title=title)
        layout = QVBoxLayout(self)
        label = QLabel(body)
        label.setWordWrap(wrap)
        layout.addWidget(label)


class SeasonTabEpisodeWidget(QWidget):
    def __init__(self, episode: Episode, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.episode = episode
        self.grid = QGridLayout(self)
        self.grid.addWidget(
            QLabel(f"Episode {episode.episode_number}: {episode.name}"), 0, 0, 1, 2
        )
        overview_label = QLabel(episode.overview)
        overview_label.setWordWrap(True)
        self.grid.addWidget(overview_label, 1, 0, 3, 3)
        self.watch_status_toggle = QPushButton("Mark Episode")
        self.watch_status_toggle.setCheckable(True)
        self.watch_status_toggle.toggled.connect(self.on_watch_status_toggle)
        self.watch_status_toggle.setStyleSheet(
            r"QPushButton:checked {background-color: green; }"
        )
        self.grid.addWidget(self.watch_status_toggle, 0, 2, 1, 1)

    def on_watch_status_toggle(self, checked: bool) -> None:
        if checked:
            self.watch_status_toggle.setText("Episode Marked")
        else:
            self.watch_status_toggle.setText("Mark Episode")

    def toggle_watch_status(self, checked: bool) -> None:
        self.watch_status_toggle.setChecked(checked)


class SeasonTabEpisodeListWidget(QWidget):
    def __init__(
        self, show_id: int, season_number: int, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent=parent)
        self.show_id = show_id
        self.season_number = season_number
        self.vbox = QVBoxLayout(self)
        self.season_watch_status_toggle = QPushButton("Mark Whole Season")
        self.season_watch_status_toggle.setCheckable(True)
        self.season_watch_status_toggle.setStyleSheet(
            r"QPushButton:checked {background-color: green; }"
        )
        self.season_watch_status_toggle.toggled.connect(
            self.on_season_watch_status_toggle
        )
        self.episode_list = QListWidget(self)
        self.vbox.addWidget(self.season_watch_status_toggle)
        self.vbox.addWidget(self.episode_list)

    def on_season_watch_status_toggle(self, checked: bool) -> None:
        if checked:
            self.season_watch_status_toggle.setText("Season Marked")
        else:
            self.season_watch_status_toggle.setText("Mark Season")
        self.toggle_all_episodes(checked=checked)

    def toggle_all_episodes(self, checked: bool) -> None:
        for i in range(self.episode_list.count()):
            item = self.episode_list.item(i)
            widget = self.episode_list.itemWidget(item)
            if isinstance(widget, SeasonTabEpisodeWidget):
                widget.toggle_watch_status(checked=checked)

    def load(self) -> None:
        if self.episode_list.count() > 0:
            return
        self.episodes_worker = SeasonEpisodesWorker(self.show_id, self.season_number)
        self.episodes_worker.result.connect(self.on_result)
        self.episodes_worker.error.connect(self.on_error)
        self.episodes_worker.start()

    def on_result(self, episodes: list[Episode]) -> None:
        for episode in episodes:
            item = QListWidgetItem(self.episode_list)
            episode_widget = SeasonTabEpisodeWidget(episode, self.episode_list)
            item.setSizeHint(episode_widget.sizeHint())
            self.episode_list.setItemWidget(item, episode_widget)

    def on_error(self, error: str) -> None:
        QMessageBox.warning(self, "Episodes Request Failed", error)


class SeasonEpisodesWorker(QThread):
    result = Signal(list)
    error = Signal(str)

    def __init__(self, show_id: int, season_number: int) -> None:
        super().__init__()
        self.show_id = show_id
        self.season_number = season_number

    def run(self) -> None:
        try:
            season = api.get_season_details(self.show_id, self.season_number)
            self.result.emit(season.episodes)
        except TmdbException as e:
            self.error.emit(str(e))


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
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        self.specials_season: SeasonBasic | None = None
        for season in self.tv_show.seasons:
            if "specials" in season.name.lower():
                self.specials_season = season
                continue
            self.tab_widget.addTab(
                SeasonTabEpisodeListWidget(
                    show_id=self.tv_show.id, season_number=season.season_number
                ),
                season.name,
            )
        if self.specials_season:
            self.tab_widget.addTab(
                SeasonTabEpisodeListWidget(
                    show_id=self.tv_show.id,
                    season_number=self.specials_season.season_number,
                ),
                self.specials_season.name,
            )
        self.right_layout.addWidget(self.tab_widget)

        self.splitter.addWidget(self.right_widget)
        self.main_layout.addWidget(self.splitter)

    def on_tab_changed(self, current_index: int) -> None:
        widget = self.tab_widget.widget(current_index)
        if not widget:
            return
        if isinstance(widget, SeasonTabEpisodeListWidget):
            widget.load()


class ShowDetailsWidget(QWidget):
    def __init__(self, show: Show, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.tv_show = show
        self.setWindowTitle(self.tv_show.name)
        self.resize(600, 400)
        self.main_layout = QVBoxLayout(self)
        self.info_widget = ShowInfoWidget(self.tv_show)
        self.main_layout.addWidget(self.info_widget)

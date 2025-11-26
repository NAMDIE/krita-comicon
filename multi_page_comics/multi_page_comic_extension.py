from typing import Optional
from krita import Extension, Krita
from PyQt5.QtWidgets import QMessageBox
from .comic_manager import ComicProjectManager
from .ui.main_docker import MultiPageComicsDockerFactory, MultiPageComicsDocker


class MultiPageComicsExtension(Extension):
    """Main Krita Comic Creator Extension."""

    def __init__(self, parent):
        super().__init__(parent)
        self.project_manager = ComicProjectManager()
        self.docker_factory = None

    def setup(self) -> None:
        """Initialize the extension."""
        # Register and add the docker factory to Krita
        if not self.docker_factory:
            self.docker_factory = MultiPageComicsDockerFactory()
            Krita.instance().addDockWidgetFactory(self.docker_factory)

    def createActions(self, window) -> None:
        """Create menu actions.
        
        Args:
            window: Krita window instance
        """
        # New Comic Project
        action_new = window.createAction(
            "comic_creator_new_project",
            "New Comic Project",
            "file"
        )
        action_new.triggered.connect(lambda: self.new_project(Krita.instance().activeWindow()))

        # Open Comic Project
        action_open = window.createAction(
            "comic_creator_open_project",
            "Open Comic Project",
            "file"
        )
        action_open.triggered.connect(lambda: self.open_project(Krita.instance().activeWindow()))

        # Export Comic
        action_export = window.createAction(
            "comic_creator_export",
            "Export Comic",
            "file"
        )
        action_export.triggered.connect(lambda: self.export_comic(Krita.instance().activeWindow()))

        # Show Docker
        action_docker = window.createAction(
            "comic_creator_show_docker",
            "Comic Creator",
            "settings/dockers"
        )
        action_docker.triggered.connect(self.show_docker)

    def new_project(self, window) -> None:
        """Create new comic project.
        
        Args:
            window: Krita window instance
        """
        from .ui.preferences_dialog import NewProjectDialog
        dialog = NewProjectDialog(window.qwindow())
        if dialog.exec_():
            project_data = dialog.get_project_data()
            self.project_manager.create_project(project_data)
            docker = self._get_docker()
            if docker and docker.isVisible():
                docker.refresh_project()

    def open_project(self, window) -> None:
        """Open existing comic project.
        
        Args:
            window: Krita window instance
        """
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getOpenFileName(
            window.qwindow(),
            "Open Comic Project",
            "",
            "Krita Documents (*.kra)"
        )
        if filename:
            self.project_manager.load_project(filename)
            docker = self._get_docker()
            if docker and docker.isVisible():
                docker.refresh_project()

    def export_comic(self, window) -> None:
        """Export comic pages.
        
        Args:
            window: Krita window instance
        """
        from .ui.export_dialog import ExportDialog
        dialog = ExportDialog(self.project_manager, parent=window.qwindow())
        dialog.exec_()

    def _get_docker(self) -> Optional["MultiPageComicsDocker"]:
        """Get the docker instance if it exists.

        Returns:
            The docker instance or None
        """
        for widget in Krita.instance().dockers():
            if widget.objectName() == "multi_page_comics_docker":
                return widget
        return None

    def show_docker(self) -> None:
        """Show the main docker panel."""
        Krita.instance().action("docker_multi_page_comics_docker").trigger()


# The extension is registered in __init__.py

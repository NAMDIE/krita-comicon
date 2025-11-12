from typing import Optional
from krita import Extension, Krita
from PyQt5.QtWidgets import QMessageBox
from .comic_manager import ComicProjectManager
from .ui.main_docker import ComicCreatorDocker


class MultiPageComicsExtension(Extension):
    """Main Krita Comic Creator Extension."""

    def __init__(self, parent):
        super().__init__(parent)
        self.project_manager = ComicProjectManager()
        self.docker: Optional[ComicCreatorDocker] = None

    def setup(self) -> None:
        """Initialize the extension."""
        pass

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
            if self.docker:
                self.docker.refresh_project()

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
            if self.docker:
                self.docker.refresh_project()

    def export_comic(self, window) -> None:
        """Export comic pages.
        
        Args:
            window: Krita window instance
        """
        from .ui.export_dialog import ExportDialog
        dialog = ExportDialog(self.project_manager, parent=window.qwindow())
        dialog.exec_()

    def show_docker(self) -> None:
        """Show the main docker panel."""
        if not self.docker:
            self.docker = ComicCreatorDocker()
            Krita.instance().addDockWidgetFactory(
                self.docker
            )


# The extension is registered in __init__.py
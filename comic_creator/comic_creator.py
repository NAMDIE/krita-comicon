from krita import Extension, Krita
from PyQt5.QtWidgets import QMessageBox
from .comic_manager import ComicProjectManager
from .ui.main_docker import ComicCreatorDocker


class ComicCreator(Extension):
'''Main Krita Comic Creator Extension'''

def __init__(self, parent):
super().__init__(parent)
self.project_manager = ComicProjectManager()
self.docker = None

def setup(self):
'''Initialize the extension'''
pass

def createActions(self, window):
'''Create menu actions'''
# New Comic Project
action_new = window.createAction(
"comic_creator_new_project",
"New Comic Project",
"file"
)
action_new.triggered.connect(self.new_project)

# Open Comic Project
action_open = window.createAction(
"comic_creator_open_project",
"Open Comic Project",
"file"
)
action_open.triggered.connect(self.open_project)

# Export Comic
action_export = window.createAction(
"comic_creator_export",
"Export Comic",
"file"
)
action_export.triggered.connect(self.export_comic)

# Show Docker
action_docker = window.createAction(
"comic_creator_show_docker",
"Comic Creator",
"settings/dockers"
)
action_docker.triggered.connect(self.show_docker)

def new_project(self):
'''Create new comic project'''
from .ui.preferences_dialog import NewProjectDialog
dialog = NewProjectDialog()
if dialog.exec_():
project_data = dialog.get_project_data()
self.project_manager.create_project(project_data)
if self.docker:
self.docker.refresh_project()

def open_project(self):
'''Open existing comic project'''
from PyQt5.QtWidgets import QFileDialog
filename, _ = QFileDialog.getOpenFileName(
None,
"Open Comic Project",
"",
"Krita Documents (*.kra)"
)
if filename:
self.project_manager.load_project(filename)
if self.docker:
self.docker.refresh_project()

def export_comic(self):
'''Export comic pages'''
from .ui.export_dialog import ExportDialog
dialog = ExportDialog(self.project_manager)
dialog.exec_()

def show_docker(self):
'''Show the main docker panel'''
if not self.docker:
self.docker = ComicCreatorDocker()
Krita.instance().addDockWidgetFactory(
self.docker
)


# Register extension
Krita.instance().addExtension(ComicCreator(Krita.instance()))

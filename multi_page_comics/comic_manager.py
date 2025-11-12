import json
from pathlib import Path
from krita import Krita


class ComicProjectManager:
'''Manages comic project data and state'''

def __init__(self):
self.current_project = None
self.project_file = None

def create_project(self, project_data):
'''Create new comic project'''
self.current_project = {
'metadata': {
'title': project_data.get('title', 'Untitled Comic'),
'author': project_data.get('author', ''),
'series': project_data.get('series', ''),
'issue': project_data.get('issue', 1),
'format': project_data.get('format', 'us_standard'),
},
'settings': {
'page_width': project_data.get('page_width', 1988),
'page_height': project_data.get('page_height', 3056),
'dpi': project_data.get('dpi', 300),
'default_gutter': project_data.get('gutter', 12),
'default_margin': project_data.get('margin', 16),
},
'pages': []
}

# Create first page
self.add_page()

def add_page(self, template_id=None):
'''Add new page to project'''
if not self.current_project:
return None

from .page_manager import PageManager
page_manager = PageManager(self.current_project['settings'])
page_data = page_manager.create_page(template_id)

self.current_project['pages'].append(page_data)
return page_data

def get_page(self, page_index):
'''Get page data by index'''
if not self.current_project:
return None
if 0 <= page_index < len(self.current_project['pages']):
return self.current_project['pages'][page_index]
return None

def delete_page(self, page_index):
'''Delete page from project'''
if not self.current_project:
return False
if 0 <= page_index < len(self.current_project['pages']):
del self.current_project['pages'][page_index]
return True
return False

def save_project(self, filename=None):
'''Save project metadata to JSON'''
if filename:
self.project_file = filename

if not self.project_file or not self.current_project:
return False

# Save metadata in .kra file's annotation
doc = Krita.instance().activeDocument()
if doc:
project_json = json.dumps(self.current_project, indent=2)
doc.setAnnotation("MultiPageComicsProject",
project_json,
"application/json")
doc.save()
return True
return False

def load_project(self, filename):
'''Load project from .kra file'''
doc = Krita.instance().openDocument(filename)
if doc:
Krita.instance().activeWindow().addView(doc)
annotation = doc.annotation("MultiPageComicsProject")
if annotation:
self.current_project = json.loads(annotation)
self.project_file = filename
return True
return False

def get_project_stats(self):
'''Get project statistics'''
if not self.current_project:
return None

total_panels = sum(
len(page.get('panels', []))
for page in self.current_project['pages']
)

return {
'page_count': len(self.current_project['pages']),
'panel_count': total_panels,
'title': self.current_project['metadata']['title']
}

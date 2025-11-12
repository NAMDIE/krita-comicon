import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from krita import Krita
from .page_manager import PageManager


class ComicProjectManager:
    """Manages comic project data and state."""

    def __init__(self):
        self.current_project: Optional[Dict[str, Any]] = None
        self.project_file: Optional[str] = None

    def create_project(self, project_data: Dict[str, Any]) -> None:
        """Create new comic project.
        
        Args:
            project_data: Dictionary containing project metadata and settings
        """
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

    def add_page(self, template_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Add new page to project.
        
        Args:
            template_id: Optional template ID to apply
            
        Returns:
            Page data dictionary or None if no project
        """
        if not self.current_project:
            return None

        page_manager = PageManager(self.current_project['settings'])
        page_data = page_manager.create_page(template_id)

        self.current_project['pages'].append(page_data)
        return page_data

    def get_page(self, page_index: int) -> Optional[Dict[str, Any]]:
        """Get page data by index.
        
        Args:
            page_index: Index of page to retrieve
            
        Returns:
            Page data dictionary or None if not found
        """
        if not self.current_project:
            return None
        if 0 <= page_index < len(self.current_project['pages']):
            return self.current_project['pages'][page_index]
        return None

    def delete_page(self, page_index: int) -> bool:
        """Delete page from project.
        
        Args:
            page_index: Index of page to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        if not self.current_project:
            return False
        if 0 <= page_index < len(self.current_project['pages']):
            del self.current_project['pages'][page_index]
            return True
        return False

    def save_project(self, filename: Optional[str] = None) -> bool:
        """Save project metadata to JSON.
        
        Args:
            filename: Optional new filename to save as
            
        Returns:
            True if save successful, False otherwise
        """
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

    def load_project(self, filename: str) -> bool:
        """Load project from .kra file.
        
        Args:
            filename: Path to .kra file
            
        Returns:
            True if load successful, False otherwise
        """
        doc = Krita.instance().openDocument(filename)
        if doc:
            Krita.instance().activeWindow().addView(doc)
            annotation = doc.annotation("MultiPageComicsProject")
            if annotation:
                try:
                    self.current_project = json.loads(annotation)
                    self.project_file = filename
                    return True
                except json.JSONDecodeError:
                    return False
        return False

    def get_project_stats(self) -> Optional[Dict[str, Any]]:
        """Get project statistics.
        
        Returns:
            Dictionary with project statistics or None if no project
        """
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
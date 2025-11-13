import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional


logger = logging.getLogger(__name__)


class TemplateManager:
    """Manages panel layout templates."""

    def __init__(self):
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.load_default_templates()

    def load_default_templates(self) -> None:
        """Load built-in templates."""
        # Standard grids
        self.templates['2x3-standard'] = {
            'id': '2x3-standard',
            'name': '2×3 Standard Grid',
            'category': 'standard',
            'region': 'western',
            'panels': [
                {'x': 0, 'y': 0, 'width': 50, 'height': 33.33},
                {'x': 50, 'y': 0, 'width': 50, 'height': 33.33},
                {'x': 0, 'y': 33.33, 'width': 50, 'height': 33.33},
                {'x': 50, 'y': 33.33, 'width': 50, 'height': 33.33},
                {'x': 0, 'y': 66.66, 'width': 50, 'height': 33.34},
                {'x': 50, 'y': 66.66, 'width': 50, 'height': 33.34},
            ]
        }

        self.templates['3x2-standard'] = {
            'id': '3x2-standard',
            'name': '3×2 Standard Grid',
            'category': 'standard',
            'region': 'western',
            'panels': [
                {'x': 0, 'y': 0, 'width': 33.33, 'height': 50},
                {'x': 33.33, 'y': 0, 'width': 33.33, 'height': 50},
                {'x': 66.66, 'y': 0, 'width': 33.34, 'height': 50},
                {'x': 0, 'y': 50, 'width': 33.33, 'height': 50},
                {'x': 33.33, 'y': 50, 'width': 33.33, 'height': 50},
                {'x': 66.66, 'y': 50, 'width': 33.34, 'height': 50},
            ]
        }

        self.templates['splash-page'] = {
            'id': 'splash-page',
            'name': 'Full Splash Page',
            'category': 'splash',
            'region': 'universal',
            'panels': [
                {'x': 0, 'y': 0, 'width': 100, 'height': 100}
            ]
        }

        self.templates['hero-moment'] = {
            'id': 'hero-moment',
            'name': 'Hero Moment',
            'category': 'action',
            'region': 'western',
            'panels': [
                {'x': 0, 'y': 0, 'width': 50, 'height': 25},
                {'x': 50, 'y': 0, 'width': 50, 'height': 25},
                {'x': 0, 'y': 25, 'width': 100, 'height': 50},  # Hero panel
                {'x': 0, 'y': 75, 'width': 50, 'height': 25},
                {'x': 50, 'y': 75, 'width': 50, 'height': 25},
            ]
        }

        self.templates['4-panel-strip'] = {
            'id': '4-panel-strip',
            'name': '4-Panel Horizontal Strip',
            'category': 'standard',
            'region': 'universal',
            'panels': [
                {'x': 0, 'y': 0, 'width': 25, 'height': 100},
                {'x': 25, 'y': 0, 'width': 25, 'height': 100},
                {'x': 50, 'y': 0, 'width': 25, 'height': 100},
                {'x': 75, 'y': 0, 'width': 25, 'height': 100},
            ]
        }

        # Manga layouts
        self.templates['manga-vertical'] = {
            'id': 'manga-vertical',
            'name': 'Manga Vertical Flow',
            'category': 'manga',
            'region': 'manga',
            'reading_direction': 'rtl',
            'panels': [
                {'x': 50, 'y': 0, 'width': 50, 'height': 30},
                {'x': 0, 'y': 0, 'width': 50, 'height': 30},
                {'x': 50, 'y': 30, 'width': 50, 'height': 40},
                {'x': 0, 'y': 30, 'width': 50, 'height': 40},
                {'x': 0, 'y': 70, 'width': 100, 'height': 30},
            ]
        }

        # Load user templates if they exist
        self.load_user_templates()

    def load_user_templates(self) -> None:
        """Load user-created templates."""
        user_template_path = Path.home() / '.krita' / 'comic_creator' / 'templates'
        if user_template_path.exists():
            for template_file in user_template_path.glob('*.json'):
                try:
                    with open(template_file, 'r') as f:
                        template = json.load(f)
                        self.templates[template['id']] = template
                except Exception as e:
                    logger.error(f"Error loading template {template_file}: {e}")

    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get template by ID.

        Args:
            template_id: Template identifier

        Returns:
            Template dictionary or None if not found
        """
        return self.templates.get(template_id)

    def get_templates_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all templates in category.

        Args:
            category: Template category name

        Returns:
            List of templates in category
        """
        return [t for t in self.templates.values() if t.get('category') == category]

    def save_template(self, template_data: Dict[str, Any]) -> bool:
        """Save user-created template.

        Args:
            template_data: Template data dictionary

        Returns:
            True if save successful, False otherwise
        """
        template_id = template_data.get('id')
        if not template_id:
            return False

        self.templates[template_id] = template_data

        # Save to file
        user_template_path = Path.home() / '.krita' / 'comic_creator' / 'templates'
        user_template_path.mkdir(parents=True, exist_ok=True)

        template_file = user_template_path / f"{template_id}.json"
        with open(template_file, 'w') as f:
            json.dump(template_data, f, indent=2)

        return True

    def delete_template(self, template_id: str) -> bool:
        """Delete user template.

        Args:
            template_id: Template identifier

        Returns:
            True if deletion successful, False otherwise
        """
        if template_id in self.templates:
            del self.templates[template_id]

        template_file = Path.home() / '.krita' / 'comic_creator' / 'templates' / f"{template_id}.json"
        if template_file.exists():
            template_file.unlink()
            return True
        return False

    def get_all_templates(self) -> List[Dict[str, Any]]:
        """Get all available templates.

        Returns:
            List of all templates
        """
        return list(self.templates.values())
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional


<<<<<<< HEAD
logger = logging.getLogger(__name__)


class TemplateManager:
    """Manages panel layout templates."""
=======
logger = logging.getLogger(__name__)
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
    def __init__(self):
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.load_default_templates()
=======
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
    def load_default_templates(self) -> None:
        """Load built-in templates."""
        # Standard grids
        self.templates['2x3-standard'] = {
            'id': '2x3-standard',
            'name': '2×3 Standard Grid',
            'category': 'standard',
            'region': 'western',
            'panels': [
                {'x': 0, 'y': 0, 'width': 50, 'height': 33.33},
                {'x': 50, 'y': 0, 'width': 50, 'height': 33.33},
                {'x': 0, 'y': 33.33, 'width': 50, 'height': 33.33},
                {'x': 50, 'y': 33.33, 'width': 50, 'height': 33.33},
                {'x': 0, 'y': 66.66, 'width': 50, 'height': 33.34},
                {'x': 50, 'y': 66.66, 'width': 50, 'height': 33.34},
            ]
        }
=======
class TemplateManager:
    """Manages panel layout templates."""
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
        self.templates['3x2-standard'] = {
            'id': '3x2-standard',
            'name': '3×2 Standard Grid',
            'category': 'standard',
            'region': 'western',
            'panels': [
                {'x': 0, 'y': 0, 'width': 33.33, 'height': 50},
                {'x': 33.33, 'y': 0, 'width': 33.33, 'height': 50},
                {'x': 66.66, 'y': 0, 'width': 33.34, 'height': 50},
                {'x': 0, 'y': 50, 'width': 33.33, 'height': 50},
                {'x': 33.33, 'y': 50, 'width': 33.33, 'height': 50},
                {'x': 66.66, 'y': 50, 'width': 33.34, 'height': 50},
            ]
        }
=======
    def __init__(self):
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.load_default_templates()
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
        self.templates['splash-page'] = {
            'id': 'splash-page',
            'name': 'Full Splash Page',
            'category': 'splash',
            'region': 'universal',
            'panels': [
                {'x': 0, 'y': 0, 'width': 100, 'height': 100}
            ]
        }
=======
    def load_default_templates(self) -> None:
        """Load built-in templates."""
        # Standard grids
        self.templates['2x3-standard'] = {
            'id': '2x3-standard',
            'name': '2×3 Standard Grid',
            'category': 'standard',
            'region': 'western',
            'panels': [
                {'x': 0, 'y': 0, 'width': 50, 'height': 33.33},
                {'x': 50, 'y': 0, 'width': 50, 'height': 33.33},
                {'x': 0, 'y': 33.33, 'width': 50, 'height': 33.33},
                {'x': 50, 'y': 33.33, 'width': 50, 'height': 33.33},
                {'x': 0, 'y': 66.66, 'width': 50, 'height': 33.34},
                {'x': 50, 'y': 66.66, 'width': 50, 'height': 33.34},
            ]
        }
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
        self.templates['hero-moment'] = {
            'id': 'hero-moment',
            'name': 'Hero Moment',
            'category': 'action',
            'region': 'western',
            'panels': [
                {'x': 0, 'y': 0, 'width': 50, 'height': 25},
                {'x': 50, 'y': 0, 'width': 50, 'height': 25},
                {'x': 0, 'y': 25, 'width': 100, 'height': 50},  # Hero panel
                {'x': 0, 'y': 75, 'width': 50, 'height': 25},
                {'x': 50, 'y': 75, 'width': 50, 'height': 25},
            ]
        }
=======
        self.templates['3x2-standard'] = {
            'id': '3x2-standard',
            'name': '3×2 Standard Grid',
            'category': 'standard',
            'region': 'western',
            'panels': [
                {'x': 0, 'y': 0, 'width': 33.33, 'height': 50},
                {'x': 33.33, 'y': 0, 'width': 33.33, 'height': 50},
                {'x': 66.66, 'y': 0, 'width': 33.34, 'height': 50},
                {'x': 0, 'y': 50, 'width': 33.33, 'height': 50},
                {'x': 33.33, 'y': 50, 'width': 33.33, 'height': 50},
                {'x': 66.66, 'y': 50, 'width': 33.34, 'height': 50},
            ]
        }
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
        self.templates['4-panel-strip'] = {
            'id': '4-panel-strip',
            'name': '4-Panel Horizontal Strip',
            'category': 'standard',
            'region': 'universal',
            'panels': [
                {'x': 0, 'y': 0, 'width': 25, 'height': 100},
                {'x': 25, 'y': 0, 'width': 25, 'height': 100},
                {'x': 50, 'y': 0, 'width': 25, 'height': 100},
                {'x': 75, 'y': 0, 'width': 25, 'height': 100},
            ]
        }
=======
        self.templates['splash-page'] = {
            'id': 'splash-page',
            'name': 'Full Splash Page',
            'category': 'splash',
            'region': 'universal',
            'panels': [
                {'x': 0, 'y': 0, 'width': 100, 'height': 100}
            ]
        }
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
        # Manga layouts
        self.templates['manga-vertical'] = {
            'id': 'manga-vertical',
            'name': 'Manga Vertical Flow',
            'category': 'manga',
            'region': 'manga',
            'reading_direction': 'rtl',
            'panels': [
                {'x': 50, 'y': 0, 'width': 50, 'height': 30},
                {'x': 0, 'y': 0, 'width': 50, 'height': 30},
                {'x': 50, 'y': 30, 'width': 50, 'height': 40},
                {'x': 0, 'y': 30, 'width': 50, 'height': 40},
                {'x': 0, 'y': 70, 'width': 100, 'height': 30},
            ]
        }
=======
        self.templates['hero-moment'] = {
            'id': 'hero-moment',
            'name': 'Hero Moment',
            'category': 'action',
            'region': 'western',
            'panels': [
                {'x': 0, 'y': 0, 'width': 50, 'height': 25},
                {'x': 50, 'y': 0, 'width': 50, 'height': 25},
                {'x': 0, 'y': 25, 'width': 100, 'height': 50},  # Hero panel
                {'x': 0, 'y': 75, 'width': 50, 'height': 25},
                {'x': 50, 'y': 75, 'width': 50, 'height': 25},
            ]
        }
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
        # Load user templates if they exist
        self.load_user_templates()
=======
        self.templates['4-panel-strip'] = {
            'id': '4-panel-strip',
            'name': '4-Panel Horizontal Strip',
            'category': 'standard',
            'region': 'universal',
            'panels': [
                {'x': 0, 'y': 0, 'width': 25, 'height': 100},
                {'x': 25, 'y': 0, 'width': 25, 'height': 100},
                {'x': 50, 'y': 0, 'width': 25, 'height': 100},
                {'x': 75, 'y': 0, 'width': 25, 'height': 100},
            ]
        }
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
    def load_user_templates(self) -> None:
        """Load user-created templates."""
        user_template_path = Path.home() / '.krita' / 'comic_creator' / 'templates'
        if user_template_path.exists():
            for template_file in user_template_path.glob('*.json'):
                try:
                    with open(template_file, 'r') as f:
                        template = json.load(f)
                        self.templates[template['id']] = template
                except Exception as e:
                    logger.error(f"Error loading template {template_file}: {e}")
=======
        # Manga layouts
        self.templates['manga-vertical'] = {
            'id': 'manga-vertical',
            'name': 'Manga Vertical Flow',
            'category': 'manga',
            'region': 'manga',
            'reading_direction': 'rtl',
            'panels': [
                {'x': 50, 'y': 0, 'width': 50, 'height': 30},
                {'x': 0, 'y': 0, 'width': 50, 'height': 30},
                {'x': 50, 'y': 30, 'width': 50, 'height': 40},
                {'x': 0, 'y': 30, 'width': 50, 'height': 40},
                {'x': 0, 'y': 70, 'width': 100, 'height': 30},
            ]
        }
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get template by ID.
        
        Args:
            template_id: Template identifier
            
        Returns:
            Template dictionary or None if not found
        """
        return self.templates.get(template_id)
=======
        # Load user templates if they exist
        self.load_user_templates()
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
    def get_templates_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all templates in category.
        
        Args:
            category: Template category name
            
        Returns:
            List of templates in category
        """
        return [t for t in self.templates.values()
                if t.get('category') == category]
=======
    def load_user_templates(self) -> None:
        """Load user-created templates."""
        user_template_path = Path.home() / '.krita' / 'comic_creator' / 'templates'
        if user_template_path.exists():
            for template_file in user_template_path.glob('*.json'):
                try:
                    with open(template_file, 'r') as f:
                        template = json.load(f)
                        self.templates[template['id']] = template
                except Exception as e:
                    logger.error(f"Error loading template {template_file}: {e}")
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
    def save_template(self, template_data: Dict[str, Any]) -> bool:
        """Save user-created template.
        
        Args:
            template_data: Template data dictionary
            
        Returns:
            True if save successful, False otherwise
        """
        template_id = template_data.get('id')
        if not template_id:
            return False
=======
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get template by ID.
        
        Args:
            template_id: Template identifier
            
        Returns:
            Template dictionary or None if not found
        """
        return self.templates.get(template_id)
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
        self.templates[template_id] = template_data
=======
    def get_templates_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all templates in category.
        
        Args:
            category: Template category name
            
        Returns:
            List of templates in category
        """
        return [t for t in self.templates.values()
                if t.get('category') == category]
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
        # Save to file
        user_template_path = Path.home() / '.krita' / 'comic_creator' / 'templates'
        user_template_path.mkdir(parents=True, exist_ok=True)
=======
    def save_template(self, template_data: Dict[str, Any]) -> bool:
        """Save user-created template.
        
        Args:
            template_data: Template data dictionary
            
        Returns:
            True if save successful, False otherwise
        """
        template_id = template_data.get('id')
        if not template_id:
            return False
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
        template_file = user_template_path / f"{template_id}.json"
        with open(template_file, 'w') as f:
            json.dump(template_data, f, indent=2)
=======
        self.templates[template_id] = template_data
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
        return True
=======
        # Save to file
        user_template_path = Path.home() / '.krita' / 'comic_creator' / 'templates'
        user_template_path.mkdir(parents=True, exist_ok=True)
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
    def delete_template(self, template_id: str) -> bool:
        """Delete user template.
        
        Args:
            template_id: Template identifier
            
        Returns:
            True if deletion successful, False otherwise
        """
        if template_id in self.templates:
            del self.templates[template_id]
=======
        template_file = user_template_path / f"{template_id}.json"
        with open(template_file, 'w') as f:
            json.dump(template_data, f, indent=2)
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
        template_file = Path.home() / '.krita' / 'comic_creator' / 'templates' / f"{template_id}.json"
        if template_file.exists():
            template_file.unlink()
            return True
        return False
=======
        return True
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

<<<<<<< HEAD
    def get_all_templates(self) -> List[Dict[str, Any]]:
        """Get all available templates.
        
        Returns:
            List of all templates
        """
        return list(self.templates.values())
=======
    def delete_template(self, template_id: str) -> bool:
        """Delete user template.
        
        Args:
            template_id: Template identifier
            
        Returns:
            True if deletion successful, False otherwise
        """
        if template_id in self.templates:
            del self.templates[template_id]
>>>>>>> 1375d439cb96bd84846c46cf56ea836bf5d26560

        template_file = Path.home() / '.krita' / 'comic_creator' / 'templates' / f"{template_id}.json"
        if template_file.exists():
            template_file.unlink()
            return True
        return False

    def get_all_templates(self) -> List[Dict[str, Any]]:
        """Get all available templates.
        
        Returns:
            List of all templates
        """
        return list(self.templates.values())
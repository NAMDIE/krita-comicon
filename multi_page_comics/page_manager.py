from typing import Optional, Dict, Any, List
from krita import Krita
from .panel_system import PanelSystem
from .template_manager import TemplateManager


class PageManager:
    """Manages individual comic pages."""

    def __init__(self, project_settings: Dict[str, Any]):
        self.settings = project_settings
        self.panel_system = PanelSystem()
        self.template_manager = TemplateManager()

    def create_page(self, template_id: Optional[str] = None) -> Dict[str, Any]:
        """Create new page with optional template.
        
        Args:
            template_id: Optional template ID to apply
            
        Returns:
            Page data dictionary
        """
        doc = Krita.instance().activeDocument()

        if not doc:
            # Create new document
            doc = Krita.instance().createDocument(
                self.settings['page_width'],
                self.settings['page_height'],
                "Comic Page",
                "RGBA",
                "U8",
                "",
                self.settings['dpi']
            )
            Krita.instance().activeWindow().addView(doc)

        # Create page data structure
        page_data = {
            'page_number': len(doc.topLevelNodes()),
            'template_id': template_id,
            'panels': [],
            'layers': []
        }

        # Create page group layer
        page_layer = doc.createGroupLayer(f"Page {page_data['page_number']}")
        doc.rootNode().addChildNode(page_layer, None)

        # Apply template if specified
        if template_id:
            template = self.template_manager.get_template(template_id)
            if template:
                page_data['panels'] = self.apply_template(
                    doc, page_layer, template
                )

        return page_data

    def apply_template(
        self,
        doc,
        page_layer,
        template: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Apply panel template to page.
        
        Args:
            doc: Krita document
            page_layer: Parent page layer
            template: Template dictionary
            
        Returns:
            List of created panel data dictionaries
        """
        panels = []

        for i, panel_def in enumerate(template['panels']):
            panel_data = self.panel_system.create_panel(
                doc,
                page_layer,
                panel_def,
                i + 1
            )
            panels.append(panel_data)

        return panels

    def add_panel_to_page(
        self,
        doc,
        page_layer,
        panel_definition: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add single panel to existing page.
        
        Args:
            doc: Krita document
            page_layer: Parent page layer
            panel_definition: Panel definition dictionary
            
        Returns:
            Panel data dictionary
        """
        panel_count = len([n for n in page_layer.childNodes()
                           if 'Panel' in n.name()])
        return self.panel_system.create_panel(
            doc,
            page_layer,
            panel_definition,
            panel_count + 1
        )
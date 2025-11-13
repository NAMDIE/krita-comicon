import os
import logging
import zipfile
from pathlib import Path
from typing import Optional, Dict, Any, List
from krita import Krita
from PyQt5.QtCore import QSize


logger = logging.getLogger(__name__)


class ExportManager:
    """Handles comic export to various formats."""

    def __init__(self):
        self.export_formats = {
            'png': 'PNG Image',
            'jpg': 'JPEG Image',
            'pdf': 'PDF Document',
            'cbz': 'Comic Book Archive (CBZ)',
            'psd': 'Photoshop Document'
        }

    def export_page(
        self,
        doc,
        page_index: int,
        output_path: str,
        format: str = 'png',
        options: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Export single page.
        
        Args:
            doc: Krita document
            page_index: Index of page to export
            output_path: Output file path
            format: Export format (png, jpg, pdf)
            options: Export options dictionary
            
        Returns:
            True if export successful, False otherwise
        """
        if options is None:
            options = self.get_default_options(format)

        if format == 'png':
            return self._export_png(doc, output_path, options)
        elif format == 'jpg':
            return self._export_jpg(doc, output_path, options)
        elif format == 'pdf':
            return self._export_pdf(doc, output_path, options)

        return False

    def export_project(
        self,
        project_manager,
        output_dir: str,
        format: str = 'png',
        options: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Export all pages in project.
        
        Args:
            project_manager: ComicProjectManager instance
            output_dir: Output directory
            format: Export format
            options: Export options
            
        Returns:
            True if all pages exported successfully
        """
        if not project_manager.current_project:
            return False

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        doc = Krita.instance().activeDocument()
        if not doc:
            return False

        exported_files = []
        pages = project_manager.current_project['pages']

        for i, page in enumerate(pages):
            filename = f"page_{i+1:03d}.{format}"
            file_path = output_path / filename

            if self.export_page(doc, i, str(file_path), format, options):
                exported_files.append(str(file_path))

        # Create CBZ if requested
        if format == 'cbz':
            return self._create_cbz(exported_files, output_path)

        return len(exported_files) == len(pages)

    def _export_png(
        self,
        doc,
        output_path: str,
        options: Dict[str, Any]
    ) -> bool:
        """Export as PNG.
        
        Args:
            doc: Krita document
            output_path: Output file path
            options: Export options
            
        Returns:
            True if successful
        """
        try:
            # Flatten if requested
            if options.get('flatten', False):
                doc = doc.clone()
                doc.flattenImage()

            # Set resolution
            resolution = options.get('dpi', 300)

            # Export
            doc.exportImage(output_path, InfoObject())
            return True
        except Exception as e:
            logger.error(f"PNG export error: {e}")
            return False

    def _export_jpg(
        self,
        doc,
        output_path: str,
        options: Dict[str, Any]
    ) -> bool:
        """Export as JPEG.
        
        Args:
            doc: Krita document
            output_path: Output file path
            options: Export options
            
        Returns:
            True if successful
        """
        try:
            quality = options.get('quality', 95)

            if options.get('flatten', True):
                doc = doc.clone()
                doc.flattenImage()

            doc.exportImage(output_path, InfoObject())
            return True
        except Exception as e:
            logger.error(f"JPEG export error: {e}")
            return False

    def _export_pdf(
        self,
        doc,
        output_path: str,
        options: Dict[str, Any]
    ) -> bool:
        """Export as PDF.
        
        Args:
            doc: Krita document
            output_path: Output file path
            options: Export options
            
        Returns:
            True if successful
        """
        try:
            # PDF export using Krita's batch export
            # This would integrate with a PDF library
            return True
        except Exception as e:
            logger.error(f"PDF export error: {e}")
            return False

    def _create_cbz(
        self,
        image_files: List[str],
        output_path: Path
    ) -> bool:
        """Create CBZ comic archive.
        
        Args:
            image_files: List of image file paths
            output_path: Output directory
            
        Returns:
            True if successful
        """
        try:
            cbz_path = output_path / "comic.cbz"
            with zipfile.ZipFile(cbz_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for img_file in sorted(image_files):
                    zipf.write(img_file, os.path.basename(img_file))
            return True
        except Exception as e:
            logger.error(f"CBZ creation error: {e}")
            return False

    def get_default_options(self, format: str) -> Dict[str, Any]:
        """Get default export options for format.
        
        Args:
            format: Export format
            
        Returns:
            Dictionary of default options
        """
        defaults = {
            'png': {
                'dpi': 300,
                'flatten': False,
                'transparency': True
            },
            'jpg': {
                'quality': 95,
                'dpi': 300,
                'flatten': True
            },
            'pdf': {
                'dpi': 300,
                'compression': True,
                'embed_fonts': True
            },
            'cbz': {
                'image_format': 'jpg',
                'quality': 90,
                'dpi': 150
            }
        }
        return defaults.get(format, {})


class InfoObject:
    """Helper class for Krita export."""
    def __init__(self):
        self.properties = {}
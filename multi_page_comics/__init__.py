from .multi_page_comic_extension import MultiPageComicsExtension
from krita import Krita

# Krita extension entry point
Krita.instance().addExtension(MultiPageComicsExtension(Krita.instance()))

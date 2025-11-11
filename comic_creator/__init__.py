from .comic_creator import ComicCreator

# Krita extension entry point
Krita.instance().addExtension(ComicCreator(Krita.instance()))

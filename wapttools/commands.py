import sys
from .config import loadVersionCheck, loadControl
from .version import versionChecker

def commands(downloader=None):
    """ Default main function fo
    """
    if len(sys.argv) == 1:
        if downloader is not None:
            downloader()
    else:
        if sys.argv[1] == 'version-check':
            versionChecker(verbose=True)

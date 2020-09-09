import bs4
import json
import os
import re
import requests

def download(url, pathname, clean=True):
    """ Download the file at a given url and save it to pathname.

    The files existing in the same folder and with the same extension are removed if clean=True.

    Parameters
    ----------
    url: string
        url of the file to be dowloaded
    pathname: string
        pathname of the file to be saved
    clean: boolean
        cleanup needed
    """
    extension = os.path.splitext(pathname)[1]

    dirname = os.path.dirname(pathname)

    if clean:
        pattern = os.path.join(dirname, '*{}'.format(extension))
        print('* Removing all files {} except {}'.format(pattern, pathname))
        for file in glob.glob(pattern):
            if file != pathname:
                print('* Removing {}'.format(file))
                os.remove(file)

    print('* Downloading {} from {}'.format(os.path.basename(pathname), url))
    if not os.path.exists(pathname):
        try:
            r = requests.get(url, stream=True)
            with open(pathname, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            del r
        except Exception as e:
            print('=> Failed to download {}, {}'.format(os.path.basename(pathname), e))
    else:
        print('{} already downloaded'.format(pathname))

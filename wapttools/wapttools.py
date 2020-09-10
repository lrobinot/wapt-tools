import argparse
import sys
from .version import checker

"""wapttools.wapttools: provides entry point main()."""

__version__ = "0.1.0"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbosity', help='increase output verbosity', action='store_true')
    parser.add_argument('--version', help='display module version', action='store_true')
    parser.add_argument('--check', help='use local version-check.json & WAPT/control to do a version check', action='store_true')
    args = parser.parse_args()

    if args.version:
        print('wapttools cli v{}'.format(__version__))
        sys.exit(0)

    if args.check:
        mismatch = checker(verbose=True)
        if mismatch:
            sys.exit(1)
        else:
            sys.exit(0)

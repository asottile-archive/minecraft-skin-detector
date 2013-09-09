
from __future__ import print_function

import argparse
import sys

from fetch import get_player_skin
from skin_compare import has_changed

def main(argv):
    parser = argparse.ArgumentParser(
        description='Detect whether minecraft skins have changed.',
    )
    parser.add_argument(
        'usernames', type=str, nargs='+',
        help='Usernames to check for skin changes',
    )
    args = parser.parse_args(argv[1:])

    for username in args.usernames:
        user_skin = get_player_skin(username)
        if has_changed(username, user_skin):
            print('{0} has a new skin!'.format(username))

if __name__ == '__main__':
    main(sys.argv)

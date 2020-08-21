"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""

import sys
from eagleeye.eagleeye import EagleEye
from eagleeye.eagleeye import create_parser


if __name__ == '__main__':
    # Execute the parse_args() method
    ARGS = create_parser(sys.argv[1:])
    EAGLEEYEOBJ = EagleEye(ARGS.path)
    EAGLEEYEOBJ.eaglewatch()

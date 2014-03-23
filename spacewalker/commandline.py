#!/usr/bin/env python

from __future__ import print_function

import argparse
import logging
import os

from spacewalker import explore
from spacewalker.walkers import walkers


def main():
    parser = argparse.ArgumentParser(description='Search a space for a string.')
    parser.add_argument('needle', help='string to search for')
    parser.add_argument('--walker', '-w', default='pyrandom', choices=sorted(walkers.keys()),
                        help='spacewalker to search with')
    parser.add_argument('--num-procs', '-n', type=int, default=None,
                        help='number of processors to run on')
    parser.add_argument('--chunk-size', '-c', type=int, default=100000)
    parser.add_argument('--verbose', '-v', action='count')
    args = parser.parse_args()

    if args.verbose > 1:
        loglevel = logging.DEBUG
    elif args.verbose == 1:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING
    logging.basicConfig(level=loglevel)

    search = walkers[args.walker].search
    validate = walkers[args.walker].validate

    os.nice(20)
    params = explore(args.needle, search, args.num_procs, args.chunk_size)
    print('Matching params: {}'.format(params))
    print('Validation: {}'.format(
        ''.join(char for char, _ in zip(
            validate(**params),  # pylint: disable=W0142
            range(len(args.needle))))))

if __name__ == '__main__':
    main()

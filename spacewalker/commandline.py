#!/usr/bin/env python

import logging
import os
import sys

from . import explore
from .walkers import walkers


def main():
    logging.basicConfig(level=logging.DEBUG)

    mod = 'randomspace'

    search = walkers[mod].search
    validate = walkers[mod].validate

    os.nice(20)
    phrase = sys.argv[1]
    params = explore(phrase, search)
    print('Matching params: {}'.format(params))
    print('Validation: {}'.format(
        ''.join(char for char, _ in zip(validate(**params), range(len(phrase))))))

if __name__ == '__main__':
    main()

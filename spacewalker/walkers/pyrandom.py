#!/usr/bin/env python

import logging
import random


def validate(seedvalue, base, width):
    random.seed(seedvalue)
    while True:
        yield chr(base + random.randrange(width))


def search(worker_number, chunk_size, needle, in_queue, out_queue):
    my_name = 'random-searcher-%d' % worker_number
    log = logging.getLogger(my_name)

    base = min(ord(_) for _ in needle)
    width = max(ord(_) for _ in needle) - base + 1
    if worker_number == 0:
        log.info('base: %d', base)
        log.info('width: %d', width)
        log.info('estimated chunks: %d', (width - 1) ** len(needle) / chunk_size)

    nums = [ord(_) - base for _ in needle]
    for chunk_num in iter(in_queue.get, None):
        log.debug('starting chunk %d', chunk_num)
        for seedvalue in range(chunk_num * chunk_size, (chunk_num + 1) * chunk_size):
            random.seed(seedvalue)
            if all(random.randrange(width) == want for want in nums):
                goal = {
                    'seedvalue': seedvalue,
                    'base': base,
                    'width': width,
                }
                log.info('chunk %d, found %s', chunk_num, goal)
                out_queue.put((chunk_num, goal))
                break
        else:
            out_queue.put(False)

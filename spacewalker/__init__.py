#!/usr/bin/env python

from multiprocessing import Process, Queue, cpu_count


def explore(needle, function, proc_count=None, chunk_size=100000):
    results = []
    in_queue = Queue()
    out_queue = Queue()
    if proc_count is None:
        proc_count = cpu_count()

    def handle_result():
        result = in_queue.get()
        if result:
            results.append(result)
            return True

    procs = [Process(target=function,
                     args=(worker_number, chunk_size, needle, out_queue, in_queue))
             for worker_number in range(proc_count)]
    for proc in procs:
        proc.start()

    for chunk, _ in enumerate(procs):
        out_queue.put(chunk)

    chunk = proc_count
    while True:
        if handle_result():
            break

        chunk += 1
        out_queue.put(chunk)

    for proc in procs:
        out_queue.put(None)

    for _ in procs[1:]:
        handle_result()

    for proc in procs:
        proc.join()

    return sorted(results)[0][1]

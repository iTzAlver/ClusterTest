# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
# Import statements:
import ray
import time
import multiprocessing

ITER = 12
GLOBAL_SIZE = int(100000000)
RAY_HEAD_IP = '192.168.79.101'
RAY_HEAD_PORT = '10001'
RAY_ADDRESS = f'ray://{RAY_HEAD_IP}:{RAY_HEAD_PORT}'
# -----------------------------------------------------------


def main_test():
    """
    Tests the connection to the RAY CLUSTER.
    :return: Console logs.
    """
    # Single process.
    init_timestamp = time.perf_counter()
    for _ in range(ITER):
        wait(GLOBAL_SIZE)
    print(f'Time elapsed (single process): {time.perf_counter() - init_timestamp} seconds.')

    # Multiprocessing.
    init_timestamp_2 = time.perf_counter()
    q = []
    for _ in range(ITER):
        q_ = multiprocessing.Queue()
        p = multiprocessing.Process(target=wait, args=(GLOBAL_SIZE, q_,))
        p.start()
        q.append(q_)
    for _q in q:
        _q.get()
    print(f'Time elapsed (multiple process): {time.perf_counter() - init_timestamp_2} seconds.')

    # Multiprocessing ray.
    ts0 = time.perf_counter()
    ray.init(address=RAY_ADDRESS, runtime_env={'working_dir': '.'})
    diff = time.perf_counter() - ts0
    init_timestamp_3 = time.perf_counter()
    remote_wait = ray.remote(wait)
    futures = []
    for _ in range(ITER):
        futures.append(remote_wait.remote(GLOBAL_SIZE))
    ray.get(futures)
    ray.shutdown()
    print(f'Time elapsed (cluster process): {time.perf_counter() - init_timestamp_3} seconds. ({diff} seconds to init)')


def wait(size, queue=None):
    """
    Waits some empty iterations.
    :param size: Number of iterations.
    :param queue: Queue for putting a '1' to set the end of the process.
    :return:
    """
    for _ in range(size):
        pass
    if queue is not None:
        queue.put(1)
    return 1


if __name__ == '__main__':
    main_test()
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #

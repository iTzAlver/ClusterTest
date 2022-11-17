# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
# Import statements:
import ray
import multiprocessing
from ._worker import Miner
from .__special__ import __src_path__ as _package_path_
RAY_ADD = 'ray://192.168.79.101:10001'


# -----------------------------------------------------------
@ray.remote
def work(obj, args):
    return obj.work(args)


class RayMinerPool:
    def __init__(self, _info_: str, n_workers: int, chunk_size: int, dif: int):
        """
        This class creates a Miner pool to compute the hash of the given block.
        :param _info_: Block of information.
        :param n_workers: Number of workers in the pool.
        :param chunk_size: The size of the chunks inside the workers.
        :param dif: The difficulty of the blockchain.
        """
        if ray.is_initialized:
            print(f'[+] Warning: ray is already initialized.')
            ray.shutdown()
        ray.init(address=RAY_ADD, runtime_env={"working_dir": f"{_package_path_}"})
        print(f'[+] Miner Pool connected to {RAY_ADD}.')

        self.info = _info_
        self.workers = [Miner(_info_, dif=dif) for _ in range(n_workers)]
        self.chunk_size = int(chunk_size)

        self._chunk_pointer = 0
        self._futures = self.__init_process__()

    def __init_process__(self):
        futures = []
        chunk_pointer = self._chunk_pointer
        for worker in self.workers:
            fts = work.remote(worker, (chunk_pointer, chunk_pointer + self.chunk_size - 1))
            futures.append(fts)
            chunk_pointer += self.chunk_size
        return futures

    @staticmethod
    def __orchestrate__(qs: list[ray.ObjectRef], solution_q: multiprocessing.Queue):
        print('\t\t[-] Pre - Orchestrating.')
        somebody_finished = False
        while not somebody_finished:
            print('\t\t[-] Orchestrating.')
            q, nr = ray.wait(qs, num_returns=1)
            print(q)
            if q:
                print('\t[-] Somebody won.')
                somebody_finished = ray.get(q)
                if somebody_finished:
                    solution_q.put(somebody_finished)

    def check(self):
        """
        This method checks if there is a winner in the miner pool.
        :return: The winner of the miner pool, None if nobody found a solution.
        """
        winner = None
        q, nr = ray.wait(self._futures, num_returns=1)
        if q:
            winner = ray.get(q[0])
            if not winner:
                winner = None
        return winner

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for p in self._futures:
            ray.cancel(p)
        print(f'[+] Miner Pool disconnected from {RAY_ADD}.')
        ray.shutdown()
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #

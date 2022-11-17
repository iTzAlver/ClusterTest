# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
# Import statements:
import multiprocessing
from ._worker import Miner


# -----------------------------------------------------------
class MinerPool:
    def __init__(self, _info_: str, n_workers: int, chunk_size: int, dif: int):
        """
        This class creates a Miner pool to compute the hash of the given block.
        :param _info_: Block of information.
        :param n_workers: Number of workers in the pool.
        :param chunk_size: The size of the chunks inside the workers.
        :param dif: The difficulty of the blockchain.
        """
        self.info = _info_
        self.workers = [Miner(_info_, dif=dif) for _ in range(n_workers)]
        self.chunk_size = chunk_size

        self._chunk_pointer = 0
        self._p, self._q = self.__init_process__()

        self._orchestrator, self._orch_queue = self._orchestrate()

    def __init_process__(self):
        p = []
        q = []
        chunk_pointer = self._chunk_pointer
        for worker in self.workers:
            q.append(multiprocessing.Queue())
            p.append(multiprocessing.Process(target=worker.work,
                                             args=((chunk_pointer, chunk_pointer + self.chunk_size - 1), q[-1])))
            p[-1].start()
            chunk_pointer += self.chunk_size
        return p, q

    def _orchestrate(self):
        orch_queue = multiprocessing.Queue()
        orchestator = multiprocessing.Process(target=self.__orchestrate__, args=(self._q, orch_queue))
        orchestator.start()
        return orchestator, orch_queue

    @staticmethod
    def __orchestrate__(qs: list[multiprocessing.Queue], solution_q: multiprocessing.Queue):
        somebody_finished = False
        while not somebody_finished:
            for n_worker, q in enumerate(qs):
                if not q.empty():
                    somebody_finished = q.get()
                    if somebody_finished:
                        solution_q.put(somebody_finished)

    def check(self):
        """
        This method checks if there is a winner in the miner pool.
        :return: The winner of the miner pool, None if nobody found a solution.
        """
        winner = None
        if not self._orch_queue.empty():
            winner = self._orch_queue.get()
            for p in self._p:
                p.terminate()
        return winner
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #

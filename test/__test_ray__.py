# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
# Import statements:
import time
from src.blockchain import Miner, MinerPool, Sha256, RayMinerPool
inf_ = '\nWallet:0xe2903jf9jf094fj98 transferred 0.00234 TestCoins to Wallet:0x3f3dkr4fmi99f4n59\n' \
       'Wallet:0xfiervj9485h94zp0u transferred 1.32493 TestCoins to Wallet:0xeprkg405gfk9jf98d\n' \
       'Wallet:0x34fj934ufj4rf9ooo transferred NFT:0xeofk3r0pfk99 to Wallet:0x49f95gfn9gfu0u0u3\n' \
       'NEXT_BLOCK_DIF:6\n'


def test_chain(_info_, dif=8):
    """
    Tests the blockchain miner with the provided information without multiprocessing and using the hash method.
    :param _info_: Raw information.
    :param dif: Difficulty of the block.
    :return: Console logs.
    """
    tsi = time.perf_counter()
    print('[+] Connected to TestChain:')
    proof_of_work_blockchain = Miner(_info_, dif=dif)
    hash(proof_of_work_blockchain)
    public_info = proof_of_work_blockchain.block
    print(f'[-] Block: {public_info}.')
    print(f'{len(proof_of_work_blockchain.hash)} / {proof_of_work_blockchain.dif}')
    print(f'[-] Hash: {Sha256(proof_of_work_blockchain.block)} == {proof_of_work_blockchain.hash}')
    print(f'[-] Total time: {time.perf_counter() - tsi} seconds.')


def test_chain_work(_info_, dif=8):
    """
    Tests the blockchain miner with the provided information without multiprocessing and using the work method.
    :param _info_: Raw information.
    :param dif: Difficulty of the block.
    :return: Console logs.
    """
    tsi = time.perf_counter()
    print('[+] Connected to TestChain (Work):')
    proof_of_work_blockchain = Miner(_info_, dif=dif)
    proof_of_work_blockchain.work(chunk=(0, int(1e8)))
    public_info = proof_of_work_blockchain.block
    print(f'[-] Block: {public_info}.')
    print(f'[-] Rank: {len(proof_of_work_blockchain.hash)} / {proof_of_work_blockchain.dif}')
    print(f'[-] Hash: {Sha256(proof_of_work_blockchain.block)} == {proof_of_work_blockchain.hash}')
    print(f'[-] Total time: {time.perf_counter() - tsi} seconds.')


def test_chain_mp(_info_, dif: int = 8, n_workers: int = 12, chunk_size: int = 1e8):
    """
    Tests the blockchain miner with the provided information with multiprocessing.
    :param _info_: Raw information.
    :param dif: Difficulty of the block.
    :param n_workers: Number of workers in parallel.
    :param chunk_size: The size of the chunks where the miners try to find a solution.
    :return: Console logs.
    """
    tsi = time.perf_counter()
    print('[+] Connected to MP TestChain:')

    mp = MinerPool(_info_, n_workers, chunk_size, dif)
    winner = None
    while winner is None:
        time.sleep(0.1)
        winner = mp.check()

    print(winner)
    public_info = winner.block
    print(f'[-] Block: {public_info}.')
    print(f'[-] Rank: {len(winner.hash)} / {winner.dif}')
    print(f'[-] Hash: {Sha256(winner.block)} == {winner.hash}')

    diff = time.perf_counter() - tsi
    mh = 16 ** dif / 1000000
    mu = mh / diff
    print(f'[-] Total time: {diff} seconds.')
    print(f'[-] Average Hash: {mh} MH.')
    print(f'[-] Average performance: {mu} MH/s.')
    print(f'[-] Average performance per worker: {mu / n_workers} MH/(s·worker).')


def test_chain_ray(_info_, dif: int = 8, n_workers: int = 12, chunk_size: int = 1e8, computable_cpus: int = 36):
    """
    Tests the blockchain miner with the provided information with multiprocessing in the RAY CLUSTER.
    :param _info_: Raw information.
    :param dif: Difficulty of the block.
    :param n_workers: Number of workers in parallel working in the cluster.
    :param chunk_size: The size of the chunks where the miners try to find a solution.
    :return: Console logs.
    """
    tsi = time.perf_counter()
    print('\n[+] Connected to Ray TestChain:')
    with RayMinerPool(_info_, n_workers, chunk_size, dif) as mp:
        winner = None
        while winner is None:
            winner = mp.check()
        print(winner)
        public_info = winner.block
        print(f'[-] Block: {public_info}.')
        print(f'[-] Rank: {len(winner.hash)} / {winner.dif}')
        print(f'[-] Hash: {Sha256(winner.block)} == {winner.hash}')

        diff = time.perf_counter() - tsi
        mh = 16 ** dif / 1000000
        mu = mh / diff
        print(f'[-] Total time: {diff} seconds.')
        print(f'[-] Average Hash: {mh} MH.')
        print(f'[-] Average performance: {mu} MH/s.')
        print(f'[-] Average performance per worker: {mu / computable_cpus} MH/(s·worker).')


if __name__ == '__main__':
    # test_chain_work(inf_, dif=6)
    test_chain_mp(inf_, dif=8)
    # test_chain_ray(inf_, dif=8, n_workers=80)
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #

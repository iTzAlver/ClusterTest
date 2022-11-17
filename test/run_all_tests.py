# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
# Import statements:
import time
from __test_connection__ import main_test
from __test_ray__ import test_chain_ray, inf_


if __name__ == '__main__':
    print('[+][+][+] Testing main connection.')
    main_test()
    print('[+][+][+] Main connection worked.')
    time.sleep(1)
    print('[+][+][+] Testing blockchain on the cluster.')
    inic = time.perf_counter()
    diff = test_chain_ray(inf_, dif=8, n_workers=100)
    time.perf_counter() - inic
    time.sleep(1)
    print(f'[+][+][+] Blockchain finished in {diff} seconds.')
    print('[+][+][+] All tests passed.')
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #

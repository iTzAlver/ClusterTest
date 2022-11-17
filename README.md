# Cluster usage: Test your RAY computing cluster. Python 3.10.8.

<p align="center">
    <img src="https://github.com/iTzAlver/ClusterTest/blob/main/multimedia/cluster.png">
</p>

<p align="center">
    <a href="https://github.com/iTzAlver/ClusterTest/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/iTzAlver/basenet_api?color=purple&style=plastic" /></a>
    <a href="https://github.com/iTzAlver/ClusterTest/blob/main/test/run_all_tests.py">
        <img src="https://img.shields.io/badge/tests-passed-green?color=green&style=plastic" /></a>
    <a href="https://github.com/iTzAlver/ClusterTest/blob/main/requirements.txt">
        <img src="https://img.shields.io/badge/requirements-ray-red?color=blue&style=plastic" /></a>
    <a href="https://docs.ray.io/en/latest/">
        <img src="https://img.shields.io/badge/doc-from ray-green?color=yellow&style=plastic" /></a>
</p>

<p align="center">
    <a href="https://www.ray.io/">
        <img src="https://img.shields.io/badge/dependencies-ray-red?color=blue&style=for-the-badge" /></a>
</p>

# Blockchain test script.

The Blockchain package implements a PoW Blockchain. The Blockchain is a great system to test the computing 
capability of a computer. The Blockchain is not implemented as a conventional blockchain, but the miner pools are 
implemented as a test script. The longer it takes to find a solution, the worse is the computing capability 
of the cluster.

## About ##

    Author: A.Palomo-Alonso (a.palomo@uah.es)
    Universidad de Alcalá.
    Escuela Politécnica Superior.
    Departamento de Teoría De la Señal y Comunicaciones (TDSC).
    ISDEFE Chair of Research.

## Explanation

The PoW consists in computing a valid hash of your piece of information. The valid hash starts with ``dif`` (blockchain 
parameter) 0's. Your piece of information is composed by 2 main parts: **the preamble** and the 
**raw block information**. 

The preamble is a number selected by the miner (the computing device looking for a valid 
hash). I.e: ``1029384458``.

When adding different preambles to the raw information (which is immutable) the hash differs. The miner will try
to find a valid hash (starting with ``dif`` zeros) by using **brute force**. There are no algorithms to search a valid 
hash quickly.

The more computing capability has the cluster, the more chances it has to find a solution quickly. The time it takes
scales exponentially with the ``dif`` parameter ``O(16^dif)`` as the zeros are found in hexadecimal basis.

The miner (worker) will try to find a valid hash cooperating with the other miners, when a miner finds the valid hash,
all the miners stop, and they raise the solution to the blockchain; which is not implemented in this test script, as it
is not needed.

In order to coordinate the miners, the preamble is different for each miner, so two miners will not try to look for a valid hash 
same preamble. The range of numbers that a miner is allowed to find a valid hash is called **chunk**. The script 
generates the chunks automatically, but the user must tell the miner pool the chunk size.

## Using ray

To use ray you must have the same Python version as the cluster. In this case: ``python 3.10.8``. To connect with the 
cluster you can call the ``init`` function:

    import ray

    ray.init(address='192.168.1.100:10001')

The address is the RAY IP address of the master server. The port is ``10001`` by default.

You must always try to shut down ray every time it is initialized. I recommend you to create a ``conext manager`` 
for your class; so in case an exception or interruption is generated, the session is properly closed.

    class MyRayActor:
        def __init__(self, *args, **kwargs):
            ray.init(address='192.168.1.100:10001', runtime_env={'working_dir': '.'})
            print('[+]: Connected to RAY: 192.168.1.100:10001.')
            ...

        ...

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            ray.shutdown()
            print('[-]: Disconnected from RAY.')


    # Testing the context manager.
    with MyRayActor(args, kwargs) as my_ray_actor:
        assert 0 == 1 #  To raise an exception will close the session by calling __exit__()


To upload packages you must use ``runtime_env= :runtime_env``. Check ray documentation for using runtime environments.
Not using this feature properly will raise ``Data channel error`` in the cluster log.

To create a worker you can create a RAY remote function or adding a decorator to your function.

    improt ray

    def big_function(args):
        """"
        This function takes a lot of time.
        ...
        """"
        ...

    @ray.remote
    def remote_big_function(args):
        return big_function(args)

    remote_big_function_in_other_way = ray.remote(big_function)

To send the job to the cluster you must call the function with the ```.remote``` method.

    remote_big_function.remote(my_args)
    remote_big_function_in_other_way.remote(my_args)

Further explanations may be provided in the official RAY documentation.

## Testing

Run the ``run_all_tests.py`` scripts to check the RAY connection.

## What's new?

### < 1.0.0
1. Blockchain included.


### Cite as

Please, cite this library as:

    @misc{testblockchainalbertopalomo2022,
      title={Simple PoW Blockchain for testing computing clusters.},
      author={A. Palomo-Alonso},
      booktitle={PhD in TIC: Machine Learning and NLP.},
      year={2022}
    }

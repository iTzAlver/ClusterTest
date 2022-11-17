# Cluster usage: Test your RAY computing cluster.

<p align="center">
    <img src="">
</p>

<p align="center">
    <a href="https://github.com/iTzAlver/basenet_api/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/iTzAlver/basenet_api?color=purple&style=plastic" /></a>
    <a href="https://github.com/iTzAlver/basenet_api/tree/main/test">
        <img src="https://img.shields.io/badge/tests-passed-green?color=green&style=plastic" /></a>
    <a href="https://github.com/iTzAlver/basenet_api/blob/main/requirements.txt">
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

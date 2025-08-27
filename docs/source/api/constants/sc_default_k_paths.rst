.. _api_constants_SC_DEFAULT_K_PATHS:

************************************
wulfric.constants.SC_DEFAULT_K_PATHS
************************************

Default k-path for each variation of Bravais lattices.

Data are from [1]_

.. code-block:: python

    SC_DEFAULT_K_PATHS = {
        "CUB" : "GAMMA-X-M-GAMMA-R-X|M-R",
        "FCC" : "GAMMA-X-W-K-GAMMA-L-U-W-L-K|U-X",
        "BCC" : "GAMMA-H-N-GAMMA-P-H|P-N",
        "TET" : "GAMMA-X-M-GAMMA-Z-R-A-Z|X-R|M-A",
        "BCT1" : "GAMMA-X-M-GAMMA-Z-P-N-Z1-M|X-P",
        "BCT2" : "GAMMA-X-Y-SIGMA-GAMMA-Z-SIGMA1-N-P-Y1-Z|X-P",
        "ORC" : "GAMMA-X-S-Y-GAMMA-Z-U-R-T-Z|Y-T|U-X|S-R",
        "ORCF1" : "GAMMA-Y-T-Z-GAMMA-X-A1-Y|T-X1|X-A-Z|L-GAMMA",
        "ORCF2" : "GAMMA-Y-C-D-X-GAMMA-Z-D1-H-C|C1-Z|X-H1|H-Y|L-GAMMA",
        "ORCF3" : "GAMMA-Y-T-Z-GAMMA-X-A1-Y|X-A-Z|L-GAMMA",
        "ORCI" : "GAMMA-X-L-T-W-R-X1-Z-GAMMA-Y-S-W|L1-Y|Y1-Z",
        "ORCC" : "GAMMA-X-S-R-A-Z-GAMMA-Y-X1-A1-T-Y|Z-T",
        "HEX" : "GAMMA-M-K-GAMMA-A-L-H-A|L-M|K-H",
        "RHL1" : "GAMMA-L-B1|B-Z-GAMMA-X|Q-F-P1-Z|L-P",
        "RHL2" : "GAMMA-P-Z-Q-GAMMA-F-P1-Q1-L-Z",
        "MCL" : "GAMMA-Y-H-C-E-M1-A-X-H1|M-D-Z|Y-D",
        "MCLC1" : "GAMMA-Y-F-L-I|I1-Z-F1|Y-X1|X-GAMMA-N|M-GAMMA",
        "MCLC2" : "GAMMA-Y-F-L-I|I1-Z-F1|N-GAMMA-M",
        "MCLC3" : "GAMMA-Y-F-H-Z-I-F1|H1-Y1-X-GAMMA-N|M-GAMMA",
        "MCLC4" : "GAMMA-Y-F-H-Z-I|H1-Y1-X-GAMMA-N|M-GAMMA",
        "MCLC5" : "GAMMA-Y-F-L-I|I1-Z-H-F1|H1-Y1-X-GAMMA-N|M-GAMMA",
        "TRI1a" : "X-GAMMA-Y|L-GAMMA-Z|N-GAMMA-M|R-GAMMA",
        "TRI1b" : "X-GAMMA-Y|L-GAMMA-Z|N-GAMMA-M|R-GAMMA",
        "TRI2a" : "X-GAMMA-Y|L-GAMMA-Z|N-GAMMA-M|R-GAMMA",
        "TRI2b" : "X-GAMMA-Y|L-GAMMA-Z|N-GAMMA-M|R-GAMMA",
    }


References
==========
.. [1] Setyawan, W. and Curtarolo, S., 2010.
       High-throughput electronic band structure calculations: Challenges and tools.
       Computational materials science, 49(2), pp. 299-312.

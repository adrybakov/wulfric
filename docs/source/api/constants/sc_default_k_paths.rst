.. _api_constants_SC_DEFAULT_K_PATHS:

************************************
wulfric.constants.SC_DEFAULT_K_PATHS
************************************

Default k-path for each variation of Bravais lattices.

Data are from [1]_

.. code-block:: python

    SC_DEFAULT_K_PATHS = {
        "CUB" : "G-X-M-G-R-X|M-R",
        "FCC" : "G-X-W-K-G-L-U-W-L-K|U-X",
        "BCC" : "G-H-N-G-P-H|P-N",
        "TET" : "G-X-M-G-Z-R-A-Z|X-R|M-A",
        "BCT1" : "G-X-M-G-Z-P-N-Z1-M|X-P",
        "BCT2" : "G-X-Y-S-G-Z-S1-N-P-Y1-Z|X-P",
        "ORC" : "G-X-S-Y-G-Z-U-R-T-Z|Y-T|U-X|S-R",
        "ORCF1" : "G-Y-T-Z-G-X-A1-Y|T-X1|X-A-Z|L-G",
        "ORCF2" : "G-Y-C-D-X-G-Z-D1-H-C|C1-Z|X-H1|H-Y|L-G",
        "ORCF3" : "G-Y-T-Z-G-X-A1-Y|X-A-Z|L-G",
        "ORCI" : "G-X-L-T-W-R-X1-Z-G-Y-S-W|L1-Y|Y1-Z",
        "ORCC" : "G-X-S-R-A-Z-G-Y-X1-A1-T-Y|Z-T",
        "HEX" : "G-M-K-G-A-L-H-A|L-M|K-H",
        "RHL1" : "G-L-B1|B-Z-G-X|Q-F-P1-Z|L-P",
        "RHL2" : "G-P-Z-Q-G-F-P1-Q1-L-Z",
        "MCL" : "G-Y-H-C-E-M1-A-X-H1|M-D-Z|Y-D",
        "MCLC1" : "G-Y-F-L-I|I1-Z-F1|Y-X1|X-G-N|M-G",
        "MCLC2" : "G-Y-F-L-I|I1-Z-F1|N-G-M",
        "MCLC3" : "G-Y-F-H-Z-I-F1|H1-Y1-X-G-N|M-G",
        "MCLC4" : "G-Y-F-H-Z-I|H1-Y1-X-G-N|M-G",
        "MCLC5" : "G-Y-F-L-I|I1-Z-H-F1|H1-Y1-X-G-N|M-G",
        "TRI1a" : "X-G-Y|L-G-Z|N-G-M|R-G",
        "TRI1b" : "X-G-Y|L-G-Z|N-G-M|R-G",
        "TRI2a" : "X-G-Y|L-G-Z|N-G-M|R-G",
        "TRI2b" : "X-G-Y|L-G-Z|N-G-M|R-G",
    }


References
==========
.. [1] Setyawan, W. and Curtarolo, S., 2010.
       High-throughput electronic band structure calculations: Challenges and tools.
       Computational materials science, 49(2), pp. 299-312.

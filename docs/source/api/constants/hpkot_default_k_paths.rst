.. _api_constants_HPKOT_DEFAULT_K_PATHS:

***************************************
wulfric.constants.HPKOT_DEFAULT_K_PATHS
***************************************

Default k-path for each extended Bravais lattice symbols.

Data are from [1]_

.. code-block:: python

    HPKOT_DEFAULT_K_PATHS = {
        "cP1" : "GAMMA-X-M-GAMMA-R-X|R-M-X1",
        "cP2" : "GAMMA-X-M-GAMMA-R-X|R-M",
        "cF1" : "GAMMA-X-U|K-GAMMA-L-W-X-W2",
        "cF2" : "GAMMA-X-U|K-GAMMA-L-W-X",
        "cI1" : "GAMMA-H-N-GAMMA-P-H|P-N",
        "tP1" : "GAMMA-X-M-GAMMA-Z-R-A-Z|X-R|M-A",
        "tI1" : "GAMMA-X-M-GAMMA-Z|Z0-M|X-P-N-GAMMA",
        "tI2" : "GAMMA-X-P-N-GAMMA-M-S|S0-GAMMA|X-R|G-M",
        "oP1" : "GAMMA-X-S-Y-GAMMA-Z-U-R-T-Z|X-U|Y-T|S-R",
        "oF1" : "GAMMA-Y-T-Z-GAMMA-SIGMA0|U0-T|Y-C0|A0-Z|GAMMA-L",
        "oF2" : "GAMMA-T-Z-Y-GAMMA-LAMBDA0|Q0-Z|T-G0|H0-Y|GAMMA-L",
        "oF3" : "GAMMA-Y-C0|A0-Z-B0|D0-T-G0|H0-Y|T-GAMMA-Z|GAMMA-L",
        "oI1" : "GAMMA-X-F2|SIGMA0-GAMMA-Y0|U0-X|GAMMA-R-W-S-GAMMA-T-W",
        "oI2" : "GAMMA-X-U2|Y0-GAMMA-LAMBDA0|G2-X|GAMMA-R-W-S-GAMMA-T-W",
        "oI3" : "GAMMA-X-F0|SIGMA0-GAMMA-LAMBDA0|G0-X|GAMMA-R-W-S-GAMMA-T-W",
        "oC1" : "GAMMA-Y-C0|SIGMA0-GAMMA-Z-A0|E0-T-Y|GAMMA-S-R-Z-T",
        "oC2" : "GAMMA-Y-F0|DELTA0-GAMMA-Z-B0|G0-T-Y|GAMMA-S-R-Z-T",
        "oA1" : "GAMMA-Y-C0|SIGMA0-GAMMA-Z-A0|E0-T-Y|GAMMA-S-R-Z-T",
        "oA2" : "GAMMA-Y-F0|DELTA0-GAMMA-Z-B0|G0-T-Y|GAMMA-S-R-Z-T",
        "hP1" : "GAMMA-M-K-GAMMA-A-L-H-A|L-M|H-K-H2",
        "hP2" : "GAMMA-M-K-GAMMA-A-L-H-A|L-M|H-K",
        "hR1" : "GAMMA-T-H2|H0-L-GAMMA-S0|S2-F-GAMMA",
        "hR2" : "GAMMA-L-T-P0|P2-GAMMA-F",
        "mP1" : "GAMMA-Z-D-B-GAMMA-A-E-Z-C2-Y2-GAMMA",
        "mC1" : "GAMMA-C|C2-Y2-GAMMA-M2-D|D2-A-GAMMA|L2-GAMMA-V2",
        "mC2" : "GAMMA-Y-M-A-GAMMA|L2-GAMMA-V2",
        "mC3" : "GAMMA-A-I2|I-M2-GAMMA-Y|L2-GAMMA-V2",
        "aP2" : "GAMMA-X|Y-GAMMA-Z|R-GAMMA-T|U-GAMMA-V",
        "aP3" : "GAMMA-X|Y-GAMMA-Z|R2-GAMMA-T2|U2-GAMMA-V2",
    }


References
==========
.. [1] Hinuma, Y., Pizzi, G., Kumagai, Y., Oba, F. and Tanaka, I., 2017.
       Band structure diagram paths based on crystallography.
       Computational Materials Science, 128, pp.140-184.

.. _api_constants_HPKOT_CONVENTIONAL_TO_PRIMITIVE:

*************************************************
wulfric.constants.HPKOT_CONVENTIONAL_TO_PRIMITIVE
*************************************************

Transformation matrices from conventional cell to primitive cell.

Data are from the Table 3 of [1]_.

.. code-block:: python

    HPKOT_CONVENTIONAL_TO_PRIMITIVE = {
        "cP" : np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ]
        ),
        "cF" : np.array(
            [
                [0.0, 0.5, 0.5],
                [0.5, 0.0, 0.5],
                [0.5, 0.5, 0.0],
            ]
        ),
        "cI" : np.array(
            [
                [-0.5, 0.5, 0.5],
                [0.5, -0.5, 0.5],
                [0.5, 0.5, -0.5],
            ]
        ),
        "tP" : np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ]
        ),
        "tI" : np.array(
            [
                [-0.5, 0.5, 0.5],
                [0.5, -0.5, 0.5],
                [0.5, 0.5, -0.5],
            ]
        ),
        "oP" : np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ]
        ),
        "oF" : np.array(
            [
                [0.0, 0.5, 0.5],
                [0.5, 0.0, 0.5],
                [0.5, 0.5, 0.0],
            ]
        ),
        "oI" : np.array(
            [
                [-0.5, 0.5, 0.5],
                [0.5, -0.5, 0.5],
                [0.5, 0.5, -0.5],
            ]
        ),
        "oA" : np.array(
            [
                [0.0, 0.0, 1.0],
                [0.5, 0.5, 0.0],
                [-0.5, 0.5, 0.0],
            ]
        ),
        "oC" : np.array(
            [
                [0.5, 0.5, 0.0],
                [-0.5, 0.5, 0.0],
                [0.0, 0.0, 1.0],
            ]
        ),
        "hP" : np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ]
        ),
        "hR" : np.array(
            [
                [1.0, -0.5, -0.5],
                [0.5, 0.5, -1.0],
                [0.5, 0.5, 0.5],
            ]
        ),
        "mP" : np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ]
        ),
        "mC" : np.array(
            [
                [0.5, -0.5, 0.0],
                [0.5, 0.5, 0.0],
                [0.0, 0.0, 1.0],
            ]
        ),
        "aP" : np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ]
        ),
    }


References
==========
.. [1] Hinuma, Y., Pizzi, G., Kumagai, Y., Oba, F. and Tanaka, I., 2017.
       Band structure diagram paths based on crystallography.
       Computational Materials Science, 128, pp.140-184.

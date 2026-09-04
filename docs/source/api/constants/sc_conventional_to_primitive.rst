.. _api_constants_SC_CONVENTIONAL_TO_PRIMITIVE:

**********************************************
wulfric.constants.SC_CONVENTIONAL_TO_PRIMITIVE
**********************************************

Transformation matrices from conventional cell to primitive cell.

Data are from Table 2 of [1]_.

.. code-block:: python

    SC_CONVENTIONAL_TO_PRIMITIVE = {
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
                [0.5, 0.5, 0.0],
                [-0.5, 0.5, 0.0],
                [0.0, 0.0, 1.0],
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
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
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
.. [1] Setyawan, W. and Curtarolo, S., 2010.
       High-throughput electronic band structure calculations: Challenges and tools.
       Computational materials science, 49(2), pp. 299-312.

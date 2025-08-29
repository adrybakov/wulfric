.. _wulfric_cite:

***************
How to cite us?
***************

If you use wulfric in a your work, please cite it

.. code-block::

    wulfric v<version>, wulfric.org.

.. code-block:: LaTeX

    @online{wulfric,
        author = {Andrey Rybakov},
        title  = {wulfric v<version>},
        year   = {2023},
        url    = {wulfric.org},
    }

Dependency citations
====================

Wulfric is using the work of other authors in some of its methods.

*   If you use functions that depend on |spglib|_, please cite

    .. code-block::

        Togo, A., Shinohara, K. and Tanaka, I., 2024.
        Spglib: a software library for crystal symmetry search.
        Science and Technology of Advanced Materials: Methods, 4(1), p.2384822.

    .. code-block:: LaTeX

        @article{Togo2024,
            title = {Spglib: a software library for crystal symmetry search},
            volume = {4},
            ISSN = {2766-0400},
            url = {http://dx.doi.org/10.1080/27660400.2024.2384822},
            DOI = {10.1080/27660400.2024.2384822},
            number = {1},
            journal = {Science and Technology of Advanced Materials: Methods},
            publisher = {Informa UK Limited},
            author = {Togo,  Atsushi and Shinohara,  Kohei and Tanaka,  Isao},
            year = {2024},
            month = oct
        }



*   If you use convention of Setyawan and Curtarolo (``convention="SC"``), please cite:

    .. code-block::

        Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.


    .. code-block:: LaTeX

        @article{Setyawan2010,
            title = {High-throughput electronic band structure calculations: Challenges and tools},
            volume = {49},
            ISSN = {0927-0256},
            url = {http://dx.doi.org/10.1016/j.commatsci.2010.05.010},
            DOI = {10.1016/j.commatsci.2010.05.010},
            number = {2},
            journal = {Computational Materials Science},
            publisher = {Elsevier BV},
            author = {Setyawan,  Wahyu and Curtarolo,  Stefano},
            year = {2010},
            month = aug,
            pages = {299-312}
        }

*   If you use convention of Hinuma, Pizzi, Kumagai, Oba, Tanaka (``convention="HPKOT"``),
    please cite:

    .. code-block::

        Hinuma, Y., Pizzi, G., Kumagai, Y., Oba, F. and Tanaka, I., 2017.
        Band structure diagram paths based on crystallography.
        Computational Materials Science, 128, pp.140-184.


    .. code-block:: LaTeX

        @article{Hinuma2017,
            title = {Band structure diagram paths based on crystallography},
            volume = {128},
            ISSN = {0927-0256},
            url = {http://dx.doi.org/10.1016/j.commatsci.2016.10.015},
            DOI = {10.1016/j.commatsci.2016.10.015},
            journal = {Computational Materials Science},
            publisher = {Elsevier BV},
            author = {Hinuma,  Yoyo and Pizzi,  Giovanni and Kumagai,  Yu and Oba,  Fumiyasu and Tanaka,  Isao},
            year = {2017},
            month = feb,
            pages = {140-184}
        }

*   If you use ``wulfric.cell.get_niggli(..., implementation="wulfric")``, please cite

    .. code-block::

        Křivý, I. and Gruber, B., 1976.
        A unified algorithm for determining the reduced (Niggli) cell.
        Acta Crystallographica Section A: Crystal Physics, Diffraction,
        Theoretical and General Crystallography,
        32(2), pp.297-298.

    and

    .. code-block::

        Grosse-Kunstleve, R.W., Sauter, N.K. and Adams, P.D., 2004.
        Numerically stable algorithms for the computation of reduced unit cells.
        Acta Crystallographica Section A: Foundations of Crystallography,
        60(1), pp.1-6.

    .. code-block:: LaTeX

        @article{Kiv1976,
            title = {A unified algorithm for determining the reduced (Niggli) cell},
            volume = {32},
            ISSN = {0567-7394},
            url = {http://dx.doi.org/10.1107/S0567739476000636},
            DOI = {10.1107/s0567739476000636},
            number = {2},
            journal = {Acta Crystallographica Section A},
            publisher = {International Union of Crystallography (IUCr)},
            author = {Křivý,  I. and Gruber,  B.},
            year = {1976},
            month = mar,
            pages = {297-298}
        }

        @article{GrosseKunstleve2003,
            title = {Numerically stable algorithms for the computation of reduced unit cells},
            volume = {60},
            ISSN = {0108-7673},
            url = {http://dx.doi.org/10.1107/S010876730302186X},
            DOI = {10.1107/s010876730302186x},
            number = {1},
            journal = {Acta Crystallographica Section A Foundations of Crystallography},
            publisher = {International Union of Crystallography (IUCr)},
            author = {Grosse-Kunstleve,  R. W. and Sauter,  N. K. and Adams,  P. D.},
            year = {2003},
            month = dec,
            pages = {1-6}
        }

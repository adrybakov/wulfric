# Wulfric - Crystal, Lattice, Atoms, K-path.
# Copyright (C) 2023-2024 Andrey Rybakov
#
# e-mail: anry@uv.es, web: adrybakov.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from copy import deepcopy
from typing import Iterable

import numpy as np

from wulfric.constants import ATOM_TYPES, TODEGREES, TORADIANS

__all__ = ["Atom"]


class Atom:
    r"""
    Atom class.

    Notes
    -----
    "==" (and "!=") operator compare two atoms based on their names and indexes.
    If index of one atom is not defined, then comparison raises ``ValueError``.
    If two atoms have the same :py:attr:`.Atom.name` and :py:attr:`.Atom.index` then they are considered to be equal.
    Even if they have different :py:attr:`.Atom.positions`.
    For the check of the atom type use :py:attr:`.Atom.type`.
    In most cases :py:attr:`.Atom.name` = :py:attr:`.Atom.type`.

    Parameters
    ----------
    name : str, default "X"
        Name of the atom. It cannot start or end with double underline "__".
    position : (3,) |array-like|_, default [0, 0, 0]
        Position of the atom in absolute or relative coordinates.
    spin : float or (3,) |array-like|_, optional
        Spin or spin vector of the atom. If only one value is given, then spin vector is oriented along *z* axis.
        Connected with ``magmom``, see :py:attr:`.Atom.magmom`.
    magmom : float or (3,) |array-like|_, optional
        Magnetic moment of the atom. Vector or the value.
        If a number is given, then oriented along *z* axis.
        Connected with ``spin``, see :py:attr:`.Atom.spin`.
    g_factor : float, default 2
        Lande g-factor. Relates ``magmom`` and ``spin``.
    charge : float, optional
        Charge of the atom.
    index : int, optional
        Custom index of an atom. It is used differently in different scenarios.
        Combination of :py:attr:`.name` and :py:attr:`.index`
        is meant to be unique, when an atom belongs to some group
        (i.e. to :py:class:`.Crystal`).
    """

    def __init__(
        self,
        name="X",
        position=(0, 0, 0),
        spin=None,
        magmom=None,
        g_factor=2.0,
        charge=None,
        index=None,
    ) -> None:
        # Set name
        self._name = "X"
        self.name = name

        # Set index
        self._index = None
        if index is not None:
            self.index = index

        # Set position
        self._position = None
        self.position = position

        # Set g-factor
        self._g_factor = None
        self.g_factor = g_factor

        # Set spin
        self._spin = None
        if spin is None and magmom is None:
            self.spin = (0, 0, 0)
        elif spin is None and magmom is not None:
            self.magmom = magmom
        elif spin is not None and magmom is None:
            self.spin = spin
        elif spin is not None and magmom is not None:
            if not np.allclose(float(g_factor) * np.array(spin), np.array(magmom)):
                raise ValueError(
                    f"Spin and magmom parameters are not independent, expected mu = g*spin to hold, got: {magmom} != {g_factor}{spin}"
                )
                self.magmom = magmom

        # Set charge
        self._charge = None
        if charge is not None:
            self.charge = charge

        # Set type placeholder
        self._type = None

    ################################################################################
    #                     Allow the atom to be a dictionary key                    #
    ################################################################################
    def __hash__(self):
        return hash(str(self.name) + str(self.index))

    # ==
    def __eq__(self, other) -> bool:
        if not isinstance(other, Atom):
            raise TypeError(
                f"TypeError: unsupported operand type(s) "
                + f"for ==: '{other.__class__.__name__}' and 'Atom'"
            )
        return self.name == other.name and self.index == other.index

    # !=
    def __neq__(self, other):
        return not self == other

    ################################################################################
    #                             Name, type and index                             #
    ################################################################################
    @property
    def name(self) -> str:
        r"""
        Name of the atom.

        Any string can be a name of an atom,
        but it cannot start nor end with double underscore "__".

        Returns
        -------
        name : str
            Name of the atom.
        """
        return self._name

    @name.setter
    def name(self, new_name):
        if new_name.startswith("__") or new_name.endswith("__"):
            raise ValueError(
                f"Name of the atom ({new_name}) is not valid. It cannot start neither end with '__'."
            )
        self._name = str(new_name)
        # Reset type
        self._type = None

    @property
    def type(self) -> str:
        r"""
        Type of an atom (i.e. Cr, Ni, ...).

        Computed from the :py:attr:`.Atom.name` automatically.
        If it is impossible to deduct the atom type based on the atom's name, then
        it is set to "X" (atom type is undefined). It is not meant to be specified directly,
        but rather encourage you to use meaningful name for atoms.

        Returns
        -------
        type : str
            Type of the atom.

        Examples
        --------

        .. doctest::

            >>> from wulfric import Atom
            >>> atom = Atom()
            >>> atom.type
            'X'
            >>> atom.name = "Cr"
            >>> atom.type
            'Cr'
            >>> atom.name = "Cr1"
            >>> atom.type
            'Cr'
            >>> atom.name = "_3341Cr"
            >>> atom.type
            'Cr'
            >>> atom.name = "cr"
            >>> atom.type
            'Cr'
            >>> atom.name = "S"
            >>> atom.type
            'S'
            >>> atom.name = "Se"
            >>> atom.type
            'Se'
            >>> atom.name = "Sp"
            >>> atom.type
            'S'
            >>> atom.name = "123a"
            >>> atom.type
            'X'

        Notes
        -----
        If :py:attr:`.Atom.name` contains several possible atom types of length 2
        as substrings, then the type is equal to the first one found.
        """

        if self._type is None:
            self._type = "X"
            for atom_type in ATOM_TYPES:
                if atom_type.lower() in self._name.lower():
                    self._type = atom_type
                    # Maximum amount of characters in the atom type
                    # Some 1-character types are parts of some 2-character types (i.e. "Se" and "S")
                    # If type of two characters is found then it is unique,
                    # If type of one character is found, then the search must continue
                    if len(atom_type) == 2:
                        break
        return self._type

    @property
    def index(self):
        r"""
        Index of an atom, meant to be unique in some abstract group of atoms.

        Returns
        -------
        index : any
            Index of the atom. Typically an integer.
            It is expected to be convertible to ``str`` in general

        Raises
        ------
        ValueError
            If index is not defined for the atom.
        """

        if self._index is None:
            raise ValueError(
                f"Index is not defined for the '{self.name}' atom ({self})."
            )
        return self._index

    @index.setter
    def index(self, new_index):
        self._index = new_index

    @property
    def fullname(self) -> str:
        r"""
        Fullname (:py:attr:`Atom.name`+``__``+:py:attr:`Atom.index`) of an atom.

        Double underscore ("__") is used intentionally,
        so the user can use single underscore ("_") in the name of the atom.

        If index is not defined, then only the name is returned.

        Returns
        -------
        fullname : str
            Fullname of the atom.
        """

        try:
            return f"{self.name}__{self.index}"
        except ValueError:
            return self.name

    ################################################################################
    #                            Position in real space                            #
    ################################################################################
    @property
    def position(self) -> np.ndarray:
        r"""
        Relative or absolute position of the atom in some units.

        Returns
        -------
        position : (3,) :numpy:`ndarray`
            Position of the atom in absolute or relative coordinates.
            The units of the coordinates and whether they are absolute or relative
            depend on the context. At the logical level of the pure :py:class:`.Atom`
            class the coordinates are just three numbers. No additional meaning is expected.
        """

        return self._position

    @position.setter
    def position(self, new_position):
        try:
            new_position = np.array(new_position, dtype=float)
        except:
            raise ValueError(f"New position is not array-like, got '{new_position}'")
        if new_position.shape != (3,):
            raise ValueError(
                f"New position has to be a 3 x 1 vector, got shape '{new_position.shape}' (expected '(3,)')"
            )
        self._position = new_position

    ################################################################################
    #                             Magnetic properties                              #
    ################################################################################
    @property
    def g_factor(self) -> float:
        R"""
        g-factor of an atom, relates its :py:attr:`.Atom.spin` with its
        :py:attr:`.Atom.magmom`.magmom

        .. versionadded:: 0.2.0

        .. math::
          \mu = - g\mu_BS

        where :math:`\mu_B` is a Bohr magneton and S is :py:attr:`.Atom.spin` or
        :py:attr:`.Atom.spin_vector` if the latter is defined.

        g-factor is equal to :math:`2` by default. We use :math:`\mu_B = 1` internally, so
        the units are left for the user, i.e. in order to have value with units - multiply by the value of
        :math:`\mu_B` in the desired system of units.



        See Also
        --------
        spin
        spin_direction
        spin_vector
        magmom
        """
        return self._g_factor

    @g_factor.setter
    def g_factor(self, new_value):
        try:
            new_value = float(new_value)
        except ValueError:
            raise ValueError(
                f"Expected something convertible to float (g-factor), got '{new_value}'"
            )

        self._g_factor = new_value

    @property
    def spin(self) -> float:
        r"""
        Spin value of the atom.

        To access the vector use :py:attr:`.Atom.spin_vector`.

        By default it is equal to :math:`0`.

        Returns
        -------
        spin : float
            Spin value of the atom.

        Raises
        ------
        ValueError
            If spin is not defined for the atom.

        Notes
        -----
        Spin is connected with :py:attr:`.Atom.magmom`,
        therefore it can  change if the magnetic moment is changed.

        See Also
        --------
        spin_vector
        spin_direction
        magmom
        g_factor
        """

        return np.linalg.norm(self._spin_vector)

    @spin.setter
    def spin(self, new_value):
        if isinstance(new_value, Iterable):
            try:
                new_value = np.array(new_value, dtype=float)
            except:
                raise ValueError(f"Expected array-like, got {new_value}")
            if new_value.shape != (3,):
                raise ValueError(
                    f"Expected (3,) array-like, got shape: {new_value.shape}"
                )
            self._spin_vector = new_value
        else:
            try:
                new_value = float(new_value)
            except ValueError:
                raise ValueError(
                    f"Expected something convertible to float, got '{new_value}'"
                )
            self._spin_vector = np.array([0, 0, 1], dtype=float) * new_value

    @property
    def spin_direction(self) -> np.ndarray:
        r"""
        Direction of the classical spin vector.

        .. math::
            \vert \boldsymbol{\hat{S}} \vert = 1

        By default it is undefined: :math:`(0,0,0)^T`

        Returns
        -------
        spin_direction : (3,) :numpy:`ndarray`
            Direction of the classical spin vector.

        See Also
        --------
        spin_vector
        spin
        magmom
        g_factor
        """

        return np.divide(
            self._spin_vector,
            np.linalg.norm(self._spin_vector),
            out=np.zeros_like(self._spin_vector),
            where=np.linalg.norm(self._spin_vector) != 0,
        )

    @spin_direction.setter
    def spin_direction(self, new_value):
        # Remember the old value
        factor = self.spin
        # Checks are the same as for spin setter
        self.spin = new_value
        # Restore original length
        if self.spin != 0:
            self._spin_vector *= factor / self.spin

    @property
    def spin_vector(self) -> np.ndarray:
        r"""
        Classical spin vector of the atom.

        .. math::
            \boldsymbol{S}
            =
            \begin{pmatrix}
                S_x \\ S_y \\ S_z
            \end{pmatrix}

        By default it is set to :math:`(0,0,0)^T`.

        Returns
        -------
        spin_vector : (3,) :numpy:`ndarray`
            Classical spin vector of the atom.

        See Also
        --------
        spin_direction
        spin
        magmom
        g_factor
        """

        return self._spin_vector

    @spin_vector.setter
    def spin_vector(self, new_value):
        self.spin = new_value

    @property
    def spin_angles(self) -> tuple:
        R"""
        Polar :math:`\theta` and azimuthal :math:`\varphi` angles of the spin vector:

        .. versionadded:: 0.2.0

        .. math::

            \boldsymbol{S} = S
            \begin{pmatrix}
                \cos\varphi\sin\theta \\
                \sin\varphi\sin\theta \\
                \cos\theta
            \end{pmatrix}

        Returns
        -------
        theta, phi : tuple of float
            :math:`0^{\circ} \le \theta \le 180^{\circ}` and :math:`0^{\circ} \le \varphi \le 360^{\circ}`.
        """

        if np.allclose(self.spin_direction, [0, 0, 1]):
            return 0.0, 90.0
        if np.allclose(self.spin_direction, [0, 0, -1]):
            return 180.0, 90.0

        theta = (
            np.arccos(np.clip(self.spin_direction[2], a_min=-1, a_max=1)) * TODEGREES
        )

        if self.spin_direction[1] >= 0:
            phi = (
                np.arccos(np.clip(self.spin_direction[0], a_min=-1, a_max=1))
                * TODEGREES
            )

        else:
            phi = (
                360
                - np.arccos(np.clip(self.spin_direction[0], a_min=-1, a_max=1))
                * TODEGREES
            )

        return theta, phi

    @spin_angles.setter
    def spin_angles(self, new_value):
        try:
            theta, phi = (
                float(new_value[0]) * TORADIANS,
                float(new_value[1]) * TORADIANS,
            )
        except ValueError:
            raise ValueError(
                f"Expected something convertible to float, got '{new_value}'"
            )

        self.spin_direction = (
            np.cos(phi) * np.sin(theta),
            np.sin(phi) * np.sin(theta),
            np.cos(theta),
        )

    @property
    def magmom(self) -> np.ndarray:
        r"""
        Magnetic moment of the atom.

        It is defined as:

        .. math::
            \boldsymbol{\mu} = g\mu_B \boldsymbol{S}

        Internally we use :math:`\mu_B = 1`, therefore the actual formula is
        :math:`\boldsymbol{\mu} = - g\boldsymbol{S}` and magnetic moment is store in Bohr magnetons.
        By default g is equal to :math:`2` (see :py:attr:`.Atom.g_factor`).


        Returns
        -------
        magmom : (3,) :numpy:`ndarray`
            Magnetic moment of the atom.

        Notes
        -----
        Magnetic moment is not stored internally, but rather computed from the :py:attr:`.Atom.spin`.
        Note that if magnetic moment is set, then the spin is changed as well:

        .. doctest::

            >>> from wulfric import Atom
            >>> atom = Atom()
            >>> atom.magmom
            array([-0., -0., -0.])
            >>> atom.magmom = (1,0,0)
            >>> atom.spin
            0.5
            >>> atom.spin_vector
            array([-0.5, -0. , -0. ])

        See Also
        --------
        spin
        spin_vector
        spin_direction
        """

        return -self.g_factor * self.spin_vector

    @magmom.setter
    def magmom(self, new_value):
        # The checks are the same as for the spin
        self.spin = new_value
        # If the assignment is correct now we need to convert the value
        self._spin_vector /= -self.g_factor

    ################################################################################
    #                              Electric properties                             #
    ################################################################################
    @property
    def charge(self) -> float:
        r"""
        Charge of the atom.

        Returns
        -------
        charge : float
            Charge of the atom.
        """

        if self._charge is None:
            raise ValueError(f"Charge is not defined for the atom {self.fullname}.")
        return self._charge

    @charge.setter
    def charge(self, new_value):
        try:
            self._charge = float(new_value)
        except ValueError:
            raise ValueError(
                f"Expected something convertible to float, got {new_value}"
            )

    ################################################################################
    #                                     Copy                                     #
    ################################################################################

    def copy(self):
        r"""
        Create a copy of the atom.

        .. versionadded:: 0.3.0

        Returns
        -------
        atom : :py:class:`.Atom`
            Copy of the atom.
        """

        deepcopy(self)

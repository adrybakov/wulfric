# Wulfric - Cell, Atoms, K-path.
# Copyright (C) 2023-2025 Andrey Rybakov
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


class AbstractBackend:
    def __init__(self) -> None:
        self.kinds = {
            "conventional": self.plot_conventional,
            "primitive": self.plot_primitive,
            "brillouin": self.plot_brillouin,
            "kpath": self.plot_kpath,
            "brillouin-kpath": self.plot_brillouin_kpath,
            "brillouin_kpath": self.plot_brillouin_kpath,
            "wigner-seitz": self.plot_wigner_seitz,
            "wigner_seitz": self.plot_wigner_seitz,
            "unit-cell": self.plot_unit_cell,
            "unit_cell": self.plot_unit_cell,
            "lattice": self.plot_lattice,
        }

    # Backend-independent functions
    def plot(self, *args, kind, **kwargs):
        r"""
        Main plotting method.

        Actual list of supported kinds can be check with:

        .. doctest::

            >>> self.kinds.keys() # doctest: +SKIP

        Parameters
        ----------
        kind : str or list of str
            Type of the plot to be plotted. Supported plots:

            * "conventional"
            * "primitive"
            * "brillouin"
            * "kpath"
            * "brillouin-kpath"
            * "wigner-seitz"
            * "unit-cell"
        *args
            Passed directly to the plotting functions.
        **kwargs
            Passed directly to the plotting functions.

        Raises
        ------
        ValueError
            If the plot kind is not supported.

        See Also
        --------
        plot_conventional : "conventional" plot.
        plot_primitive : "primitive" plot.
        plot_brillouin : "brillouin" plot.
        plot_kpath : "kpath" plot.
        plot_brillouin_kpath : "brillouin_kpath" plot.
        plot_wigner_seitz : "wigner-seitz" plot.
        plot_unit_cell : "unit-cell" plot.
        show : Shows the plot.
        save : Save the figure in the file.
        """
        if isinstance(kind, str):
            kinds = [kind]
        else:
            kinds = kind
        for kind in kinds:
            if kind in self.kinds:
                self.kinds[kind](*args, **kwargs)
            else:
                raise ValueError(f"Plot kind '{kind}' does not exist!")

    # Backend-dependent functions
    def remove(self, *args, **kwargs):
        raise NotImplementedError

    def show(self, *args, **kwargs):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        raise NotImplementedError

    def clear(self, *args, **kwargs):
        raise NotImplementedError

    def legend(self, *args, **kwargs):
        raise NotImplementedError

    # Backend-independent functions
    def plot_brillouin(self, *args, color="#FF4D67", **kwargs):
        r"""
        Plot brillouin zone.

        Parameters
        ----------
        *args
            Passed to the :py:meth:`.plot_wigner_seitz` function.
        color : str, default "#FF4D67"
            Colour for the brillouin zone. Any format supported by the used backend.
        **kwargs
            Passed to the :py:meth:`.plot_wigner_seitz` function.

        See Also
        --------
        plot_wigner_seitz : for the list of parameters
        """

        self.plot_wigner_seitz(*args, reciprocal=True, color="#FF4D67", **kwargs)

    def plot_brillouin_kpath(
        self, *args, zone_color="#FF4D67", path_color="black", **kwargs
    ):
        r"""
        Plot brillouin zone and kpath.

        Parameters
        ----------
        *args
            Passed to the :py:meth:`.plot_brillouin` and :py:meth:`.plot_kpath` functions.
        zone_color : str, default "#FF4D67"
            Colour for the brillouin zone. Any format supported by the used backend.
        zone_color : str, default "black"
            Colour for the k path. Any format supported by the used backend.
        **kwargs
            Passed to the :py:meth:`.plot_brillouin` and :py:meth:`.plot_kpath` functions.

        See Also
        --------
        plot_brillouin : plot brillouin zone
        plot_kpath : plot kpath
        """

        self.plot_brillouin(*args, color=zone_color, **kwargs)
        self.plot_kpath(*args, color=path_color, **kwargs)

    def plot_primitive(self, *args, **kwargs):
        r"""
        Plot primitive unit cell.

        Parameters
        ----------
        **kwargs
            Passed to the :py:meth:`.plot_unit_cell` function.

        See Also
        --------
        plot_unit_cell : for the list of parameters
        """

        self.plot_unit_cell(*args, conventional=False, **kwargs)

    def plot_conventional(self, *args, **kwargs):
        r"""
        Plot conventional unit cell.

        See Also
        --------
        plot_unit_cell : for the list of parameters
        """

        self.plot_unit_cell(*args, conventional=True, **kwargs)

    # Backend-dependent functions
    def plot_unit_cell(self, *args, **kwargs):
        raise NotImplementedError

    def plot_wigner_seitz(self, *args, **kwargs):
        raise NotImplementedError

    def plot_kpath(self, *args, **kwargs):
        raise NotImplementedError

    def plot_lattice(self, *args, **kwargs):
        raise NotImplementedError

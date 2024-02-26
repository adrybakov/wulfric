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

__version__ = "0.3.0"
__doclink__ = "wulfric.org"
__git_hash__ = "5fb82627cf4e29e0bec963e761371a49e14d7ed7"
__release_date__ = "26 February 2024"


from . import bravais_lattice
from . import cell as Cell
from . import (
    constants,
    crystal,
    decorate,
    geometry,
    identify,
    io,
    kpoints,
    lattice,
    lattice_plotter,
    numerical,
)
from .atom import *
from .bravais_lattice import *
from .constants import *
from .crystal import *
from .decorate import *
from .geometry import *
from .identify import *
from .io import *
from .kpoints import *
from .lattice import *
from .lattice_plotter import *
from .numerical import *

__all__ = ["__version__", "__doclink__", "__git_hash__", "__release_date__", "Cell"]
__all__.extend(bravais_lattice.__all__)
__all__.extend(decorate.__all__)
__all__.extend(io.__all__)
__all__.extend(atom.__all__)
__all__.extend(constants.__all__)
__all__.extend(crystal.__all__)
__all__.extend(geometry.__all__)
__all__.extend(identify.__all__)
__all__.extend(kpoints.__all__)
__all__.extend(lattice_plotter.__all__)
__all__.extend(lattice.__all__)
__all__.extend(numerical.__all__)

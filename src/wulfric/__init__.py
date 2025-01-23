# Wulfric - Crystal, Lattice, Atoms, K-path.
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

__version__ = "0.4.0"
__doclink__ = "wulfric.org"
__git_hash__ = "a581649f7c740a326f6be323517e533f921a214a"
__release_date__ = "15 October 2024"


from . import cell, constants
from ._decorate_array import *
from ._exceptions import *
from ._numerical import *
from ._package_info import *

# from . import bravais_lattice
# from . import (
#     crystal,
#     decorate,
#     geometry,
#     identify,
#     io,
#     kpoints,
#     lattice,
#     lattice_plotter,
#     numerical,
# )
# from .atom import *
# from .bravais_lattice import *
# from .crystal import *
# from .decorate import *
# from .geometry import *
# from .identify import *
# from .io import *
# from .kpoints import *
# from .lattice import *
# from .lattice_plotter import *
# from .numerical import *

# __all__.extend(bravais_lattice.__all__)
# __all__.extend(decorate.__all__)
# __all__.extend(io.__all__)
# __all__.extend(atom.__all__)
# __all__.extend(crystal.__all__)
# __all__.extend(geometry.__all__)
# __all__.extend(identify.__all__)
# __all__.extend(kpoints.__all__)
# __all__.extend(lattice_plotter.__all__)
# __all__.extend(lattice.__all__)
# __all__.extend(numerical.__all__)

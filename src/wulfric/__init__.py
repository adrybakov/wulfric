# WULFRIC - Crystal, Lattice, Atoms, K-path.
# Copyright (C) 2023 Andrey Rybakov
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

__version__ = "0.1.0"
__doclink__ = "wulfric.org"
__git_hash__ = "undefined"
__release_date__ = "undefined"


from . import (
    #     # constants,
    #     # crystal,
    decorate,
    #     # geometry,
    #     # io,
    #     # numerical,
)

# from .constants import *
# from .crystal import *
from .decorate import *

# from .geometry import *
# from .io import *
# from .numerical import *

__all__ = ["__version__", "__doclink__", "__git_hash__", "__release_date__"]
# __all__.extend(constants.__all__)
# __all__.extend(crystal.__all__)
__all__.extend(decorate.__all__)
# __all__.extend(geometry.__all__)
# __all__.extend(io.__all__)
# __all__.extend(numerical.__all__)

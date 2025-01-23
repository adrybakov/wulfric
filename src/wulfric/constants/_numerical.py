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

from math import pi

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")

# Length variables
ABS_TOL = 1e-8  # For the linear spatial variables
REL_TOL = 1e-4  # For the linear spatial variables

# MIN_LENGTH is a direct consequence of the REL_TOL and ABS_TOL:
# for l = MIN_LENGTH => ABS_TOL = l * REL_TOL
MIN_LENGTH = ABS_TOL / REL_TOL

# MAX_LENGTH is a direct consequence of the ABS_TOL:
# Inverse of the MAX_LENGTH in the real space has to be meaningful
# in the reciprocal space (< ABS_TOL).
MAX_LENGTH = 1 / ABS_TOL

# TODO Think how to connect angle tolerance with spatial tolerance.

ABS_TOL_ANGLE = 1e-4  # For the angular variables, in degrees.
REL_TOL_ANGLE = 1e-2  # For the angular variables.

# MIN_ANGLE is a direct consequence of the REL_TOL_ANGLE and ABS_TOL_ANGLE:
# for a = MIN_ANGLE => ABS_TOL_ANGLE = a * REL_TOL_ANGLE
MIN_ANGLE = ABS_TOL_ANGLE / REL_TOL_ANGLE  # In degrees

# No need to define MAX_ANGLE, as it is restricted by 2 pi in the context of Wulfric.


################################################################################
#                                   Numerical                                  #
################################################################################
TODEGREES = 180.0 / pi


TORADIANS = pi / 180.0

# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir

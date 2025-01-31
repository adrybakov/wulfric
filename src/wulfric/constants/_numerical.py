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


from math import pi

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")

# Length variables
# For the linear spatial variables.
EPS_LENGTH = 1e-10
# For the linear spatial variables. It serves as eps_volume for is_relative()
EPS_RELATIVE = 1e-5

# MIN_LENGTH is a direct consequence of the EPS_LENGTH:
MIN_LENGTH = EPS_LENGTH

# MAX_LENGTH is a direct consequence of the EPS_LENGTH:
# Inverse of the MAX_LENGTH in the real space has to be meaningful
# in the reciprocal space (>= EPS_LENGTH).
MAX_LENGTH = 1 / EPS_LENGTH

# TODO Think how to connect angle tolerance with spatial tolerance.

EPS_ANGLE = 1e-4  # For the angular variables, in degrees.

# MIN_ANGLE is a direct consequence of the EPS_ANGLE
MIN_ANGLE = EPS_ANGLE  # In degrees

# No need to define MAX_ANGLE, as it is restricted by 2 pi in the context of wulfric.


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

*******************************************
Tools for the package setup and development
*******************************************

All scripts, which are intended to be use in the development/deployment process
are located here, unless they belong in the docs/ or tests/ directories.

Makefile is not located here, but heavily relies on the scripts in this directory.

All scripts are intended to be run from the root directory of the project.


Tools
=====

plot-bravais-lattice.py
-----------------------

Plot all examples of the bravais lattice.

plot-data-structure.py
-----------------------

Plot the data structure of the package.

check-release-metadata.py
------------------

Prepare the release of the package. Never release without the successful run of it.

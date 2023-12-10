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

from argparse import ArgumentParser, RawDescriptionHelpFormatter

from wulfric import __version__
from wulfric._pinfo import conditions, logo, warranty


def main():
    parser = ArgumentParser(
        description=logo(),
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "command",
        default=None,
        help="Which command to run",
        choices=["logo", "warranty", "conditions", "version"],
        nargs="?",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Print version",
    )
    args = parser.parse_args()
    if args.command == "logo":
        print(logo())
    elif args.command == "warranty":
        print("\n" + warranty() + "\n")
    elif args.command == "conditions":
        print("\n" + conditions() + "\n")
    elif args.command == "version" or args.version:
        print(f"WULFRIC v{__version__}")
    elif args.command is None:
        parser.print_help()
    else:
        raise ValueError(f"Command {args.command} is not recognized.")


if __name__ == "__main__":
    main()

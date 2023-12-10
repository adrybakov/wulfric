# wulfric - program for spin Hamiltonian and magnons.
# Copyright (C) 2022-2023  Andrey Rybakov
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

from argparse import ArgumentParser

from wulfric._pinfo import logo, copyright, warranty, conditions
from wulfric import __version__


def main():
    parser = ArgumentParser(
        description="WULFRIC package",
    )
    parser.add_argument(
        "command",
        default="logo",
        help="Which command to run",
        choices=["logo", "warranty", "conditions", "version", "-v", "--version"],
    )
    args = parser.parse_args()
    if args.command == "logo":
        print(logo() + "\n" + copyright())
    elif args.command == "warranty":
        print(warranty())
    elif args.command == "conditions":
        print(conditions())
    elif (
        args.command == "version" or args.command == "-v" or args.command == "--version"
    ):
        print(__version__)
    else:
        raise ValueError(f"Command {args.command} is not recognized.")


if __name__ == "__main__":
    main()

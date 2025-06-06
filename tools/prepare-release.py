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


import os
import re
import sys
from argparse import ArgumentParser
from calendar import month_name
from datetime import datetime
from random import randint

import git
from termcolor import colored

N = 60

QUOTES_IF_BAD = [
    # Albus Dumbledore
    "To the well-organized mind, death is but the next great adventure.",
    # Ron Weasley
    "When in doubt, go to the library.",
    # Albus Dumbledore
    "We must try not to sink beneath our anguish, but battle on.",
    # Albus Dumbledore
    "We must all face the choice between what is right and what is easy.",
    # Cheshire Cat
    "We're all mad here.",
]

QUOTES_IF_GOOD = [
    # Dobby
    "Dobby is free.",
    # Harry Potter
    "Mischief Managed!",
    # Severues Snape
    "After all this time? Always.",
    # Albus Dumbledore
    "And now, let us step out into the night and pursue that flighty temptress, adventure.",
    # Hamfast Gamgee
    "All's well that ends better.",
]


class ERROR(Exception):
    pass


def envelope(message: str):
    """
    Decorator for printing a message before and "Done" after a function.

    Parameters
    ----------
    message : str
        Message to print before the function.
    """

    def wrapper(func):
        def inner(*args, relax=False, **kwargs):
            print(f"{f'{message}'} ... ")
            errors = func(*args, **kwargs)
            if errors is not None:
                quote = colored(
                    "\n" + QUOTES_IF_BAD[randint(0, len(QUOTES_IF_BAD) - 1)], "red"
                )
                if relax:
                    print(errors + quote)
                else:
                    raise ERROR(errors + quote)
            else:
                quote = colored(
                    "\n" + QUOTES_IF_GOOD[randint(0, len(QUOTES_IF_GOOD) - 1)], "green"
                )
                print(quote)
            print(f"{'':=^{N}}")
            return errors is None

        return inner

    return wrapper


@envelope(message="Updating __init__.py")
def update_init(version, root_dir: str):
    """
    Update __init__.py file.

    Change the __git_hash__, __release_date__ and __version__ variables.

    Parameters
    ----------
    version : str
        Target version for the release.
    """
    cd = datetime.now()

    variables = ["__release_date__", "__version__"]
    values = [f"{cd.day} {month_name[cd.month]} {cd.year}", version]
    good = [False, False]
    good_message = {False: "not updated", True: "updated"}

    # Read __init__.py
    init_file_path = os.path.join(root_dir, "src", "wulfric", "__init__.py")
    init_file = open(init_file_path, "r")
    init_file_content = init_file.readlines()
    init_file.close()

    # Update __init__.py
    for l_i, line in enumerate(init_file_content):
        # Update git hash
        for v_i, variable in enumerate(variables):
            if re.fullmatch(f"{variable}.*\n", line):
                init_file_content[l_i] = f'{variable} = "{values[v_i]}"\n'
                good[v_i] = True

    # Check if all variables were updated
    if not all(good):
        sys.tracebacklimit = 0
        return "".join(
            [
                colored("\nFailed to update some variables in '__init__.py':\n", "red"),
                *[
                    f"    {variables[i]:20} : {good_message[good[i]]}\n"
                    for i in range(len(variables))
                ],
                "Please check the file and try again\n",
            ]
        )

    # Write __init__.py
    init_file = open(init_file_path, "w", encoding="utf-8")
    init_file.writelines(init_file_content)
    init_file.close()


@envelope(message="Checking release notes")
def check_release_notes(version: str, root_dir: str):
    """
    Check if the release notes are up to date.

    Parameters
    ----------
    version : str
        Target version for the release.
    """
    path = os.path.join(root_dir, "docs", "source", "release-notes")
    # (major, minor, rest)
    major, minor, rest = tuple(map(int, version.split(".")[:3]))

    for _, _, filenames in os.walk(path):
        break
    # (major, minor)
    files = []
    for filename in sorted(filenames):
        if re.fullmatch(R"[0-9]*\.[0-9]*\.rst", filename):
            files.append(tuple(map(int, filename.split(".")[:2])))

    # Check the minor version file
    if (major, minor) not in files:
        sys.tracebacklimit = 0
        return "".join(
            [
                colored(
                    f"\nRelease notes for the minor version {major}.{minor} are not available\n",
                    "red",
                ),
                "Please add the file\n\n",
                f"    {major}.{minor}.rst\n\n",
                "to the directory\n\n",
                f"    docs/source/release-notes/\n",
            ]
        )

    # Update the toctree in the index file
    # Read and process current content
    index_file = open(os.path.join(path, "index.rst"), "r")
    lines = []
    skip_empty = False
    for line in index_file:
        untouched_line = line
        line = line.translate(str.maketrans("", "", " \n"))
        if re.fullmatch(f":maxdepth:1", line):
            lines.append(untouched_line + "\n")
            skip_empty = True
            lines.extend([f"  {major}.{i}\n" for i in range(minor, 0, -1)])
        elif not re.match(f"{major}" R"\.", line) and (not skip_empty or line != ""):
            lines.append(untouched_line)
    index_file.close()
    # Write new content
    index_file = open(os.path.join(path, "index.rst"), "w", encoding="utf-8")
    index_file.writelines(lines)
    index_file.close()

    # Check the version note in the minor version file
    # For the x.x.0 versions there are no note required, but 'Whats new?' section
    file = open(os.path.join(path, f"{major}.{minor}.rst"), "r")
    found_note = False
    for line in file:
        line = line.translate(str.maketrans("", "", " \n"))
        if re.fullmatch(f"{major}" R"\." f"{minor}" R"\." f"{rest}", line) or (
            re.fullmatch(R"Whatsnew\?", line) and rest == 0
        ):
            found_note = True
            break
    file.close()
    if not found_note:
        sys.tracebacklimit = 0
        if rest == 0:
            return "".join(
                [
                    colored(
                        f"\n'Whats new?' section for the {major}.{minor}.{rest} version is not available\n",
                        "red",
                    ),
                    f"Please add it to the file\n\n",
                    f"    docs/source/release-notes/{major}.{minor}.rst\n\n",
                    "Follow the style:\n\n",
                    f"    Whats new?\n",
                    f"    {'':-^10}\n",
                    "    Text\n",
                ]
            )
        else:
            return "".join(
                [
                    colored(
                        f"\nRelease notes for the {major}.{minor}.{rest} version are not available\n",
                        "red",
                    ),
                    f"Please add the note for the {major}.{minor}.{rest} version ",
                    "to the file\n\n",
                    f"    docs/source/release-notes/{major}.{minor}.rst\n\n",
                    "Follow the style:\n\n",
                    f"    {major}.{minor}.{rest}\n",
                    f"    {'':-^{len(version)}}\n",
                    "    Note text\n",
                ]
            )


@envelope(message="Checking if everything is committed and pushed")
def check_git_status(repo: git.Repo):
    """
    Check if everything is committed and pushed.

    Parameters
    ----------
    repo : git.Repo
        Git repository object.
    """
    status = repo.git.status()
    if "nothing to commit, working tree clean" not in status:
        sys.tracebacklimit = 0
        return "".join(
            [
                colored("\nThere are uncommitted changes\n", "red"),
                "Please commit them:\n\n",
                status,
            ]
        )
    if (
        "Your branch is up to date with" not in status
        and "HEAD detached at v" not in status
    ):
        sys.tracebacklimit = 0
        return "".join(
            [
                colored("\nThere are unpushed changes\n", "red"),
                "Please push them:\n\n",
                status,
            ]
        )


def main(version: str, root_dir: str, relax: bool = False):
    if version == "None":
        sys.tracebacklimit = 0
        raise ERROR(
            "".join(
                [
                    colored("\nVersion is undefined\n", "red"),
                    "For the make command use the syntax:\n\n",
                    "    make prepare-release VERSION=vx.x.x\n",
                ]
            )
        )
    elif version[0] != "v":
        sys.tracebacklimit = 0
        raise ERROR(colored("\n VERSION should start with lowercase 'v'.", "red"))

    version = version[1:]

    print(f"{'':=^{N}}\n{f'Preparing {version} release':^{N}}\n{'':=^{N}}")
    repo = git.Repo(search_parent_directories=True)

    # rtd - ready to deploy
    rtd = True

    rtd = check_release_notes(version=version, root_dir=root_dir, relax=relax) and rtd

    rtd = update_init(version=version, root_dir=root_dir, relax=relax) and rtd

    rtd = check_git_status(repo, relax=relax) and rtd
    if rtd:
        print(colored(f"{f'{version} ready to deploy':^{N}}", "green"))
    else:
        print(colored(f"{f'{version} not ready to deploy':^{N}}", "red"))
    print(f"{'':=^{N}}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        metavar="vx.x.x",
        type=str,
        required=True,
        help="Version to release",
    )
    parser.add_argument(
        "-rd",
        "--root-dir",
        metavar="PATH",
        type=str,
        required=True,
        help="Path to the root directory of the project",
    )
    parser.add_argument(
        "-r",
        "--relax",
        action="store_true",
        help="Relax the errors",
    )
    args = parser.parse_args()
    main(**vars(args))

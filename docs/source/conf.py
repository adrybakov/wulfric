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

import sys
from datetime import datetime
from os.path import abspath

from wulfric import __release_date__ as release_date
from wulfric import __version__ as version

sys.path.insert(0, abspath(".."))


##########################################################################################
##                                   Project metadata                                   ##
##########################################################################################
project = "Wulfric"
copyright = f"2023-{datetime.now().year}, Andrey Rybakov"
author = "Andrey Rybakov"
if ".dev" in version:
    switcher_version = "dev"
    github_version = "dev"
else:
    major, minor, rest = version.split(".")[0:3]
    switcher_version = f"{major}.{minor}"
    github_version = "main"


##########################################################################################
##                                      Extensions                                      ##
##########################################################################################
extensions = [
    "sphinx.ext.duration",  # Measure the time of the build
    "sphinx.ext.autodoc",  # Pull documentation from the docstrings
    "sphinx.ext.autosummary",  # Generate autodoc summaries
    "sphinx.ext.viewcode",  # Add links to highlighted source code
    "sphinx.ext.extlinks",  # Markup to shorten external links
    "sphinx.ext.intersphinx",  # Link to other projects’ documentation
    "sphinx.ext.doctest",  # For the doctests
    "sphinx.ext.mathjax",  # For latex-style math
    "sphinx_copybutton",  # Copybutton for the blocks
    "sphinx_design",  # For the design elements on the from page
    "numpydoc",  # For the numpy-style docstrings
]


##########################################################################################
##                                  Build configuration                                 ##
##########################################################################################
autosummary_generate = True
autodoc_member_order = "alphabetical"
smartquotes = False

# Avoid double generating the entries for the members of the class
numpydoc_class_members_toctree = False

# Fix problem with autosummary and numpydoc:
numpydoc_show_class_members = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]


##########################################################################################
##                                Options for HTML output                               ##
##########################################################################################
htmlhelp_basename = "wulfric"
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["wulfric.css"]

html_title = f"{project} v{version}"
html_favicon = "img/favicon.png"

# Theme specific options
html_theme_options = {
    "collapse_navigation": True,
    "use_edit_page_button": True,
    "navbar_center": ["version-switcher", "navbar-nav"],
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "switcher": {
        "version_match": switcher_version,
        "json_url": "https://docs.wulfric.org/en/latest/_static/versions.json",
    },
    "navbar_align": "left",
    "logo": {
        "image_light": "_static/logo.jpg",
        "image_dark": "_static/logo.jpg",
    },
    "header_links_before_dropdown": 4,
    "icon_links": [
        {
            "name": "Twitter",
            "url": "https://twitter.com/adrybakov",
            "icon": "fa-brands fa-twitter",
        },
        {
            "name": "GitHub",
            "url": "https://github.com/adrybakov/wulfric",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/wulfric/",
            "icon": "fa-solid fa-box",
        },
    ],
}


html_context = {
    "default_mode": "light",
    "display_github": True,  # Integrate GitHub
    "github_user": "adrybakov",  # Username
    "github_repo": "wulfric",  # Repo name
    "github_version": github_version,  # Version
    "doc_path": "docs/source",  # Path in the checkout to the docs root
}


##########################################################################################
##              Custom variables with access from .rst files and docstrings             ##
##########################################################################################
variables_to_export = [
    "project",
    "copyright",
    "version",
    "release_date",
]

frozen_locals = dict(locals())
rst_epilog = "\n".join(
    map(lambda x: f".. |{x}| replace:: {frozen_locals[x]}", variables_to_export)
)
del frozen_locals


##########################################################################################
##                                Dynamic external links                                ##
##########################################################################################
# Usage :issue:`123`
extlinks = {
    "DOI": ("https://doi.org/%s", "DOI: %s"),
    "numpy": (
        "https://numpy.org/doc/stable/reference/generated/numpy.%s.html",
        "numpy.%s",
    ),
    "matplotlib": (
        "https://matplotlib.org/stable/api/%s_api.html",
        "matplotlib.%s",
    ),
    "issue": ("https://github.com/adrybakov/wulfric/issues/%s", "issue #%s"),
}


##########################################################################################
##                                 Static external links                                ##
##########################################################################################

# Solution source:
# https://docutils.sourceforge.io/docs/ref/rst/directives.html#directives-for-substitution-definitions
# Usage: |Python|_
custom_links = {
    "Author": ("author", "https://adrybakov.com"),
    "ANSI": ("ANSI", "https://en.wikipedia.org/wiki/ANSI_escape_code"),
    "projwfc": ("projwfc.x", "https://www.quantum-espresso.org/Doc/INPUT_PROJWFC.html"),
    "QE": ("Quantum Espresso", "https://www.quantum-espresso.org"),
    "TB2J": ("TB2J", "https://tb2j.readthedocs.io/en/latest/"),
    "Vampire": ("Vampire", "https://vampire.york.ac.uk/"),
    "Wannier90": ("Wannier90", "http://www.wannier.org/"),
    "Python": ("Python", "https://python.org"),
    "NumPy": ("NumPy", "https://numpy.org/"),
    "SciPy": ("SciPy", "https://scipy.org/"),
    "matplotlib": ("matplotlib", "https://matplotlib.org/"),
    "termcolor": ("termcolor", "https://pypi.org/project/termcolor/"),
    "Python-installation": (
        "Python installation",
        "https://wiki.python.org/moin/BeginnersGuide/Download",
    ),
    "pytest": ("pytest", "https://docs.pytest.org/en/7.3.x/"),
    "hypothesis": ("hypothesis", "https://hypothesis.readthedocs.io/en/latest/"),
    "doctest": (
        "sphinx.ext.doctest",
        "https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html",
    ),
    "latex": ("LaTeX", "https://www.latex-project.org/"),
    "black": ("black", "https://black.readthedocs.io"),
    "array-like": (
        "array-like",
        "https://numpy.org/doc/stable/glossary.html#term-array-like",
    ),
    "termcolor": ("termcolor", "https://github.com/termcolor/termcolor"),
    "PearsonSymbol": ("Pearson symbol", "https://en.wikipedia.org/wiki/Pearson_symbol"),
    "matplotlibFocalLength": (
        "3D plot projection types",
        "https://matplotlib.org/stable/gallery/mplot3d/projections.html",
    ),
    "matplotlibSavefig": (
        "plt.savefig()",
        "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html",
    ),
    "matplotlibViewInit": (
        "view_init",
        "https://matplotlib.org/stable/api/_as_gen/mpl_toolkits.mplot3d.axes3d.Axes3D.view_init.html",
    ),
    "matplotlibLegend": (
        "legend()",
        "https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.legend.html",
    ),
    "matplotlibColor": (
        "matplotlib colors",
        "https://matplotlib.org/stable/tutorials/colors/colors.html",
    ),
    "array_interface": (
        "Array interface",
        "https://numpy.org/doc/stable/reference/arrays.interface.html#object.__array_interface__",
    ),
    "repo": ("Wulfric repository", "https://github.com/adrybakov/wulfric"),
    "numpydoc": ("numpydoc", "https://numpydoc.readthedocs.io/en/latest/format.html"),
    "plotly": ("Plotly", "https://plotly.com/python/"),
    "plotly-update-layout": (
        ".update_layout()",
        "https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html?highlight=update_layout#plotly.graph_objects.Figure.update_layout",
    ),
    "plotly-write-html": (
        ".write_html()",
        "https://plotly.com/python-api-reference/generated/plotly.io.to_html.html",
    ),
    "POSCAR": (
        "POSCAR",
        "https://www.vasp.at/wiki/index.php/POSCAR#Full_format_specification",
    ),
    "numba": ("Numba", "https://numba.pydata.org/"),
    "coprime": ("coprime", "https://en.wikipedia.org/wiki/Coprime_integers"),
    "good-commit-messages": ("good commit messages", "https://cbea.ms/git-commit/"),
    "sphinx": ("Sphinx", "https://www.sphinx-doc.org/en/master/"),
    "sphinx-autodoc": (
        "sphinx.ext.autodoc",
        "https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html",
    ),
    "sphinx-autosummary": (
        "sphinx.ext.autosummary",
        "https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html",
    ),
    "siesta": ("SIESTA", "https://siesta-project.org/siesta/"),
    "spglib": ("spglib", "https://spglib.readthedocs.io/en/stable/index.html"),
    "spglib-python": (
        "spglib's python interface",
        "https://spglib.readthedocs.io/en/stable/python-interface.html#",
    ),
}


rst_epilog += "\n".join(
    map(
        lambda x: f"\n.. |{x}| replace:: {custom_links[x][0]}\n.. _{x}: {custom_links[x][1]}",
        [i for i in custom_links],
    )
)

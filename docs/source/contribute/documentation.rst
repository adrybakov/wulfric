.. _contribute_docs:

*************
Documentation
*************

The documentation of Wulfric is built by |sphinx|_.

.. hint::

  The best way to get a feeling about how the documentation of Wulfric is
  structured and written is to read its source code in the "docs/source"
  directory and compare its content and structure with this webpage. If you
  have any questions, we encourage you to :ref:`contact us <user-support>`.

Documentation structure
=======================

The documentation is structured as follows

* API ("api" folder)

  Semi-automatically generated documentation of the source code. It is mostly
  built from the docstrings of the source code, using |sphinx-autodoc|_ and
  |sphinx-autosummary|_.

  It is located in the "docs/source/api" directory. Its content loosely follows
  the public structure of the package. Functions are recalled by hand, rather
  than automatically to improve readability. Please read existing files to get a
  feeling about the structure of API.

* User guide ("user-guide" folder)

  Hand-written |ReStructuredText-Sphinx|_ files with usage examples and
  explanation of the Wulfric's functionality. It is located in the
  "docs/source/user-guide" directory.

  We separate the user guide into several parts:

  - "usage" folder

    The usage guide is a detailed explanation of the functionality of Wulfric,
    grouped by concepts. The majority of examples (and doctests) are written
    there.

  - "library" folder

    Description of theory and algorithms behind Wulfric. Individual
    documents/folders are located there, however in the toctrees they are placed
    directly under the "user-guide" for better visibility (as opposed to being
    served from within the "library" page).

The rest of the documentation is located in the "docs/source" directory and it
includes, among other things:

* "conf.py" file

  The configuration file for |sphinx|_.

* "index.rst" file

  The main page of the documentation. It includes the table of contents and the
  introduction to Wulfric.

* "support.rst" file

  The page with the information about how users of Wulfric can get support.

* "release-notes" folder

  The release notes for each version of Wulfric.

* "contribute" folder

  Folder for the documentation of how to contribute to Wulfric.

* "img" folder

  All images should be placed here.


Docstrings
==========

All public classes and functions have to have a docstring.  The docstring has to
be written following the |numpydoc|_ style guide.

To get a feeling about the style you can read examples in the source code of Wulfric.

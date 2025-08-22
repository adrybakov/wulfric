.DEFAULT_GOAL := help

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build
VERSION="None"
NAME="None"
SCRIPT="all"
# Assuming that the Makefile is located in the root directory of the project
ROOT_DIR = $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

help:
	@echo "\x1b[31m"
	@echo "Please specify what do you want to do!"
	@echo "\x1b[0m"
	@echo "Available options are:\n"
	@echo "    help - show this message"
	@echo "    html - build the html docs"
	@echo "    clean-html - clean all files from docs and build html docs from scrutch"
	@echo "    html-from-zero - html from absolute zero (replot everything)"
	@echo "    doctest - run doctests"
	@echo "    clean - clean all files from docs and pip routines"
	@echo "    install - install the package"
	@echo "    test - execute unit tests"
	@echo "    test-all - execute full testing suite"
	@echo "    bravais-pictures - update pictures of bravais lattices"
	@echo "    docs-generate-images - update pictures for the docs"
	@echo "    requirements - installs all requirements (package + dev + tests + docs)"
	@echo

# $(O) is meant as a shortcut for $(SPHINXOPTS).
html:
	@python tools/produce-constantc-api.py
	@$(SPHINXBUILD) -M html "docs/$(SOURCEDIR)" "docs/$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean-html: clean install html
	@echo "Done"

html-from-zero: clean install bravais-pictures docs-generate-images html
	@echo "Done"

doctest:
	@$(SPHINXBUILD) -b doctest "docs/$(SOURCEDIR)" "docs/$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	-@rm -r docs/_build
	-@rm -r docs/source/api/generated
	-@rm -r docs/source/api/crystal/generated
	-@rm -r docs/source/api/_autosummary
	-@rm -r wulfric.egg-info
	-@rm -r build
	-@rm -r dist
	-@rm -r .env*/lib/python*/site-packages/wulfric*
	-@rm -r .env*/bin/wulfric*
	-@rm -r .venv*/lib/python*/site-packages/wulfric*
	-@rm -r .venv*/bin/wulfric*

install:
	@python3 -m pip install .

test:
	@pytest -s

test-all: html-from-zero test doctest
	@echo "Done"

bravais-pictures:
	@python3 tools/plot-bravais-lattices.py

docs-generate-images:
	@python3 tools/plot-repositories.py
	@python3 tools/plot-cell-choices.py
	@python3 tools/plot-cell-derivatives.py
	@python3 tools/plot-niggli-step-4.py

.ONESHELL:
requirements:
	@pip install -r requirements.txt --no-cache
	@pip install -r requirements-dev.txt --no-cache
	@pip install -r docs/requirements.txt --no-cache
	@pip install -r utest/requirements.txt --no-cache

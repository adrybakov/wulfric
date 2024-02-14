.DEFAULT_GOAL := help

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build
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
	@echo "    html-examples - update examples and build html docs"
	@echo "    doctest - run doctests"
	@echo "    clean - clean all files from docs and pip routines"
	@echo "    install - install the package"
	@echo "    test - execute unit tests"
	@echo "    test-all - execute full testing suite"
	@echo "    pip - publish the package to the PyPi index"
	@echo "    bravais-pictures - update pictures of bravais lattices"
	@echo "    prepare-release - prepare the package for release"
	@echo "    docs-pictures - update pictures for the docs"
	@echo "    venv - create and prepare a virtual environment in .venv folder"
	@echo

# $(O) is meant as a shortcut for $(SPHINXOPTS).
html:
	@$(SPHINXBUILD) -M html "docs/$(SOURCEDIR)" "docs/$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean-html: clean install html
	@echo "Done"

html-examples: bravais-pictures
	@$(SPHINXBUILD) -M html "docs/$(SOURCEDIR)" "docs/$(BUILDDIR)" $(SPHINXOPTS) $(O)

doctest:
	@$(SPHINXBUILD) -b doctest "docs/$(SOURCEDIR)" "docs/$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	-@rm -r docs/build
	-@rm -r docs/source/api/generated
	-@rm -r docs/source/api/crystal/generated
	-@rm -r docs/source/api/_autosummary
	-@rm -r wulfric.egg-info
	-@rm -r build
	-@rm -r dist
	-@rm -r .env*/lib/python3.11/site-packages/wulfric*
	-@rm -r .env*/bin/wulfric*

install:
	@python3 -m pip install .

test:
	@pytest -s

test-all: clean install test bravais-pictures html doctest
	@echo "Done"


.ONESHELL:
pip: prepare-release
	@read -p "Press Enter to publish to PyPI"
	-@rm -r dist
	-@rm -r build
	-@rm -r wulfric.egg-info
	@python3 -m build
	@python3 -m twine upload --repository pypi dist/* --verbose
	@git tag -a "v$(VERSION)" -m "Version $(VERSION)"
	@git push origin "v$(VERSION)"
	@git add src/wulfric/__init__.py
	@git commit -m "Post-release commit"
	@git push


bravais-pictures:
	@python3 tools/plot-bravais-lattices.py

prepare-release:
	@python3 -u tools/prepare-release.py -v $(VERSION) -rd $(ROOT_DIR) -r

docs-pictures:
	@python3 tools/plot-package-scheme.py
	@python3 tools/plot-atom-magnetic-properties.py

.ONESHELL:
venv:
	@rm -r .venv
	@python3 -m venv .venv
	@pip install -r requirements.txt --no-cache
	@pip install -r requirements-dev.txt --no-cache
	@pip install -r docs/requirements.txt --no-cache
	@pip install -r utest/requirements.txt --no-cache

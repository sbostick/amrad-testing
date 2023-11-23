SHELL      := /bin/bash
TAG        := $(shell git describe --tags --long --abbrev=8)
BUILD_TIME := $(shell date "+%F %H:%M:%S %Z (%z)")
TIMESTAMP  := $(shell date +%Y%m%d-%H%M%S)
BACKUP_DIR := ${HOME}/Library/CloudStorage/Dropbox/HAM-Radio
BACKUP_TGZ := ${BACKUP_DIR}/AMRAD-Questions-${TIMESTAMP}.tgz

tag:
	@echo ${TAG}

lint: pycodestyle pyruff pylint

# https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes
# E128 continuation line under-indented for visual indent
# E501 line too long (85 > 79 characters)
# E203 whitespace before ':'
# E402 module level import not at top of file
# E266 too many leading '#' for block comment
pycodestyle:
	pycodestyle --ignore E128,E501,E203,E402,E266 --verbose ./src/*.py

# https://pypi.org/project/ruff/0.0.47/
# E402 Module level import not at top of file
pyruff:
	@echo "+ Checking source with ruff (linter written in Rust)"
	ruff --verbose --ignore E402 --cache-dir /tmp/ruff_cache .

# https://pylint.org/
# https://pylint.pycqa.org/en/latest/
pylint:
	@echo "+ Checking source with pylint (most comprehensive and popular)"
	@[[ -e pylintrc ]] || pylint --generate-rcfile > pylintrc
	pylint --rcfile pylintrc ./src/*.py
	@echo

tech:
	mkdir -p ./OUTPUT/Tech/
	./src/parser.py --verbose \
		--input-file ./INPUT/Tech/Questions.txt \
		--output-file ./OUTPUT/Tech/Questions.json
	jq . -r ./OUTPUT/Tech/Questions.json > /dev/null

general:
	mkdir -p ./OUTPUT/General/
	./src/parser.py --verbose \
		--input-file ./INPUT/General/Questions.txt \
		--output-file ./OUTPUT/General/Questions.json
	jq . -r ./OUTPUT/General/Questions.json > /dev/null

extra:
	mkdir -p ./OUTPUT/Extra/
	./src/parser.py --verbose \
		--input-file ./INPUT/Extra/Questions.txt \
		--output-file ./OUTPUT/Extra/Questions.json
	jq . -r ./OUTPUT/Extra/Questions.json > /dev/null

backup:
	tar -czf ${BACKUP_TGZ} --exclude .git .
	tar -tzf ${BACKUP_TGZ}
	ls -lh ${BACKUP_TGZ}

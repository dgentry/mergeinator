## Makefile usage:
## `make install`

#
# Debugging Stuff
#

# This target is handy for figuring out the value of a macro and how it got that way.
# For example, `make print-TGT`
print-%: ; @$(error $* is $($*) ($(value $*)) (from $(origin $*)))

##
##To add Make debugging info to the log, use "make DUMP=1 <other args>"
##
ifdef DUMP
OLD_SHELL := $(SHELL)
SHELL = $(warning [$@])$(OLD_SHELL) -x
endif

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    # You're on Linux!
endif
ifeq ($(UNAME_S),Darwin)
    # You're on Darwin
endif


help: ## Show this help.
	@fgrep -h "##" Makefile | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: prereq-packages
prereq-packages:
	python3 -m pip install -r requirements.txt

.PHONY: install
install:  ## Install to your system or virtualenv.
install: prereq-packages
	python3 -m pip install .

.PHONY: develop
develop:  ## Install to your system or virtualenv, using a symlink so edits take immediate effect.
develop: prereq-packages
	python3 -m pip install -e .

.PHONY: uninstall
uninstall:  ## Remove 'merge' from your system or virtualenv
	python3 -m pip uninstall -y mergeinator

.PHONY: clean
clean: ## Removes ErrorLog, wheels, TAGS, and emacs auto-save files (*~) everywhere.
	rm -f ErrorLog *.whl TAGS
	rm -rf __pycache__ mergeinator.egg-info
	find . -name \*~ | xargs rm -f

.PHONY: cleaner
cleaner: ## Clean, plus removes .pyc's everywhere (even those
cleaner: ## lurking in any virtual environment you might have).
cleaner: clean
	rm -rf .pytest_cache
	find . -name \*.pyc | xargs rm -f

.PHONY: distclean
distclean: ## Cleaner, plus removes virtualenvs, .orig files, and autosave files
distclean: cleaner
	find . -name \#\*\# -o -name \*.orig | xargs rm -f
	rm -rf venv

.PHONY: tags
tags: ## Refresh tags file for whole project.
	ctags -e -R --exclude=venv .

.PHONY: profile
profile: ## Runs the app and produces profiling data

.PHONY: test
test:	## Invoke pytest to run tests
	py.test

.PHONY: viewprofile
viewprofile:
	pyprof2calltree -k -i main.profile

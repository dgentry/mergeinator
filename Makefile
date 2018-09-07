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

.PHONY: install
install:  ## Install to your system or virtualenv.
	pip install --no-deps .

.PHONY: develop
develop:  ## Install to your system or virtualenv, using a symlink so edits take immediate effect.
	pip install --no-deps -e .

.PHONY: uninstall
uninstall:  ## Remove 'merge' from your system or virtualenv
	pip uninstall -y mergeinator

.PHONY: clean
clean: ## Removes old tpg.logs (those with date-times) and emacs auto-save files (*~) everywhere.
	rm -f ErrorLog tpg.log.* *.whl TAGS test-requirements.txt
	rm -rf __pycache__ mergeinator.egg-info
	find . -name \*~ | xargs rm -f

.PHONY: cleaner
cleaner: ## Clean, plus removes .mats, tpg.log, and .pyc's everywhere (even those
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
	py.test --pyargs mergeinator

.PHONY: viewprofile
viewprofile:
	pyprof2calltree -k -i main.profile

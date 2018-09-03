## POP Makefile usage:
## `make setup`, then `make`
##

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

requirements.txt: ## Create this starting with a clean virtualenv.  Then
requirements.txt: ## run this after you add your new packages to the virtualenv.
requirements.txt: $(KIVY_PACKAGES) Makefile
	# depends on the makefile because of these echo things below
	echo "# 0 This file is automatically generated by the Makefile" > requirements.txt
	echo "# 1 so any edits you make will eventually be overwritten." >> requirements.txt
	echo "# 2 Instead, add (only) the packages you need to kivy's virtualenv" >> requirements.txt
	echo "# 3 using 'kivy -m pip install <package>' then" >>requirements.txt
	echo "# 4 'make requirements.txt'" >>requirements.txt
	python -m pip freeze >> requirements.txt
	# Create the "-windows" version by removing scipy and numpy
	# (which have to be installed by hand).
	grep -v scipy requirements.txt | grep -v numpy >rw.tmp
	# And add the additional stuff for windows.
	cat rw.tmp req-add-for-windows.txt | sort -f >requirements-windows.txt
	rm -f rw.tmp

.PHONY: setup
setup: ## No automated setup provided yet.
	echo "You'll need brew."

.PHONY: install
install:  ## Install to your system
	echo "Depends on your system."

.PHONY: clean
clean: ## Removes old tpg.logs (those with date-times) and emacs auto-save files (*~) everywhere.
	rm -f ErrorLog tpg.log.* *.whl TAGS test-requirements.txt
	rm -rf __pycache__
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
	rm tmp-requirements.txt
	rm -rf venv

.PHONY: shellcheck
shellcheck: ## Check shell scripts for non-portability and other potential bugs.
shellcheck: $(SHELLSCRIPTS)
	shellcheck $(SHELLCHECK_OPTS) --color=never $(SHELLSCRIPTS)

shellcheck-color:  ## Same as shellcheck, but with color output.
shellcheck-color:  $(SHELLCHECK)
	shellcheck $(SHELLCHECK_OPTS) --color=always $(SHELLSCRIPTS)

.PHONY: tags
tags: ## Refresh tags file for whole project.
	ctags -e -R --exclude=venv .

.PHONY: profile
profile: ## Runs the app and produces profiling data

.PHONY: test
test:
	py.test

.PHONY: viewprofile
viewprofile:
	pyprof2calltree -k -i main.profile

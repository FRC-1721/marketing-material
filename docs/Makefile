SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Refactored from minimal makefile

all: patches latexpdf

# Build custom patches
patches:
	mkdir -p uniforms/patches/renders
	cd uniforms/patches && python patchbuilder.py

clean:
	git clean -fdX 

latexpdf: Makefile
	@$(SPHINXBUILD) -M latexpdf "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

html: patches Makefile
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

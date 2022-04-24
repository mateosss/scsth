BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/source
OUTPUTDIR=$(BASEDIR)/output
TEMPLATEDIR=$(INPUTDIR)/templates
STYLEDIR=$(BASEDIR)/style
SCRATCHDIR=$(BASEDIR)/scratch
EXTERNALDIR=$(BASEDIR)/external

BIBFILE=$(INPUTDIR)/references.bib

help:
	@echo ''
	@echo 'Makefile for the Markdown thesis'
	@echo ''
	@echo 'Usage:'
	@echo '   make install                     install pandoc plugins'
	@echo '   make pdfull                      generate a PDF file with updated bib'
	@echo '   make pdfast                      generate a PDF file'
	@echo '   make tex                         generate a Latex file'
	@echo ''
	@echo ''
	@echo 'get local templates with: pandoc -D latex/html/etc'
	@echo 'or generic ones from: https://github.com/jgm/pandoc-templates'
# TODO@low@style: here we have some talk about pandoc templates ^

UNAME := $(shell uname)
ifeq ($(UNAME), Linux)
install:
	bash $(BASEDIR)/install_linux.sh
else ifeq ($(shell uname), Darwin)
install:
	bash $(BASEDIR)/install_mac.sh
endif

md:
	gpp -n -U "" "" "(" "," ")" "(" ")" "#" "" \
    -M "<!-- #\w" "-->\n" " " " " "-->\n" "(" ")" \
    +s "\"" "\"" "\\" \
		-I $(INPUTDIR)/ \
    $(INPUTDIR)/main.md > $(OUTPUTDIR)/thesis.md

# TODO@low: Define HTML, PDF, TEX macros and use them in sourcecode for conditional
# stuff like: BEGIN_FORMULA(), which would pick $$ or \begin{align} based on
# type of compilation

# TODO@low: Generar buenas macros con gpp para el uso de imagenes, margins, etc
# ver https://narkive.com/WEV34A29:3.378.60
# Olvidarme del visor de vscode, a ese lo puedo usar sobre el archivo ya
# procesado por gpp y chau

tex: md
	pandoc \
	--output="$(OUTPUTDIR)/thesis.tex" \
	--template="$(STYLEDIR)/template.tex" \
	--include-in-header="$(EXTERNALDIR)/01mf02/pandocfilters/header.tex" \
	--include-in-header="$(STYLEDIR)/preamble.new.tex" \
	--listings \
	--top-level-division=part \
	--metadata=link-citations:true \
	--filter=external/01mf02/pandocfilters/all.py \
	--bibliography="$(BIBFILE)" \
	--biblatex \
	--citeproc \
	--verbose \
	"$(OUTPUTDIR)/thesis.md"
	2> $(OUTPUTDIR)/logs/pandoc.tex.log

LATEXCMD = xelatex -halt-on-error \
	-output-directory=$(OUTPUTDIR)/latex $(OUTPUTDIR)/thesis.tex 2>&1 && \
	mv $(OUTPUTDIR)/latex/thesis.pdf $(OUTPUTDIR)/ \
	| tee output/logs/xelatex.pdf.log

pdfast: tex
		$(LATEXCMD)

pdfull: tex
		$(LATEXCMD)
		cd output/latex && bibtex thesis && cd ..
		$(LATEXCMD)
		$(LATEXCMD)
		cp output/thesis.pdf output/thesis.raw.pdf
		pdftk output/thesis.raw.pdf cat 1 3-end output output/thesis.pdf
		rm output/thesis.raw.pdf

pdf: pdfull

all: pdf

.PHONY: help install md tex pdfull pdfast

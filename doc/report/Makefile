BIBTEX=bibtex
LATEX=latex
PDFLATEX=pdflatex


all: msc-report

msc-report: msc-report.tex
	$(LATEX) $@
	$(PDFLATEX) $@
	$(BIBTEX) $@
	$(LATEX) $@
	$(PDFLATEX) $@
	$(LATEX) $@
	$(PDFLATEX) $@
	-rm -rf *.aux *.log

clean:
	-rm -rf *.dvi *.pdf

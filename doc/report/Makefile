BIBTEX=bibtex
LATEX=latex
PDFLATEX=pdflatex
DVIPSPDF=dvips -Ppdf


all: msc-report

msc-report: msc-report.tex
	$(LATEX) $@
#	$(PDFLATEX) $@
	$(DVIPSPDF) $@
	$(BIBTEX) $@
	$(LATEX) $@
#	$(PDFLATEX) $@
	$(DVIPSPDF) $@
	$(LATEX) $@
#	$(PDFLATEX) $@
	$(DVIPSPDF) $@
	-rm -rf *.aux *.log

clean:
	-rm -rf *.dvi *.pdf *.aux *.log

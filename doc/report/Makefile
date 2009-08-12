BIBTEX=bibtex
LATEX=latex
PDFLATEX=pdflatex
DVIPSPDF=dvips -Ppdf
PS2PDF=ps2pdf


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
	$(PS2PDF) msc-report.ps msc-report.pdf
	-rm -rf *.aux *.log

clean:
	-rm -rf *.dvi *.pdf *.aux *.log

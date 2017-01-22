# TARGETS

.PHONY: hw dis img render

hw:
	make render cat=hw n=${n}
	mv src/hw/hw${n}-raw.tex rendered/hw${n}/
	open rendered/hw${n}/hw${n}.pdf
	open rendered/hw${n}/hw${n}-sol.pdf

dis:
	make render cat=dis n=${n}
	open rendered/dis${n}/dis${n}.pdf
	open rendered/dis${n}/dis${n}-sol.pdf

img:
	./generate-img ${n}

render:
	ruby generate.rb ${cat} ${n}
	mkdir -p rendered/${cat}${n}
	pdflatex -jobname=rendered/${cat}${n}/${cat}${n} src/${cat}/${cat}${n}.tex
	pdflatex -jobname=rendered/${cat}${n}/${cat}${n}-sol src/${cat}/${cat}${n}-sol.tex

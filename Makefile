# TARGETS

.PHONY: hw dis img render

# Usage: make hw n=<str>
hw:
	make render cat=hw n=${n}
	mv src/hw/hw${n}-raw.tex rendered/hw${n}/
	open rendered/hw${n}/hw${n}.pdf
	open rendered/hw${n}/hw${n}-sol.pdf

# Usage: make dis n=<str>
dis:
	make render cat=dis n=${n}
	open rendered/dis${n}/dis${n}.pdf
	open rendered/dis${n}/dis${n}-sol.pdf

# Usage: make render n=<str>
img:
	./utils/generate-img ${n}

# Usage: make render cat=<str> n=<str>
render:
	mkdir -p src/${cat}/${cat}${n}_data
	python utils/generate.py ${cat} ${n}
	mkdir -p rendered/${cat}${n}
	rm -rf rendered/${cat}${n}/data
	mv src/${cat}/${cat}${n}_data/ rendered/${cat}${n}/data
	pdflatex -jobname=rendered/${cat}${n}/${cat}${n} src/${cat}/${cat}${n}.tex
	pdflatex -jobname=rendered/${cat}${n}/${cat}${n}-sol src/${cat}/${cat}${n}-sol.tex
	rm -f {rendered/**/*.aux,rendered/**/*.log,rendered/**/*-img*.pdf}

# Usage: make piazza n=<str>
piazza:
    node utils/piazza.js ./config.json n=${n}

clean:
	rm -f {src/**/hw*-sol.tex,src/**/hw*-raw.tex,src/**/hw*-img*.tex}

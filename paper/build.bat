pdflatex -interaction nonstopmode -shell-escape paper.tex
bibtex paper
pdflatex -interaction nonstopmode -shell-escape paper.tex
pdflatex -interaction nonstopmode -shell-escape paper.tex
pdflatex -interaction nonstopmode -shell-escape paper.tex
qpdf --linearize --newline-before-endstream paper.pdf tmp/paper.pdf
mv tmp/paper.pdf paper.pdf
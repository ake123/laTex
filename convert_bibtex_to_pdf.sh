#!/bin/bash

# Loop through all .bib files in the current directory
for bibfile in *.bib; do
    # Extract the filename without extension
    filename="${bibfile%.*}"

    # Create a basic .tex file that uses the .bib file
    cat > $filename.tex << EOF
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{biblatex}
\addbibresource{$bibfile}
\begin{document}
\nocite{*}
\printbibliography
\end{document}
EOF

    # Run pdflatex and bibtex to generate the PDF
    pdflatex $filename.tex
    bibtex $filename
    pdflatex $filename.tex
    pdflatex $filename.tex

    # Clean up auxiliary files
    rm $filename.aux $filename.bbl $filename.blg $filename.log $filename.tex
done

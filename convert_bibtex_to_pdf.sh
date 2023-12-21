#!/bin/bash

# Create the pdfs directory if it does not exist
mkdir -p pdfs

# Loop through all .bib files in the current directory
for bibfile in *.bib; do
    # Extract the filename without extension
    filename="${bibfile%.*}"

    # Create a basic .tex file that uses the .bib file
    cat > $filename.tex << EOF
\documentclass[a4paper,12pt]{article}
\usepackage[verbose,nomarginpar,a4paper,margin=25mm]{geometry}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{textcomp}
\usepackage[datesep=.]{datetime2}
\usepackage[url=false, doi=false, isbn=false, style=alphabetic, maxnames=10, sorting=ydnt, texencoding=utf8]{biblatex}
\addbibresource{lahti.bib}


% use entry keys verbatim from the bib file
\DeclareFieldFormat{labelalpha}{\thefield{entrykey}}
\DeclareFieldFormat{extraalpha}{}



% highlight authors matching the given first and last names
\renewcommand*{\mkbibnamegiven}[1]{%
	\ifthenelse{\equal{\namepartgiven}{\filterfirstname} \and \equal{\namepartfamily}{\filterlastname}}%
	{\mkbibbold{#1}}%
	{#1}%
}
\renewcommand*{\mkbibnamefamily}[1]{%
	\ifthenelse{\equal{\namepartgiven}{\filterfirstname} \and \equal{\namepartfamily}{\filterlastname}}%
	{\mkbibbold{#1}}%
	{#1}%
}
\newcommand{\filterfirstname}{Leo}
\newcommand{\filterlastname}{Lahti}



% separate entries to their corresponding (complex) categories
% edited = there is an editor field, and the type is either book or proceedings
% tech / phd = filter by type field
% misc = misc entry type, or a type field with "mathesis"
\DeclareBibliographyCategory{edited}
\DeclareBibliographyCategory{tech}
\DeclareBibliographyCategory{phd}
\DeclareBibliographyCategory{misc}
\AtDataInput{%
	\ifthenelse{\not \ifnameundef{editor} \and \( \ifentrytype{book} \or \ifentrytype{proceedings} \)}%
	{\addtocategory{edited}{\thefield{entrykey}}}%
	{}%
	\ifthenelse{\iffieldequalstr{type}{techreport}}%
	{\addtocategory{tech}{\thefield{entrykey}}}%
	{}%
	\ifthenelse{\iffieldequalstr{type}{phdthesis}}%
	{\addtocategory{phd}{\thefield{entrykey}}}%
	{}%
	\ifthenelse{\iffieldequalstr{type}{mathesis} \or \ifentrytype{misc}}%
	{\addtocategory{misc}{\thefield{entrykey}}}%
	{}%
}



% main bib file
\addbibresource{lahti.bib}

% there are no citations, but every bib entry is needed in the bibliography
\nocite{*}


\begin{document}

\begin{center}
	\huge\textbf{List of publications}\\
	\large\textit{Leo Lahti, PhD}\\
	\small{\today}
\end{center}

\printbibliography[title={Edited volumes}, category=edited]
\printbibliography[title={Journal articles}, type=article]
\printbibliography[title={Book chapters}, type=incollection]
\printbibliography[title={Conference proceedings}, type=inproceedings]
\printbibliography[title={Technical reports}, category=tech]
\printbibliography[title={PhD theses}, category=phd]
\printbibliography[title={Miscellaneous}, category=misc]

\end{document}
EOF

    # Run pdflatex and bibtex to generate the PDF
    pdflatex $filename.tex
    bibtex $filename
    pdflatex $filename.tex
    pdflatex $filename.tex

   # Move the PDF and log file to the pdfs directory if the PDF exists
    if [[ -f "$filename.pdf" ]]; then
        mv "$filename.pdf" "$filename.log" pdfs/
    else
        echo "PDF for $filename not generated."
        # Move the log file for inspection
        mv "$filename.log" pdfs/
    fi

    # Clean up auxiliary files
    rm -f $filename.aux $filename.bbl $filename.blg $filename.run.xml $filename.tex
done

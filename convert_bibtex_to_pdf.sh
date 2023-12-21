#!/bin/bash

# Create the pdfs directory if it does not exist
mkdir -p pdfs

# Loop through all .bib files in the current directory
for bibfile in *.bib; do
    # Extract the filename without extension
    filename="${bibfile%.*}"

    # Create a basic .tex file that uses the .bib file
    cat > $filename.tex << EOF

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

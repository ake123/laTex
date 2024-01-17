import subprocess
import pybtex.database.input.bibtex as bibtex_input

# Define your .bib and .tex file names
bib_file = "lahti.bib"
tex_file = "lahti.tex"

# Load the BibTeX file
parser = bibtex_input.Parser()
bib_data = parser.parse_file(bib_file)

# Generate a LaTeX file with the bibliography
with open(tex_file, "a") as tex_file:
    tex_file.write("\n\n\\begin{document}\n\n")
    for key in bib_data.entries.keys():
        tex_file.write(f"\\cite{{{key}}}\n")
    tex_file.write("\n\n\\bibliographystyle{plain}\n")
    tex_file.write("\\bibliography{" + bib_file.split(".")[0] + "}\n")
    tex_file.write("\n\n\\end{document}\n")

# Compile the LaTeX document to generate the PDF
try:
    subprocess.run(["pdflatex", tex_file])
    subprocess.run(["bibtex", tex_file.split(".")[0]])
    subprocess.run(["pdflatex", tex_file])
    subprocess.run(["pdflatex", tex_file])
    print(f'Successfully generated {tex_file.split(".")[0]}.pdf')
except Exception as e:
    print(f"Error: {e}")

import os
import subprocess
import pybtex.database.input.bibtex as bibtex_input

script_dir = os.path.dirname(os.path.abspath(__file__))

# Define your .bib and .tex file names
bib_file = os.path.join(script_dir, "lahti.bib")
tex_file = os.path.join(script_dir, "lahti.tex")

# Specify the output PDF file path
pdf_file_path = os.path.join(script_dir, "lahti.pdf")

# Load the BibTeX file
parser = bibtex_input.Parser()
bib_data = parser.parse_file(bib_file)

# Generate a LaTeX file with the bibliography
with open(tex_file, "w") as tex_file:
    tex_file.write("\\documentclass[a4paper,12pt]{article}\n")
    tex_file.write("\\usepackage[verbose,nomarginpar,a4paper,margin=25mm]{geometry}\n")
    tex_file.write("\\usepackage[utf8]{inputenc}\n")
    tex_file.write("\\usepackage[T1]{fontenc}\n")
    tex_file.write("\\usepackage{lmodern}\n")
    tex_file.write("\\usepackage{textcomp}\n")
    tex_file.write("\\usepackage[datesep=.]{datetime2}\n")
    tex_file.write(
        "\\usepackage[backend=biber, style=alphabetic, maxnames=10, sorting=ydnt, texencoding=utf8]{biblatex}\n"
    )
    tex_file.write("\\addbibresource{" + bib_file + "}\n")
    tex_file.write("\\begin{document}\n")
    tex_file.write("\\nocite{*}\n")
    tex_file.write("\\printbibliography\n")
    tex_file.write("\\end{document}\n")

# Compile the LaTeX document to generate the PDF
try:
    subprocess.run(["pdflatex", tex_file])
    subprocess.run(["biber", tex_file.split(".")[0]])
    subprocess.run(["pdflatex", tex_file])
    subprocess.run(["pdflatex", tex_file])

    # Move the generated PDF to the specified output path
    os.rename(tex_file.split(".")[0] + ".pdf", pdf_file_path)

    print(f"Successfully generated PDF at: {pdf_file_path}")
except Exception as e:
    print(f"Error: {e}")

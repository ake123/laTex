import os
import subprocess
import pybtex.database.input.bibtex as bibtex_input

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the .bib and .tex file paths
bib_file = os.path.join(script_dir, "lahti.bib")

# Specify the path to the .tex file one level up from the script folder
tex_file = os.path.join(os.path.dirname(script_dir), "lahti.tex")

# Define the output PDF file path as 'lahti.pdf' one level up from the script folder
pdf_file_path = os.path.join(os.path.dirname(script_dir), "lahti.pdf")

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

    # Move the generated PDF to the specified output path
    os.rename(tex_file.split(".")[0] + ".pdf", pdf_file_path)

    print(f"Successfully generated PDF at: {pdf_file_path}")
except Exception as e:
    print(f"Error: {e}")

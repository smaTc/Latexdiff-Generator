# Latexdiff-Generator
Small python script that allows to generate the Latexdiff files of versions of a project automatically in a new project. 

Note: The project structure must be the same. Only the content of the `.tex` files can be changed.

## Requirements
Python and Latexdiff (and maybe other Latex dependencies, if texlive is installed completely everything should work)

## Usage
Execute `python LatexdiffGenerator.py Project1 Project2 NewProject` to generate the Latexdiff project.

Note: The third `NewProject` parameter is optional if you want a custom name or path. Default name is `latexdiff-doc` and it will be created in the current working directory.

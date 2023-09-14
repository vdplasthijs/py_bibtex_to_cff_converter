# Python implementation of bibtext to cff citation file converter
Convert bibtex citation files to cff file for compatibility with github citations

## Installation:
- `pip install bibtexparser==2.0.0b2`

## How to use:
- Use functions from `citation_conversion_utilities.py`. 
- Example of how to use this in `Example conversion.ipynb`. 
- Recommended to also include the original `.bib` file in the repo; Github's cff to bib conversion is not perfect.

## Info about cff files:
- Github explainer & examples: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files
- Primer on cff files & create from scratch online: https://citation-file-format.github.io/
- Overview of cff software: https://github.com/citation-file-format/citation-file-format/blob/main/README.md#tools-to-work-with-citationcff-files-wrench

## Alternatives:
Given a bibtex file `cite_source.bib` that we want to convert to `cite_target.cff`. 

### Julia:
- Bibliography.jl

Then:

`using Bibliography`

`imported_bib = import_bibtex("cite_source.bib")`

`export_cff(imported_bib["key"]; destination="cite_target.cff")`

where `"key"` is the bibtex entry for that citation. 


Note: if you get an `ERROR: ArgumentError: input string is empty or only contains whitespace` error, then it's likely because some required field (for cff) was not filled out in the bibtex. Find out which field is needed by seeing in the error message which line in `cff.jl` threw the error. 

# Python implementation of bibtext to cff citation file converter
Convert bibtex citation files to cff file for compatibility with github citations

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

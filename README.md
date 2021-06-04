# filibuster: counting how many times certain words occur in docx and pdf files

Counts how many times each of a list of words occurs in all of the docx and pdf files in a single directory.

## why?

Requested by an Assistive Technologist for analysing about 60 .docx and .pdf
files for keywords. His first name is Fil. Hence the script's name
'filibuster.py'.

## how to use

You put your list of search words into a file called search_terms.txt. Put all the pdf and docx files into the same directory as the search_terms.txt file. Put the python script filibuster.py into the same directory. Then type 'python filibuster.py' from a terminal opened in that directory. All the words in search_terms.txt are searched for in all of the .pdf and .docx files and the total count for each search term output.

## dependencies

.docx files are processed using the docx2txt library.
.pdf files are process using the PyPDF2 library.

## contacts
matt@mattoppenheim.com


# filibuster: counting how many times certain words occur in docx and pdf files

Counts how many times each of a list of words occurs in all of the docx and pdf files in a single directory.
Outputs:
Count of how many each word occurs in each file.
Count of how many files each word occurs in.
Total number of times each word is found.

## why?

Requested by an Assistive Technologist for analysing about 60 .docx and .pdf
files for keywords. His first name is Fil. Hence the script's name
'filibuster.py'.

## quickstart

Install Python3. Click all the options to install pip when you do this and to add python to the path.

Install the dependencies using pip3 install -r requirements.txt.

If this doesn't work, type:

pip install click PyPDF2 click docx2txt pandas

Put all your .docx and .pdf files into the same directory as filibuster.py.

Make a list of search terms and put them in a file called search_terms.txt.

Run using: python3 filibuster.py

## how to use, detailed

Install Python3. Click the options to add Python to your path and to install pip.

Unpack the zip file from this repository to a convenient directory. Open a command line terminal in
this directory.

There are a few libraries that the script needs that are not included with the
default Python installation. Install these libraries using the command:

**pip3 install -r requirements.txt**

In the directory containing the file requirements.txt.

If you don't have pip3 installed, you may have not ticked that option when installing Python. For more details and pictures of what to do, have a look at [this website](https://medium.com/swlh/solved-windows-pip-command-not-found-or-pip-is-not-recognized-as-an-internal-or-external-command-dd34f8b2938f) and re-install Python with the options to install pip selected and adding Python to the system path selected.

Sometimes using pip does not work as I may have built the script using an older or newer version of Python than you have installed. If you get errors type:

**pip install click PyPDF2 click docx2txt pandas**

To install the dependencies this way.

Put all of the .docx and .pdf files that you want to search through into a
single directory. Either the same directory as the filibuster.py script or
another one of your choice.

Put your list of search terms into a single file called search_terms.txt in the
same directory as the .pdf and .docx files.

If the .docx and .pdf files are in the same directory as the script
filibuster.py, run the script using:

**python3 filibuster.py**

If the .docx and .pdf files and search_terms.txt files are in a different
directory, use the command:

**python3 filibuster.py --dir=path to files**

## notes

The script looks for complete words. It will not count words that are
substrings of longer words. e.g. if you are searching for 'the', then 'theatre'
will not be counted as 'the' is a substring of 'theatre'. Punctuation marks are
removed before searching, so 'the,' or '!the' will be counted.

The output could do with some cosmetic tidying, but I want to get this out to
the end user.

## test files

There is a directory called 'test' with some files used for testing the script
with.

## dependencies

These are all in the requirements.txt file.

.docx files are processed using the docx2txt library.
.pdf files are process using the PyPDF2 library.
pandas is used to collate the results
click is used for the command line interface

## contacts

matt@mattoppenheim.com

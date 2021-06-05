''' filibuster.py
Searches through all .pdf and .docx files in the directory that the script is 
run from for keywords contained in the file search_terms.txt in the same 
directory.
Outputs a list of the search terms and how many times these occur in all of
the documents. Counts every occurrence of the search term, not how many 
documents it appears in.

Matt Oppenheim June 2021
'''
import docx2txt
import logging
import os
import pandas as pd
import PyPDF2

DIR = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logging.info('started filibuster')
SEARCH_TERMS_FILENAME = 'search_terms.txt'


def count_search_terms(text, search_term):
    ''' Update df with how many times search_terms occurs in text. '''
    # remove trailing newline characters from the search terms
    search_term = search_term.strip()
    search_term_count = text.count(search_term.lower())
    logging.info('{} occurs {} times'.format(search_term, search_term_count))
    return search_term_count

    

def create_dataframe(search_terms):
    ''' Create pandas dataframe to store found terms in. '''
    col_names = search_terms.copy()
    col_names.insert(0, 'doc_name')
    df = pd.DataFrame(columns=col_names)
    # df.set_index('doc_name')
    logging.debug('df_head: {}'.format(df.head()))
    return df


def docx_to_text(filepath):
    ''' Extract text from Word docx files. '''
    logging.info('  processing Word file: {}'.format(os.path.basename(filepath)))
    text = docx2txt.process(os.path.join(DIR, filepath))
    return text


def exit_code(message):
    ''' exits '''
    print(message)
    print("exiting")
    raise SystemExit


def found_search_terms(file_text, search_terms):
    ''' Create list of how many of each search term is found in file_text. '''
    # text and search terms are made lower case to make the process case insensitive
    found_terms_count = []
    file_text = file_text.lower().split()
    for search_term in search_terms:
        search_term_count = count_search_terms(file_text, search_term)
        found_terms_count.append(search_term_count)
    logging.debug('found_terms_count: {}'.format(found_terms_count))
    return found_terms_count


def get_filepath(dir, filename):
    ''' Create filepath. '''
    return os.path.join(DIR, filename)


def get_search_terms():
    ''' Extract list of search terms from file.'''
    search_terms = []
    with open(os.path.join(DIR, SEARCH_TERMS_FILENAME), 'r') as search_terms_file:
        for search_term in search_terms_file:
            search_terms.append(search_term.strip())
    return search_terms
        

def pdf_to_text(filepath):
    ''' Extract text from pdf files. '''
    logging.info('  processing pdf file: {}'.format(os.path.basename(filepath)))
    with open(filepath, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        all_text = ''
        for page in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page) 
            page_text = page.extractText()
            all_text = '{} {}'.format(all_text, page_text)
    return all_text


def update_df(df, filename, found_terms_list):
    ''' Add the found_terms_list as a new row to the dataframe. '''
    found_terms_list.insert(0, filename)
    df.loc[len(df)] = found_terms_list
    return df


def main():
    search_terms_filepath = os.path.join(DIR, SEARCH_TERMS_FILENAME)
    if not os.path.exists(search_terms_filepath):
        exit_code('search terms file does not exist: {}'.format(search_terms_filepath))
    search_terms = get_search_terms()
    logging.info('searching for Word and pdf files in: {}'.format(DIR))
    df = create_dataframe(search_terms)
    for filename in os.listdir(DIR):
        logging.info('found {}'.format(filename))

        if filename.endswith('.docx'):
            filepath = get_filepath(DIR, filename)
            file_text = docx_to_text(filepath)
            found_terms_list = found_search_terms(file_text, search_terms)
            df = update_df(df, filename, found_terms_list)

        if filename.endswith('.pdf'):
            filepath = get_filepath(DIR, filename)
            file_text = pdf_to_text(filepath)
            found_terms_list = found_search_terms(file_text, search_terms)
            df = update_df(df, filename, found_terms_list)

    logging.debug('df_head: {}'.format(df.head()))

if __name__ == '__main__':
    main()
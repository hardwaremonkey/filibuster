''' filibuster.py
Searches through all .pdf and .docx files in the directory that the script is 
run from for keywords contained in the file search_terms.txt in the same 
directory.
Outputs a list of the search terms and how many times these occur in all of
the documents. Counts every occurrence of the search term, not how many 
documents it appears in.

Matt Oppenheim June 2021
'''
import click
import docx2txt
import logging
import os
import pandas as pd
import PyPDF2
import re

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.info('started filibuster')
SEARCH_TERMS_FILENAME = 'search_terms.txt'


def clean_text(text):
    ''' Make all text lower case and replaces punctuation marks with spaces. '''
    output_text = ''
    logging.debug('*** unclean_text\n{}'.format(text))
    for word in text.split():
        word = word.lower()
        # replace all non-alphanumeric or non-whitespace characters with space
        word = re.sub(r'[^\w\s]', "", word)
        output_text = '{} {}'.format(output_text, word)
    logging.debug('*** clean_text\n{}'.format(output_text))
    return output_text

def count_search_terms(text, search_term):
    ''' Update df with how many times search_terms occurs in text. '''
    # remove trailing newline characters from the search terms
    search_term = search_term.lower().strip()
    # want complete word matches only, e.g. not 'acat' when looking for 'cat'
    search_term = ' {} '.format(search_term)
    search_term_count = text.count(search_term)
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


def display_df(df):
    logging.info('\nSearch results:\n')
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)


def docx_to_text(filepath):
    ''' Extract text from Word docx files. '''
    logging.info('  processing Word file: {}'.format(os.path.basename(filepath)))
    text = docx2txt.process(filepath)
    # remove punctuation marks
    text = clean_text(text)
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
    for search_term in search_terms:
        search_term_count = count_search_terms(file_text, search_term)
        found_terms_count.append(search_term_count)
    logging.debug('found_terms_count: {}'.format(found_terms_count))
    return found_terms_count


def get_filepath(dir, filename):
    ''' Create filepath. '''
    return os.path.join(dir, filename)


def get_search_terms(dir):
    ''' Extract list of search terms from file.'''
    search_terms = []
    with open(os.path.join(dir, SEARCH_TERMS_FILENAME), 'r') as search_terms_file:
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
            # add this page of text to all_text
            all_text = '{} {}'.format(all_text, page_text)
    # remove punctuation marks
    all_text = clean_text(all_text)
    logging.debug('*** pdf_to_text: {}'.format(all_text))
    return all_text


def sum_df_columns(df):
    ''' Add a row containing column totals to dataframe. '''
    df = df.apply(pd.to_numeric, downcast='signed', errors='ignore')
    # df = df.append(df.sum(numeric_only=True), ignore_index=True)
    totals = df.sum(numeric_only=True)
    totals.name=('Totals')
    df = df.append(totals)
    return df


def update_df(df, filename, found_terms_list):
    ''' Add the found_terms_list as a new row to the dataframe. '''
    found_terms_list.insert(0, filename)
    df.loc[len(df)] = found_terms_list
    return df

@click.command()
@click.option('--dir', default=SCRIPT_DIR, help='Directory containing files.')
def main(dir):
    logging.info('search directory: {}'.format(dir))
    search_terms_filepath = os.path.join(dir, SEARCH_TERMS_FILENAME)
    if not os.path.exists(search_terms_filepath):
        exit_code('search terms file does not exist: {}'.format(search_terms_filepath))
    search_terms = get_search_terms(dir)
    logging.info('searching for Word and pdf files in: {}'.format(dir))
    df = create_dataframe(search_terms)
    for filename in os.listdir(dir):
        logging.info('found {}'.format(filename))

        if filename.endswith('.docx'):
            filepath = get_filepath(dir, filename)
            file_text = docx_to_text(filepath)
            found_terms_list = found_search_terms(file_text, search_terms)
            df = update_df(df, filename, found_terms_list)

        if filename.endswith('.pdf'):
            filepath = get_filepath(dir, filename)
            file_text = pdf_to_text(filepath)
            found_terms_list = found_search_terms(file_text, search_terms)
            df = update_df(df, filename, found_terms_list)

    df = sum_df_columns(df)
    logging.debug('df_head:\n{}'.format(df.head()))
    display_df(df)
if __name__ == '__main__':
    main()
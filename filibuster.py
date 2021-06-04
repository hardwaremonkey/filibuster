import docx2txt
import logging
import os
import PyPDF2

DIR = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.info('started filibuster')
search_terms = ['the', 'relevant']


def count_words(text, search_term):
    ''' Count how many times search_term occurs in text. '''
    text = text.lower().split()
    search_term_count = text.count(search_term.lower())
    return search_term_count


def docx_to_text(filepath):
    ''' Extract text from Word docx files. '''
    logging.info('  processing Word file: {}'.format(os.path.basename(filepath)))
    text = docx2txt.process(os.path.join(DIR, filepath))
    logging.debug(text)
    return text


def get_filepath(dir, filename):
    ''' Create filepath. '''
    return os.path.join(DIR, filename)


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


def count_search_terms(text, search_terms):
    ''' Count the occurrences of search terms in text. '''
    for search_term in search_terms:
        count_word = count_words(text, search_term)
        logging.info('\t{} occurs {} times'.format(search_term, count_word))

def main():
    logging.info('searching for Word and pdf files in: {}'.format(DIR))
    for filename in os.listdir(DIR):
        logging.info('found {}'.format(filename))

        if filename.endswith('.docx'):
            filepath = get_filepath(DIR, filename)
            docx_text = docx_to_text(filepath)
            count_search_terms(docx_text, search_terms)

        if filename.endswith('.pdf'):
            filepath = get_filepath(DIR, filename)
            pdf_text = pdf_to_text(filepath)
            count_search_terms(pdf_text, search_terms)

if __name__ == '__main__':
    main()
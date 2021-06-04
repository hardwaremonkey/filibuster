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


def docx_to_text(filename):
    ''' Extract text from Word docx files. '''
    logging.info('* processing Word file: {}'.format(filename))
    text = docx2txt.process(os.path.join(DIR, filename))
    logging.debug(text)
    return text
    #if any(term in text for term in search_words):
    if ('the' in text):
        term = 'the'
        logging.debug('*** found {}'.format(term))


def pdf_to_text(filename):
    ''' Extract text from pdf files. '''
    logging.info('* processing pdf file: {}'.format(filename))

def main():
    logging.info('searching for Word and pdf files in: {}'.format(DIR))
    for filename in os.listdir(DIR):
        logging.info('found {}'.format(filename))
        if filename.endswith('.docx'):
            docx_text = docx_to_text(filename)
            for search_term in search_terms:
                count_word = count_words(docx_text, search_term)
                logging.info('\t{} occurs {} times'.format(search_term, count_word))

        if filename.endswith('.pdf'):
            pdf_text = pdf_to_text(filename)

if __name__ == '__main__':
    main()
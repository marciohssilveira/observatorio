import re
import pdfplumber
import glob
import os


class PdfExtractor:
    """
    Contains methods to access, read and extract parts of text on a pdf document.
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def get_text_from_pdf(self):
        """
        Utilizes pdfplumber <https://pypi.org/project/pdfplumber/> to read the
        contents of a pdf document.

        Iterates over files in a folder, open and extracts its contents.
        :return: a string
        """
        pdf = pdfplumber.open(self.file_path)
        text = ''
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            text += page.extract_text()
        pdf.close()
        return text

    def get_period_from_text(self):
        """
        Utilizes a regex sentence to find a specific part of the text containing the interval of dates covered for
        each pdf document and stores it in a string.
        :return: a string
        """
        period = re.findall(
            r'(\d{2}[\/ ](\d{2}|Janeiro|Jan|Fevereiro|Fev|Março|Mar|Abril|Abr|Maio|May|Junho|Jun|Julho|Jul|Agosto|Ago|Setembro|Set|Outobro|Out|Novembro|Nov|Dezembro|Dez)[\/ ]\d{2,4})',
            self.get_text_from_pdf())
        interval = period[0][0] + ' a ' + period[1][0]
        return interval

    def get_news_from_text(self):
        """
        Utilizes a regex sentence to find a specific part of the text containing each news itself.
        :return: a list of strings skipping the first one (the summary)
        """
        news = re.findall(r'\d- (.*?)\n \n', self.get_text_from_pdf(), re.DOTALL)
        return news[1:]

    def get_reference_from_news(self):
        """
        Utilizes a regex sentence to find a specific part of the text containing the reference for each news.
        :return: a list containing the reference
        """
        references = []
        for each_new in self.get_news_from_text():
            matches = re.findall(r'\((.*?)\)', each_new, re.DOTALL)
            references.append(matches[-1].replace('\n', ''))
        return references


path = './files'

observatorio = {}
for filename in glob.glob(os.path.join(path, '*.pdf')):  # Navigates through all the files in a specified folder
    pdf = PdfExtractor(filename)
    periods = pdf.get_period_from_text()
    news = pdf.get_news_from_text()
    references = pdf.get_reference_from_news()
    observatorio[periods] = dict(zip(references, news))  # creates a dictionary (periods are the keys) of dictionaries
    # containing the references as keys, the news as values

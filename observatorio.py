import re
import pdfplumber
import glob
import os


class PdfExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_text_from_pdf(self):
        pdf = pdfplumber.open(self.file_path)
        text = ''
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            text += page.extract_text()
        pdf.close()
        return text

    def get_period_from_text(self):
        period = re.findall(
            r'(\d{2}[\/ ](\d{2}|Janeiro|Jan|Fevereiro|Fev|Março|Mar|Abril|Abr|Maio|May|Junho|Jun|Julho|Jul|Agosto|Ago|Setembro|Set|Outobro|Out|Novembro|Nov|Dezembro|Dez)[\/ ]\d{2,4})',
            self.get_text_from_pdf())
        interval = period[0][0] + ' a ' + period[1][0]
        return interval

    def get_news_from_text(self):
        news = re.findall(r'\d- (.*?)\n \n', self.get_text_from_pdf(), re.DOTALL)
        return news[1:]

    def get_reference_from_news(self):
        references = []
        for each_new in self.get_news_from_text():
            matches = re.findall(r'\((.*?)\)', each_new, re.DOTALL)
            references.append(matches[-1].replace('\n', ''))
        return references


path = './sample'

observatorio = {}
for filename in glob.glob(os.path.join(path, '*.pdf')):
    pdf = PdfExtractor(filename)
    periods = pdf.get_period_from_text()
    news = pdf.get_news_from_text()
    references = pdf.get_reference_from_news()
    observatorio[periods] = dict(zip(references, news))
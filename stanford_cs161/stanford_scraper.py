from bs4 import BeautifulSoup
import requests


class Scraper():
    def __init__(self, base_url):
        self.base_url = base_url
        html_text = requests.get(self.base_url).text
        self.soup = BeautifulSoup(html_text, 'lxml')

    def get_all_pdf(self, save_path):
        all_pdf = []
        for url in self.soup.find_all('a'):

            # pick up all 'href' elements that contains 'pdf'
            pdf_link = url.get('href')
            if 'pdf' in pdf_link:

                # append base url if no 'https' available
                if 'https' not in pdf_link:
                    pdf_link = self.base_url+pdf_link
                    all_pdf.append(pdf_link)

                # pick up urls if 'https' available
                elif 'pdf' in pdf_link and 'https' in pdf_link:
                    all_pdf.append(pdf_link)

                # write content into pdf file and save to 'save_path'
                file_name = pdf_link.split('/')[-1]
                file_content = requests.get(pdf_link).content
                with open(save_path + file_name, 'wb') as f:
                    f.write(file_content)

                # check progress
                print('{} has been saved.'.format(file_name))


def main():
    stanford_cs161_scraper = Scraper(
        'https://web.stanford.edu/class/archive/cs/cs161/cs161.1172/')
    stanford_cs161_scraper.get_all_pdf('./materials/')


if __name__ == '__main__':
    main()

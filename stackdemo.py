import requests, os
from bs4 import BeautifulSoup
import pandas as pd
import csv

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}

question_list = []

def get_tag():
    with open('tags.csv', 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            return row


def save_csv():
    header = ['tag', 'title', 'link', 'votes', 'date']
    exists = os.path.exists('stackQuestions.csv')
    with open('stackQuestions.csv', 'a', newline= "") as file:
        csv_writer = csv.DictWriter(file, fieldnames= header)
        if not exists: csv_writer.writeheader()
        try:
            csv_writer.writerows(question_list)
        except:
           pass

def soup_obj(url):
    r = requests.get(url, headers=headers)
    return BeautifulSoup(r.text, 'lxml')

def page_questions(tag, questions):
    for item in questions:
        question = {
            'tag': tag,
            'title' : item.find('a', {'class': 'question-hyperlink'}).text,
            'link' : 'https://stackoverflow.com' + item.find('a', {'class': 'question-hyperlink'})['href'],
            'votes' : int(item.find('span', {'class':  'vote-count-post'}).text),
            'date' : item.find('span', {'class': 'relativetime'})['title'],
        }
        question_list.append(question)

def getQuestions(tag, pages = 3, page_size = 50):
    BASE_URL  = f'https://stackoverflow.com/questions/tagged/{tag}'
    # soup = soup_obj(BASE_URL)
    # pages = int(soup.find_all('a', {'class': 's-pagination--item js-pagination-item'})[-2].text)

    for page in range(1,pages):
        url  = f'{BASE_URL}?tab=Active&page={page}&pagesize={page_size}'
        soup = soup_obj(url)     
        questions = soup.find_all('div', {'class': 'question-summary'})      
        page_questions(tag, questions)
    
    return

if __name__ == "__main__":
    tags = get_tag()
    for tag in tags:
        getQuestions(tag)
    save_csv()
    df = pd.DataFrame(question_list)
    df.to_csv('stackQuestions .csv', index=False)

    print("Done")


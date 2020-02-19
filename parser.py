from bs4 import BeautifulSoup
import requests
import csv
from datetime import date as today_date

#Внутренне представлние новости
class newsinfo:
	def __init__(self, head, text = None, date = None, comm_num = None):
		self.head = head
		self.text = text
		if date != None:
			date = str(today_date.today()) + '-' + date
		self.date = date
		self.comm_num = comm_num
	def __str__(self):
		return str({'head' : self.head, 'text' : self.text, 'date' : self.date, "comm_num" : self.comm_num})
	


def get_list(self):
	return [self.head, self.text, self.date ,self.comm_num] 

def csv_writer(data, path):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)

news_list = []
comm_num = [0]
prefix = 'https://www.zakon.kz'
#Открываем выгруженный сайт(страничку)
with open('test.html', 'r') as inp:
	content = inp.read()
	soup = BeautifulSoup(content, 'lxml')
	#теги с ссылками на новости
	tags = soup.find_all('a', attrs = {"class" : 'tahoma font12', 'target' : '_blank'})
	#теги с информацией о времени публиуации
	times = soup.find_all('span', attrs = {"class" : 'tahoma font12 date n3'})
	times = [t.text for t in times] 
	#для получения числа комментариев, пришлось повозиться
	#если комменты есть, они находятся в теге span с атрибутом class = comm_num
	#если их нет, то и тега нет
	news_lst = soup.find_all('div', attrs = {"class" : 'cat_news_item'})
	comm_num = [0] * len(news_lst)
	for index, news in enumerate(news_lst):
		com_number = 0
		for child in news.children:
			if child.name == 'span' and child['class'] == ['comm_num']:
				com_number = int(child.text)
		comm_num[index] = com_number
	comm_num.pop(0)
	
	for index, tag in enumerate(tags):
	#	print(20 * '*')
	#	print(tag.text)
		req = requests.get(prefix + tag['href'])
		news_soup = BeautifulSoup(req.text, 'lxml')
		#текст может быть в разных тегах как оказалось
		news_tag = news_soup.find('div', id = 'initial_news_story')
		if 'text' not in dir(news_tag):
			news_tag = news_soup.find('div', attrs = {"class" : 'WordSection1'})
		
		#если текста совсем нет
		if 'text' not in dir(news_tag):
			text = tag.text
		else:
			text = news_tag.text
		#print(text)
		#print(20 * '*')
		news_list.append(newsinfo(tag.text, text, times[index], comm_num[index]))

#print(news_list[0].head, '\n', news_list[0].text, '\n', news_list[0].date, '\n',news_list[0].comm_num)
headers = ['head', 'text', 'date', 'comm_num']
ans = [headers]

for news in news_list:
	ans.append(get_list(news))

csv_writer(ans, '14-02-2020.csv')


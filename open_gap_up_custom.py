import json
import pandas
import datetime
import lxml.html as lh
import webbrowser as browser
from requests import get
from bs4 import BeautifulSoup

def main():
	response = input("Enter gap percentage (int): ")
	if response[-1] == "%":
		gap_amount = float(response[:-1])
		get_upper_BB_crossover_tickers(gap_amount)
	else:
		gap_amount = float(response)
		get_upper_BB_crossover_tickers(gap_amount)
	
def get_upper_BB_crossover_tickers(amount):
	url = "https://finviz.com/screener.ashx?v=111&f=ta_gap_u" + str(int(amount)) + "&ft=3"
	html_raw = get(url).content
	"""doc = lh.fromstring(html_raw)
	tables = doc.xpath('//table')
	for table in tables:
		print(table.text_content(), '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
	
	"""
	html_soup = BeautifulSoup(html_raw, "lxml")
	tables = html_soup.find_all('table')
	for table in tables:
		print(table, '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
	
if __name__ == "__main__":
	main()
import requests
from bs4 import BeautifulSoup
import ssl



# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# using the requests module, we use the function get.
result = requests.get("https://edition.cnn.com/")


src = result.content
soup = BeautifulSoup(src, 'html.parser')


# scraping all the A tags that can be found on the page.

links = soup('a')
url_ext = []
title = []

for link in links:
	try:
		# Look at the parts of a link - print('Attrs:', link.attrs)
		url_ext.append(link.attrs['title'])
		title.append(link.attrs['href'])
	except Exception as e:
		print('Tag has no link or title.')
		print('\n')


results = dict(zip(url_ext, title))

for key,value in results.items():
	print(key, '-', value)


# Searching for a specific section of headers to print


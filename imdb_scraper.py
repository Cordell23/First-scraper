import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import pandas as pd
import ssl


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE



website = 'https://www.imdb.com/'
ext = 'search/title-text/?plot='
search = input('Enter movie topic search term: ')

if len(search) < 1:
	# Example search on heros
	url = 'https://www.imdb.com/search/title-text/?plot=heros'
else:
	url = website + ext + search

print(url)


html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

movie_containers = soup.find_all('div', class_= 'lister-item mode-detail')
print(type(movie_containers))
print(len(movie_containers))


# Data scraped from first movie listing to check if code works

first_movie = movie_containers[0]

# Movie title extract
movie_title = first_movie.h3.a.text


# extracting movie release year
movie_year = first_movie.find('span', class_= 'lister-item-year text-muted unbold')

# Movie runtime
runtime = first_movie.p
runtime = runtime.find('span', class_='runtime').text



# Movie rating
rating = first_movie.find('div', attrs = {'name':'ir'})
rating = rating['data-value']





# Loop first 50 movies and scrape relevant data 
movie_titles 	= []
release_years 	= []
runtimes 		= []
ratings 		= []


for container in movie_containers:
	try:
		# Movie titles:
		titles = container.h3.a.text
		movie_titles.append(titles)

		# release year:
		years = container.find('span', class_= 'lister-item-year text-muted unbold').text
		release_years.append(years)

		# Runtimes
		times = container.p
		times = times.find('span', class_='runtime').text
		runtimes.append(times)

		# Ratings:
		rating = container.find('div', attrs = {'name':'ir'})
		rating = rating['data-value']
		ratings.append(rating)

	except Exception as e:
		continue



movie_df = pd.DataFrame.from_dict({
	'Movie': movie_titles,
	'Year': release_years,
	'Length': runtimes,
	'Rating': ratings,
	}, orient='index')

df = movie_df.transpose()

print(df.info())
print(df)

# Export to CSV:
question = input('Would you like to save data to csv? Input Yes or No: ')
if question.lower() == 'no':
	exit()
else:
	location = input('Please enter file pathway: ')
	name = input('Please enter a save name (with .csv extension): ')
	file_name = r'/' + location + name
	df.to_csv(file_name, index= False, header= True)
	print('csv saved...')




''' Next section will be to scrape multiple pages and retrieve same data '''
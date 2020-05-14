import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import pandas as pd
import ssl
from time import sleep
from random import randint
# from time import timestart_time
from IPython.core.display import clear_output

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


print('Scraping by genre & year')

# Genre input
imbd_genres = ['Action', 'Adventure','Animation','Biography','Comedy','Crime','Documentary','Drama','Family','Fantasy','Film-Noir','Game-Show','History','Horror','Music','Musical','Mystery','News','Reality-TV','Romance','Sci-Fi','Sport','Talk-Show','Thriller','War','Western']

for genre in imbd_genres:
	print(genre)

chosen_genre = input('Please choose one of the following genres: ')

# Year range input
print('please choose year ranges for your chosen genre')
try:
	date_1 = input('first year: ')
	date_2 = input('second year: ')
except Exception as e:
	print(e)
	print('Non-valid date input, please try again')
	exit()


def url_gen(genre, date_1, date_2):
	# Putting url together using given parametres
	url = 'https://www.imdb.com/search/title/?release_date='+ date_1 + ',' + date_2 + '&genres=' + chosen_genre + '&start=1&ref_=adv_nxt'
	return url



def next_page(url, num):
    url = url.split('start')
    next_url = url[0] + 'start=' + str(num) + '&ref_=adv_nxt'
    return next_url



url = url_gen(genre, date_1, date_2)
print(url)


pages = [str(i) for i in range(1,5)]




'''
for _ in range(5):
# A request would go here
    requests += 1
    sleep(randint(1,3))
    elapsed_time = time() - start_time
    print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
clear_output(wait= True)
'''



html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

movie_containers = soup.find_all('div', class_= 'lister-item mode-advanced')


# Declaring the lists to store data in
movie_titles    = []
release_years   = []
runtimes        = []
ratings         = []

# Loop for first page of data

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

# looping through following pages
num = 1

for page in pages:
    num = num + 50
    url = next_page(url, num)

    # Preparing the monitoring of the loop
    #start_time = time()
    #requests = 0


    # Make a get request
    html = urllib.request.urlopen(url, context=ctx).read()

    # Pause the loop
    # sleep(randint(8,15))

    '''
    # Monitor the requests
    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)

    # Throw a warning for non-200 status codes
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))

    # Break the loop if the number of requests is greater than expected
    if requests > 72:
        warn('Number of requests was greater than expected.')
        break
    '''


    # Parse the content of the request with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Select all the 50 movie containers from a single page
    movie_containers = soup.find_all('div', class_= 'lister-item mode-advanced')



    # For every movie of these 50
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



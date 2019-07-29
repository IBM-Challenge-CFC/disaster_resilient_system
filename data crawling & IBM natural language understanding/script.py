import bs4 as bs
import urllib.request
import requests

"""This script contains the demo version for the data crawling from the social media (i.e. bbc news)
   and later on applied IBM Watson Natural Language Understanding to generate the trigger with various
   kinds of output including the precautionary measures, necessities and other useful information."""

source = urllib.request.urlopen('https://bbc.com')
soup= bs.BeautifulSoup( source, 'html.parser')

"""For demo we changed disasters to other topics to show how this code
   works, but on deployment the keywords would change
   Currently, the world seems safe as per bbc.com (british news agency)"""
   
#disasters= [ 'volcano', 'volcanic eruption', 'earthquake', 'quake', 'flood', 'typhoon', 'hurricane', 'storm', 'hail', 'disaster', 'rainstorm', 'landslide', 'leakage', 'chemical leakage', 'tornado']
disasters= ['trump', 'immigration', 'diabetes']
#Volcano, Earthquake, Waterflood, Hail, Snow, Tornado, Hurricane
behaviors= ["Stay away from active volcanoes, Use goggles mask and flashlight, Drive rather than walk, Close all windows doors and fireplace, If caught in a rockfall roll into a ball to protect your head","Stay away from active volcanoes, Use goggles mask and flashlight, Drive rather than walk, Close all windows doors and fireplace, If caught in a rockfall roll into a ball to protect your head","Do not wait until you see rising water, Get out of low areas and move to high ground, Do not drive through flooded areas, Keep clear of power lines and electrical wires","Stay Indoors, If driving pull to a safe place so hail doesn't break the windshield","Keep your thermostat as high as possible for as long as you have electricity, Stay inside, Limit travel to emergencies only, Keep pipes from freezing by turning on every water faucet to a slow drip, Wear dry or waterproof clothes, Stay hydrated with plenty of fluids","Go to the basement or take shelter in a small interior ground floor room such as a bathroom closet or hallway, If you have no basement protect yourself by taking shelter under a heavy table or desk, Stay away from windows outside walls and doors","Go to the basement or take shelter in a small interior ground floor room such as a bathroom closet or hallway, If you have no basement protect yourself by taking shelter under a heavy table or desk, Stay away from windows outside walls and doors"]

sites= []
h3s= soup.find_all('h3')
for tag in h3s:
    for keyword in tag.getText().lower().split():
        if keyword in disasters:
            a= tag.find('a', href= True)
            if a:
                sites.append( a['href'])
h2s= soup.find_all( 'h2')
for tag in h2s:
    for keyword in tag.getText().lower().split():
        if keyword in disasters:
            a= tag.find('a', href= True)
            if a:
                sites.append( a['href'])
for i, href in enumerate( sites):
    if 'bbc.com' not in href:
        sites[ i]= ''.join( [ 'bbc.com', href])

headers = {'Content-Type': 'application/json',}
params = (('version', '2018-11-16'),)
responses= []
for site in sites:
    data = '{\n  "url": "' + site + '",\n  "features": {\n    "sentiment": {},\n    "categories": {},\n    "concepts": {},\n    "emotion": {},\n    "entities": {},\n    "keywords": {}\n  }\n}'
    responses.append( requests.post('https://gateway-tok.watsonplatform.net/natural-language-understanding/api/v1/analyze', headers=headers, params=params, data=data, auth=('apikey', 'rwvQDylZAfkwqNKwPqNdmiTt-Hdbd8rL7raHoJe4NMjz')))

news_feed= []
for response in responses:
    #threshold should change during deployment to -0.5
    if response.json()['sentiment']['document']['score'] < 1:
        current_news_feed= dict()
        type_of_disaster= ''
        location= []
        for i in range( 10):
            words= response.json()['keywords'][i]['text'].lower().split()
            for word in words:
                if word in disasters:
                    type_of_disaster= word
                    break
            if len(type_of_disaster) > 0:
                break
        if len( type_of_disaster) > 0:
            current_news_feed[ 'type']= type_of_disaster
            current_news_feed[ 'Country']= ''
            current_news_feed[ 'City']= ''
            for entity in response.json()['entities']:
                if entity['type'] == 'Location':
                    for dis in entity['disambiguation']['subtype']:
                        if dis in [ 'City', 'Country'] and dis not in location:
                            location.append( dis)
                            current_news_feed[ dis]= entity[ 'text']
                if len( location) == 2:
                    break
        if len( current_news_feed) > 0:
            news_feed.append( current_news_feed)


for news in news_feed:
    for i, disaster in enumerate(disasters):
        if news['type'] == disaster:
            city= ''
            country= ''
            if news['Country']:
                country= news['Country']
            if news['City']:
                city= news['City']
            if city or country:
                if city:
                    file = open( city + ".txt", "w")
                else:
                    file = open( country + ".txt", "w")
                file.write(news['type'] + " in " + news['City'] + " " + news[ 'Country'] + "\n" + behaviors[i]) 
        file.close()

# -*- coding: utf-8 -*-
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

print('Saving forusquare client id')
foursquare_client_id = 'WBSAHJNUXI5TCXZ1TNBUE5IX0P1GJNP2NJWNQMLRAYJDHRAO'
print('Saving forusquare client secret')
foursquare_client_secret = 'NKQ4OMCA3L2PFRV3NZVZF2U3WWU215JFRUWLMFIVFJGDHCLI'
print('saving google api key')
google_api_key = 'AIzaSyAOBqpknb1ayz_kyaoL3fKjS2RPMMpKi9Y'

print('Defining getGeocodeLocation')
def getGeocodeLocation(inputString):
    #Replace Spaces with '+' in URL
    locationString = inputString.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'% (locationString, google_api_key))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    #print response
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return (latitude, longitude)

#This function takes in a string representation of a location and cuisine type geocodes the location, and then pass in the latitude and longitude coordinates to the Foursquare API
print('Defining findARestaurant')
def findARestaurant(mealType, location):
    latitude, longitude = getGeocodeLocation(location)
    url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s' % (foursquare_client_id, foursquare_client_secret,latitude,longitude,mealType))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result['response']['venues']:
        #Grab the first restaurant
        restaurant = result['response']['venues'][0]
        venue_id = restaurant['id']
        restaurant_name = restaurant['name']
        restaurant_address = restaurant['location']['formattedAddress']
        #Format the Restaurant Address into one string
        address = ''
        for i in restaurant_address:
            address += i + ' '
        restaurant_address = address
        
        #Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
        url = url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % ((venue_id,foursquare_client_id,foursquare_client_secret)))
        result = json.loads(h.request(url, 'GET')[1])
        #Grab the first image
        #if no image available, insert default image url
        if result['response']['photos']['items']:
            firstpic = result['response']['photos']['items'][0]
            prefix = firstpic['prefix']
            suffix = firstpic['suffix']
            imageURL = prefix + '300x300' + suffix
        else:
            imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"
            
        restaurantInfo = {'name':restaurant_name, 'address': restaurant_address, 'image':imageURL}
        return restaurantInfo
    else:
        return "No Restaurants Found"

    
print('testing findARestaurant')
if __name__ == '__main__':
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland") 
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney Austrailia")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
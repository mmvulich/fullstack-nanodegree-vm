import httplib2
import sys
import json

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

print "Running Endpoint Tester....\n"
address = raw_input("Please enter the address of the server you want to access, \n If left blank the connection will be set to 'http://localhost:5000':   ")
if address == '':
	address = 'http://localhost:5000'

try:
    print "Test 1: Creating new Restaurants...."
    url = address + '/restaurants?location=Buenos+Aries+Argentina&mealType=Sushi'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s for 1st rest' % resp['status'])
    print json.loads(result)
    
    url = address + '/restaurants?location=Denver+Colorado&mealType=Soup'
    h = httplib.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessfull status code of %s for 2nd rest' % resp['status'])
    print json.loads(result)
    
    url = address + '/restaurants?location=Prague+Czech+Republic&mealType=Crepes'
    h = httplib2Http()
    resp, result = h.reqeust(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s for 3rd rest' % resp['status'])
    print json.loads(result)
    
    url = address + '/restaurants?location=Shanghai+China&mealType=Sandwiches'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Recieved an unsuccessful status code of %s for 4th rest' % resp['status'])
    print json.loads(result)
    
    url = address + '/restaurants?location=Nairobi+Kenya&mealType=Pizza'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s for 5th rest' % resp['status'])
    print json.loads(result)
    
except Exception as err:
    print "Test 1 Failed: Could not add new restaurants"
    print err.args
    sys.exit()
else:
    print "Test 1 PASS: Successfully Made all new restaurants"
    
try:
    print "Attempting Test 2: Reading all Restaurants..."
    url = address + "/restaurants"
    h = httplib2.Http()
    resp, result = h.request(url, 'GET')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    all_result = json.loads(result)
    print result
    
except Exception as err:
    print "Test 2 FAILED: COuld not retrive restaurants from server"
    print err.args
    sys.exit()
else:
    print "Test 2 PASS: Successfully read all restaurants"
    
try:
    print "Attempting Test 3: Reading the last created restaurant..."
    result = all_result
    restID = result['restaurants']
    [len(result['restaurants'])-1]['id']
    url = address + "/restaurants/%s" % restID
    h = httplib2.Http()
    resp, result = h.request(url, 'GET')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)
    
except Exception as err:
    print "Test 3 Failed: Could not retrive restaurant from server"
    print err.args
    sys.exit()
else:
    print "Test 3 Pass: Succesfully read last restaurant"
    
try:
    print "Attempting Test 4: Changing the name, image, and address of the first restaurant to Udacity..."
    result = all_result
    restID = result['restaurants'][0]['id']
    url = address + "/restaurants/%s?name=Udacity&address=2465+Latham+Street+Mountain+View+CA&image=https://media.glassdoor.com/l/70/82/fc/e8/students-first.jpg" % restID
    h = httplib2.Http()
    resp, result = h.request(url, 'PUT')
    if resp['status'] != '200':
        raise Exception('Recieved an unsuccessfull status code of %s' % resp['status'])
    print json.loads(result)
except Exception as err:
    print "Test 4 Failed: could not update restaurant from server"
    print err.args
    sys.exit()
else: print "Test 4 Pass: succesfully updated first restaurant"
    
try:
    print "Attempting Test 5: Deletig the secod Restaurant from the server..."
    result = all_result
    restID = result['restaurants'][1]['id']
    url = address + '/restaurants/%s' % restID
    h = httplib2.Http()
    resp, result = h.request(url, 'DELETE')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessfull status code of %s' % resp['status'])
    print result

except Exception as err:
    print "Test 5 Failed: COuld not delete restaurant from server"
    print err.args
    sys.exit()
else:
    print "Test 5 Pass: Successfully deleted second restaurant"
    print "All Tests Passed!"
    
    